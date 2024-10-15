#include <Keypad.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>

//UART setup
// Define the pins for RX and TX
#define RXD 25
#define TXD 14


// for the keypad
#define ROWS  4
#define COLS  4

// Configuration
//replace with wifi credentials
const char* ssid = "Asgard16";
const char* password = "14MTH0R16";
const char* tokenUrl = "https://smart-pharmacist-production.up.railway.app/api/token/";
const char* esp32Url = "https://smart-pharmacist-production.up.railway.app/api/esp32/";
const char* vendingMachineUrl = "https://smart-pharmacist-production.up.railway.app/api/vending-machines/1/"; //the integer in the url corresponds to a Vending Machine ID

const uint8_t vendingMachineId = 1; //used in the fetchVendingSlots method to update inventory of the correct vending machine

//Buzzer Initialisation
const int buzzerPin = 15;

// SSL Root Certificate for HTTPS (replace with your server’s certificate)
const char* root_ca = R"literal(
-----BEGIN CERTIFICATE-----
...
-----END CERTIFICATE-----
)literal";

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


// Global variable to keep track of the motor's current slot
//uint8_t currentSlot = 1;  // Assuming the motor starts at slot 1 (or a known home position)
int currentSlot = 1;

void setup() {

  Serial.begin(9600);
  Serial2.begin(9600, SERIAL_8N1, RXD, TXD);  

  // Initialise the Buzzer 
  pinMode(buzzerPin, OUTPUT);

  // Initialize the LCD
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Connecting WiFi...");

  // Connect to WiFi
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
    delay(2000);

    // Turn the buzzer on
    digitalWrite(buzzerPin, HIGH);
    delay(500);  // Wait for 1 second
    digitalWrite(buzzerPin, LOW);


    // Get the current slot from the server
    if (getCurrentSlotFromServer()) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Slot: " + String(currentSlot));  // Show the current slot on LCD
      delay(3000);
    } else {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Slot Fetch Failed");
    }
    displayReadyMessage();  // Display the scrolling ready message
  } else {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Auth Failed");
  }
}

// Function to get the current_slot from the server
bool getCurrentSlotFromServer() {
  if (WiFi.status() == WL_CONNECTED) {  

    WiFiClientSecure client;
    client.setCACert(root_ca);  // Attach the SSL certificate

    HTTPClient http;

    http.begin(client, vendingMachineUrl);  // Use HTTPS with secure client
    http.addHeader("Content-Type", "application/json");
    http.addHeader("Authorization", "Bearer " + jwtToken);

    int httpResponseCode = http.GET();  // Send GET request

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Response: " + response);

      // Parse the JSON response to extract current_slot
      DynamicJsonDocument doc(1024);
      DeserializationError error = deserializeJson(doc, response);

      if (error) {
        Serial.println("JSON deserialization failed!");
        http.end();
        return false;
      }

      // Extract current_slot from the response
      currentSlot = doc["current_slot"];
      Serial.println("Current Slot: " + String(currentSlot));
      
      //send the currentSlot to the uno to setup
      Serial2.println(String(currentSlot));
      Serial.println("Sent to Arduino: " + String(currentSlot));

      http.end();  // Close the connection
      return true;

    } else {
      Serial.println("Error on HTTP request: " + String(httpResponseCode));
      http.end();
      return false;
    }
  } else {
    Serial.println("WiFi Disconnected");
    return false;
  }
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
  WiFiClientSecure client;
  client.setCACert(root_ca);  // Attach the SSL certificate

  HTTPClient http;
  http.begin(client, tokenUrl);  // Use HTTPS with secure client

  String postData = "{\"username\":\"vending_machine1\",\"password\":\"VKG@1234\"}";
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
  WiFiClientSecure client;
  client.setCACert(root_ca);  // Attach the SSL certificate

  HTTPClient http;
  http.begin(client, esp32Url);  // Use HTTPS with secure client

  http.addHeader("Content-Type", "application/json");
  http.addHeader("Authorization", "Bearer " + jwtToken);

  String postData = "{\"code\":\"" + inputCode + "\", \"current_slot\": " + String(currentSlot) + ", \"vending_machine_id\": " + String(vendingMachineId) + "}";
  int httpResponseCode = http.POST(postData);

  std::vector<int> vendingSlots;

  if (httpResponseCode > 0) {
    // Turn the buzzer on
    digitalWrite(buzzerPin, HIGH);
    delay(250);  
    
    // Turn the buzzer off
    digitalWrite(buzzerPin, LOW);
    delay(250);

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
      // Turn the buzzer on
      digitalWrite(buzzerPin, HIGH);
      delay(250);  
      
      // Turn the buzzer off
      digitalWrite(buzzerPin, LOW);
      delay(250);

      digitalWrite(buzzerPin, HIGH);
      delay(250);  
      
      // Turn the buzzer off
      digitalWrite(buzzerPin, LOW);
      delay(250);  

      Serial.println("Error: 'vending_slots' not found in the response");
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Mwalakwisa code");
      lcd.setCursor(1, 0);
      lcd.print("kapena mankhwala atha");
      //buzzer must beep twice quickly
    }

  } else {
      // Turn the buzzer on
      digitalWrite(buzzerPin, HIGH);
      delay(250);  
      
      // Turn the buzzer off
      digitalWrite(buzzerPin, LOW);
      delay(250);

      digitalWrite(buzzerPin, HIGH);
      delay(250);  
      
      // Turn the buzzer off
      digitalWrite(buzzerPin, LOW);
      delay(250);  

      digitalWrite(buzzerPin, HIGH);
      delay(250);  
      
      // Turn the buzzer off
      digitalWrite(buzzerPin, LOW);
      delay(250);  

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Error: No Resp");
    Serial.println("Error: No response from server");
  }

  http.end();
  return vendingSlots;
}


//uno function
void createDispensation(std::vector<int> vendingSlots) {
  // Rotate motor based on each vending slot received
  if (!vendingSlots.empty()) {
    for (int slot : vendingSlots) {
      // send the slot over serial to trigger uno's motor rotate function.
      Serial2.println(String(slot));
      Serial.println("Sent Target Slot: " + String(slot));
      // need a flag to determine whether the uno completed the rotation, atp the flag is false
      // when OK status the flag is set to true so the next iteration can happen
      currentSlot = slot;
      updateCurrentSlotOnServer(currentSlot); //called when OK status is received
      delay(1000);  // Simulate delay for dispensing medication
    }
  } else {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("No Slots Found");
  }
}




void updateCurrentSlotOnServer(int slot) {
  WiFiClientSecure client;
  client.setCACert(root_ca);  // Attach the SSL certificate

  HTTPClient http;

  http.begin(client, vendingMachineUrl);  // Use HTTPS with secure client
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Authorization", "Bearer " + jwtToken);

  // Create JSON data for the PATCH request
  DynamicJsonDocument doc(256);
  doc["current_slot"] = slot;  // Update with the current slot
  String requestBody;
  serializeJson(doc, requestBody);

  // Send the PATCH request
  int httpResponseCode = http.PATCH(requestBody);

  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("Successfully updated current_slot: " + response);
  } else {
    Serial.print("Error updating current_slot: ");
    Serial.println(httpResponseCode);
  }

  http.end();
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
  static int scrollPos = 0;

  if (millis() - lastScrollTime >= 300) {  // Adjust the scroll speed here
    lastScrollTime = millis();
    lcd.setCursor(0, row);
    lcd.print(message.substring(scrollPos, scrollPos + 16));
    scrollPos++;
    if (scrollPos > message.length()) {
      scrollPos = 0;  // Reset scroll position to start again
    }
  }
}