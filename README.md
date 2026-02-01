<img width="2816" height="1536" alt="RFID" src="https://github.com/user-attachments/assets/088d10d9-9519-4dab-8f18-e235da758768" />

# 🚪🤖 Multimodal Smart Turnstile System

A high-security **Multimodal Intelligent Access Control System** that combines **Computer Vision (AI)** and **IoT (RFID)** for dual-factor authentication.  
Built with **Python + Arduino**, designed for real-world secure entry scenarios such as campuses, labs, and smart buildings.

---

## 🌟 Key Features

- **Dual-Factor Authentication**
  - Access granted only when:
    - Face recognition is successful  
    - Correct RFID card is detected

- **Real-time AI Face Recognition**
  - Powered by:
    - `face_recognition`
    - `OpenCV`

- **IoT Hardware Integration**
  - Dual Arduino architecture  
  - Independent sensor & actuator management

- **Multithreaded System**
  - Parallel handling of:
    - Camera stream  
    - Serial communication  
  - Zero-lag performance

- **Security Feedback**
  - LCD messages  
  - Buzzer alerts  
  - LED indicators  
  - Servo-controlled gate

---

## 🛠 Hardware Stack

| Component | Model / Type |
|------|---------------|
| Camera | USB Webcam |
| RFID | MFRC522 Module |
| Motor | SG90 Servo |
| Display | 16x2 LCD |
| Alerts | Buzzer |
| Indicators | Green & Red LEDs |
| Controllers | 2x Arduino Uno |

---

## 💻 Software Stack

- **Language:** Python 3.x  
- **Core Libraries:**
  - `face_recognition` – biometric encoding & matching  
  - `opencv-python` – image processing  
  - `pyserial` – Arduino communication  

- **Architecture**
  - Multithreading  
  - Serial protocol  
  - Modular design  

---

## 🧠 System Workflow

1. User approaches turnstile  
2. Camera captures face  
3. System checks biometric database  
4. RFID card is scanned  
5. If BOTH match → gate opens  
6. Otherwise → access denied alert

---

## 📁 Project Structure

```
Multimodal-Smart-Turnstile-System
│
├── software
│   ├── main.py
│   ├── requirements.txt
│   └── database/
│        └── authorized_faces/
│
├── hardware
│   ├── gate-control/
│   │    └── gate-control.ino
│   └── rfid-reader/
│        └── rfid-reader.ino
│
└── docs/
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone [https://github.com/Emirkaraman9/Multimodal-Smart-Turnstile-System.git](https://github.com/Emirkaraman9/Multimodal-Smart-Turnstile-System.git)
cd Multimodal-Smart-Turnstile-System
```

### 2. Install Python Requirements

```bash
pip install -r software/requirements.txt
```

### 3. Flash Arduino Devices

- Upload to **Arduino 1**
```
hardware/gate-control/gate-control.ino
```

- Upload to **Arduino 2**
```
hardware/rfid-reader/rfid-reader.ino
```

### 4. Prepare Face Database

- Add images of authorized users:

```
software/database/
```

- Each user should have:
  - Clear front face image  
  - Proper lighting  
  - Unique filename

### 5. Run the System

```bash
python software/main.py
```

---

## 🛡 Security Design

- Two independent verification layers  
- Serial data validation  
- Timeout protection  
- False access prevention  
- Real-time alerts

---

## ⚠ Limitations

- Requires good lighting  
- Camera quality affects accuracy  
- Single face per frame recommended  
- RFID must be pre-registered

---

## 🎯 Future Improvements

- Mobile app integration  
- Cloud logging  
- Liveness detection  
- Encrypted serial protocol  
- Multi-camera support

---

## 📝 License

Developed for **educational and research purposes**.
