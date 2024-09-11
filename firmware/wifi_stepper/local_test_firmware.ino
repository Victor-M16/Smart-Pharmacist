#include <Stepper.h>
#include <Keypad.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <vector>

// for the stepper motor
const int steps_per_rev = 200;  // Set to 200 for NEMA 17
#define IN1 14
#define IN2 27
#define IN3 26
#define IN4 25

// for the keypad
#define ROWS  4
#define COLS  4

// Configuration
const char* ssid = "Asgard16";
const char* password = "14MTH0R16";
const char* tokenUrl = "http://192.168.8.168:8000/api/token/";
const char* esp32Url = "http://192.168.8.168:8000/api/esp32/";

const uint8_t vendingMachineId = 1;

// configure the keypad
char keyMap[ROWS][COLS] = {
  {'1','2','3', 'A'},
  {'4','5','6', 'B'},
  {'7','8','9', 'C'},
  {'*','0','#', 'D'}
};

uint8_t rowPins[ROWS] = {33, 32, 18, 19};  // GPIO33, GPIO32, GPIO18, GPIO19
uint8_t colPins[COLS] = {4, 5, 16, 17};    // GPIO4, GPIO5, GPIO16, GPIO17
Keypad keypad = Keypad(makeKeymap(keyMap), rowPins, colPins, ROWS, COLS);

uint8_t LCD_CursorPosition = 6;  // Start after "Code: "
bool isReady = true;  // Flag to indicate if the system is in ready state
String jwtToken = "";
String inputCode = "";

// configure the display
LiquidCrystal_I2C lcd(0x27, 16, 2);  // set the LCD address to 0x27 for a 16 chars and 2 line display

// configure the motor
Stepper motor(steps_per_rev, IN1, IN2, IN3, IN4);

// Global variable to keep track of the motor's current slot
uint8_t currentSlot = 1;  // Assuming the motor starts at slot 1 (or a known home position)

void setup() {
  Serial.begin(115200);

  // initialize the motor speed
  motor.setSpeed(60);

  // initialize the LCD
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Connecting WiFi...");

  // connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected to WiFi");
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("WiFi Connected");

  // Authenticate and get JWT token
  if (authenticate()) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Authenticated");
    delay(3000);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Code: ");
  } else {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Auth Failed");
  }

  displayReadyMessage();  // Display the scrolling ready message
}

void loop() {
  if (isReady) {
    displayReadyMessage();
  }

  char key = keypad.getKey();

  if (key) {
    if (isReady) {
      lcd.clear();
      isReady = false;  // Stop displaying the ready message once input starts
      lcd.setCursor(0, 0);
      lcd.print("Code: ");
      lcd.setCursor(0, 1);
      lcd.print("Kuyambanso: C");
    }

    if (key == 'C') {
      resetToReadyState();
    } else {
      Serial.print(key);

      lcd.setCursor(LCD_CursorPosition++, 0);
      lcd.print(key);
      inputCode += key;  // Append the key to the input code

      if (inputCode.length() == 4) {
        processCode(inputCode);
        resetToReadyState();
      }
    }
  }
}

// API functions
bool authenticate() {
  HTTPClient http;
  http.begin(tokenUrl);  

  String postData = "{\"username\":\"****\",\"password\":\"***\"}";
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(postData);

  if (httpResponseCode > 0) {
    String response = http.getString();
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, response);
    jwtToken = doc["access"].as<String>();  // Extract the JWT token
    Serial.println("Authenticated. JWT Token: " + jwtToken);
    http.end();
    return true;
  } else {
    Serial.print("Error on sending POST: ");
    Serial.println(httpResponseCode);
    http.end();
    return false;
  }
}

std::vector<int> fetchVendingSlots() {
  HTTPClient http;
  http.begin(esp32Url);  // Use HTTP without secure client

  http.addHeader("Content-Type", "application/json");
  http.addHeader("Authorization", "Bearer " + jwtToken);

  String postData = "{\"code\":\"" + inputCode + "\", \"current_slot\": " + String(currentSlot) + ", \"vending_machine_id\": " + String(vendingMachineId) + "}";
  int httpResponseCode = http.POST(postData);

  std::vector<int> vendingSlots;

  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("Response: " + response);

    // Parse the JSON response
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, response);

    // Check if "vending_slots" is present
    if (doc.containsKey("vending_slots")) {
      JsonArray slots = doc["vending_slots"].as<JsonArray>();
      
      // Iterate through the array and populate the list
      for (int i = 0; i < slots.size(); i++) {
        vendingSlots.push_back(slots[i].as<int>());
      }
    } else {
      Serial.println("Error: 'vending_slots' not found in the response");
    }

  } else {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Error: No Resp");
    Serial.println("Error: No response from server");
  }

  http.end();
  return vendingSlots;
}

void createDispensation(std::vector<int> vendingSlots) {
  // Rotate motor based on each vending slot received
  if (!vendingSlots.empty()) {
    for (int slot : vendingSlots) {
      rotateMotorToSlot(slot);  // Rotate to the correct slot
      delay(1000);  // Simulate delay for dispensing medication
    }
  } else {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("No Slots Found");
  }
}

void rotateMotorToSlot(int slot) {
  int steps_per_slot = steps_per_rev / 6;  // Assuming 6 slots for the motor rotation
  int targetSlot = slot; 

  // Calculate the difference in steps based on the current position
  int slotDifference = targetSlot - currentSlot;  // Difference between target and current slot
  int steps_to_move = steps_per_slot * slotDifference;  // Steps needed to move to the target slot

  // Rotate the motor by the calculated number of steps
  motor.step(steps_to_move);  

  // Update the currentSlot to reflect the new position
  currentSlot = targetSlot;

  // Provide feedback on the LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Vending slot: ");
  lcd.setCursor(0, 1);
  lcd.print(slot);

  // Print the action to the serial monitor for logging
  Serial.println("Dispensing medication at slot: " + String(slot));
  delay(3000);
}

// Main logic
void processCode(String code) {
  Serial.println("\nProcessing Code: " + code);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Code yanu: " + code);

  lcd.setCursor(0, 1);
  lcd.print("Dikilani pangono");

  std::vector<int> vendingSlots = fetchVendingSlots(); 

  Serial.println("slots fetched successfully");

  createDispensation(vendingSlots);  // Call the function to dispense medication
  Serial.println("medication dispensed");

}

// LCD functions
void resetToReadyState() {
  inputCode = "";  // Clear the input code
  LCD_CursorPosition = 6;  // Reset position after "Code: "
  lcd.clear();
  isReady = true;
  displayReadyMessage();  // Display the ready message again
}

void displayReadyMessage() {
  scrollMessage("Ready. Lowetsani Vending Code ", 0);  // Scroll on the top row
}

void scrollMessage(String message, uint8_t row) {
  static unsigned long lastScrollTime = 0;
  static uint8_t startIndex = 0;

  if (millis() - lastScrollTime > 300) {
    lcd.clear();
    lcd.setCursor(0, row);
    lcd.print(message.substring(startIndex));
    startIndex++;
    if (startIndex > message.length()) {
      startIndex = 0;
    }
    lastScrollTime = millis();
  }
}
