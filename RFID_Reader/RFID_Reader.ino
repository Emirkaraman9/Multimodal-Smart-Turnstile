#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9   // RFID reset pini
#define SS_PIN 10   // RFID SDA/SS pini

MFRC522 rfid(SS_PIN, RST_PIN);
// TX = 1, RX = 0 (USB ile bağlıyken bunlara dokunma)
void setup() {
  Serial.begin(9600); // Python veya Arduino 1 için USB
  SPI.begin();
  rfid.PCD_Init();
  Serial.println("RFID hazır...");
}

void loop() {
  // Yeni kart var mı kontrol et
  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial()) return;

  // UID oluştur
  String uidStr = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    if (rfid.uid.uidByte[i] < 0x10) uidStr += "0";
    uidStr += String(rfid.uid.uidByte[i], HEX);
  }
  uidStr.toUpperCase();

  // Python'a ve Arduino 1'e gönder
  Serial.print("UID:");
  Serial.println(uidStr);

  // Kart okutulmasını önlemek için kısa bekleme
  rfid.PICC_HaltA();
  delay(500);
}