import cv2
import face_recognition
import serial
import time
import os
import numpy as np
from PIL import Image
import threading

# ---------- AYARLAR ----------
KNOWN_FACES_DIR = r"C:\Users\emirk\OneDrive\Ekler\Masaüstü\face_recognition\face_recognition\Data_base"
COM_RFID = "COM6"   # Arduino 2
COM_GATE = "COM5"   # Arduino 1
BAUDRATE = 9600
FACE_THRESHOLD = 0.45
# -------------------------------

user_uid_map = {
    "Emir": "5E031B06",
    "Ali": "B387E62C"
}

def load_known_faces(folder):
    known_encodings = []
    known_names = []
    print("Yüzler yükleniyor...")
    if not os.path.exists(folder): return [], []
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            try:
                image = face_recognition.load_image_file(os.path.join(folder, filename))
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    known_encodings.append(encodings[0])
                    known_names.append(os.path.splitext(filename)[0])
            except: pass
    return known_encodings, known_names

# --- RFID İŞLEM FONKSİYONU ---
def check_rfid_for_face(name, ser_rfid, ser_gate, processing_faces):
    expected_uid = user_uid_map.get(name, "")
    start_time = time.time()
    timeout = 15 
    
    print(f"\n>>> {name} İÇİN İŞLEM BAŞLADI <<<")
    print("Lütfen Kartı Okutun...")

    # Arabellek temizliği (Eski veriyi sil)
    ser_rfid.reset_input_buffer()
    
    access_granted = False

    try:
        while time.time() - start_time < timeout:
            if ser_rfid.in_waiting > 0:
                try:
                    line = ser_rfid.readline().decode(errors="ignore").strip()
                    if "UID:" in line:
                        uid = line.replace("UID:", "").strip().upper().replace(" ", "")
                        print(f"Okunan: {uid}")
                        
                        if uid == expected_uid:
                            print(f"✅ EŞLEŞTİ: {name}. Kapı açılıyor...")
                            
                            # --- SERVONUN ÇALIŞMASI İÇİN KRİTİK KISIM ---
                            ser_gate.write(b"access_granted\n") 
                            ser_gate.flush() # Python'u veriyi göndermeye zorla!
                            # --------------------------------------------
                            
                            access_granted = True
                            break
                        else:
                            print(f"❌ REDDEDİLDİ.")
                            ser_gate.write(b"access_denied\n")
                            ser_gate.flush()
                            break
                except: pass
            time.sleep(0.05)

        if not access_granted:
            print(f"⏳ SÜRE DOLDU: {name}")
            ser_gate.write(b"access_denied\n")
            ser_gate.flush()

    finally:
        # --- İŞLEM BİTTİ, SİSTEMİ SIFIRLA ---
        print(f"🔄 {name} için sistem soğuyor (4 saniye)...")
        time.sleep(4) # Arduino'nun kapıyı açıp kapatması için süre tanı
        
        # İsmi listeden sil ki tekrar okutabilsin
        if name in processing_faces:
            processing_faces.remove(name)
            
        # Tamponu bir sonraki kişi için temizle
        ser_rfid.reset_input_buffer()
        print("--- SİSTEM HAZIR ---\n")

def main():
    known_encodings, known_names = load_known_faces(KNOWN_FACES_DIR)

    # Bağlantıları aç
    try:
        ser_rfid = serial.Serial(COM_RFID, BAUDRATE, timeout=1)
        ser_gate = serial.Serial(COM_GATE, BAUDRATE, timeout=1)
        time.sleep(2) # Arduino'ların resetlenmesini bekle
        print("✅ Bağlantılar Tamam.")
    except Exception as e:
        print(f"HATA: {e}")
        return
    

    cap = cv2.VideoCapture(0)
    processing_faces = set() # Şu an işlem yapılan kişilerin listesi

    print("Sistem Aktif.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        # Yüz tanıma işlemleri (Hız için resmi küçültebilirsin ama şart değil)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            top, right, bottom, left = face_location
            name = "Unknown"
            matched = False

            if known_encodings:
                distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_idx = np.argmin(distances)
                if distances[best_idx] < FACE_THRESHOLD:
                    name = known_names[best_idx]
                    matched = True

            color = (0, 255, 0) if matched else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            # EĞER KİŞİ TANINDI VE ŞU AN İŞLEM GÖRMÜYORSA
            if matched and name not in processing_faces:
                processing_faces.add(name) # Listeye ekle (KİLİTLE)
                
                # Arka planda RFID kontrolünü başlat
                threading.Thread(target=check_rfid_for_face, 
                                 args=(name, ser_rfid, ser_gate, processing_faces), 
                                 daemon=True).start()

        cv2.imshow("Turnike", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()
    ser_rfid.close()
    ser_gate.close()

if __name__ == "__main__":
    main()
    