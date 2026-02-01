#include <LiquidCrystal.h>
#include <Servo.h>

// LCD pinleri 
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
Servo servo_motor;

int buzzer = 10;
int greenLed = 7;
int redLed = 8;

void setup() {
  Serial.begin(9600); // Python’dan komutları okuyacak
  servo_motor.attach(6);

  pinMode(buzzer, OUTPUT);
  pinMode(greenLed, OUTPUT);
  pinMode(redLed, OUTPUT);

  lcd.begin(16, 2);
  servo_motor.write(0);

  // Başlangıç ekranı
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Kart ve Yuz");
  lcd.setCursor(0, 1);
  lcd.print("bekleniyor...");
  digitalWrite(redLed, HIGH);
  digitalWrite(greenLed, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "access_granted") {
      accessGranted();
    } else if (cmd == "access_denied") {
      accessDenied();
    }
  }
}

void accessGranted() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Hos Geldiniz");

  digitalWrite(greenLed, HIGH);
  digitalWrite(redLed, LOW);
  servo_motor.write(90);
  buzzerBeep(3, 200); // kısa bipler
  servo_motor.write(0);

  digitalWrite(greenLed, LOW);
  digitalWrite(redLed, HIGH);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Yeni karti okutun");
}

void accessDenied() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Gecis reddedildi");
  digitalWrite(buzzer, HIGH);
  delay(1000);
  digitalWrite(buzzer, LOW);

  servo_motor.write(0);
  digitalWrite(greenLed, LOW);
  digitalWrite(redLed, HIGH);
}

void buzzerBeep(int times, int duration) {
  for (int i = 0; i < times; i++) {
    digitalWrite(buzzer, HIGH);
    delay(duration);
    digitalWrite(buzzer, LOW);
    delay(200);
  }
}