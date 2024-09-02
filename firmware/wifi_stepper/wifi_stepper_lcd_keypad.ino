#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <AccelStepper.h>
#include <Keypad.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Wi-Fi credentials
const char* ssid = "your-SSID";
const char* password = "your-PASSWORD";

// Keypad setup
const byte ROWS = 4;
const byte COLS = 4;
char keys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};
byte rowPins[ROWS] = {14, 27, 26, 25};
byte colPins[COLS] = {33, 32, 35, 34};
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// Stepper setup
AccelStepper stepper(AccelStepper::FULL4WIRE, 12, 14, 27, 26);
#define STEPS_PER_SLOT 200 // Example value, set according to your hardware

// LCD setup
LiquidCrystal_I2C lcd(0x27, 16, 2); // Adjust the address to match your LCD

String getPrescriptionSlot(String code) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String serverPath = "http://your-django-api-url/prescriptions/?code=" + code;
    
    http.begin(serverPath);
    int httpResponseCode = http.GET();

    if (httpResponseCode == 200) {
      String payload = http.getString();
      DynamicJsonDocument doc(1024);
      deserializeJson(doc, payload);
      String slot = doc[0]["slot"].as<String>();
      return slot;
    } else {
      Serial.println("Error on HTTP request");
      return "";
    }
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
    return "";
  }
}

void rotateToSlot(String slot) {
  int targetPosition = slot.toInt() * STEPS_PER_SLOT;
  stepper.moveTo(targetPosition);
  stepper.runToPosition();
}

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Initialize the stepper motor
  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(500);

  // Initialize the LCD
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.print("Ready");
}

String code = "";
void loop() {
  char key = keypad.getKey();
  
  if (key) {
    Serial.println(key);
    code += key;

    // Display the entered code on the LCD
    lcd.clear();
    lcd.print("Code: ");
    lcd.print(code);

    if (code.length() == 4) {
      Serial.print("Code entered: ");
      Serial.println(code);
      
      // Display processing message on the LCD
      lcd.clear();
      lcd.print("Checking...");
      
      String slot = getPrescriptionSlot(code);
      if (slot != "") {
        Serial.print("Slot found: ");
        Serial.println(slot);
        
        // Display success and slot number on the LCD
        lcd.clear();
        lcd.print("Slot: ");
        lcd.print(slot);

        // Rotate to the corresponding slot
        rotateToSlot(slot);
      } else {
        Serial.println("Invalid Code");

        // Display error message on the LCD
        lcd.clear();
        lcd.print("Invalid Code");
      }
      
      // Reset code
      code = "";
      delay(2000); // Pause for 2 seconds before clearing the display
      lcd.clear();
      lcd.print("Ready");
    }
  }
}
