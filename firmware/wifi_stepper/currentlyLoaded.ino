#include <Keypad.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define ROWS  4
#define COLS  4


// Configuration
const char* ssid = "Asgard16";
const char* password = "14MTH0R16";
const char* tokenUrl = "http://192.168.8.168:8000/api/token/";
const char* esp32Url = "http://192.168.8.168:8000/api/esp32/";

char keyMap[ROWS][COLS] = {
  {'1','2','3', 'A'},
  {'4','5','6', 'B'},
  {'7','8','9', 'C'},
  {'*','0','#', 'D'}
};

uint8_t rowPins[ROWS] = {14, 27, 26, 25}; // GIOP14, GIOP27, GIOP26, GIOP25
uint8_t colPins[COLS] = {33, 32, 18, 19}; // GIOP33, GIOP32, GIOP18, GIOP19
Keypad keypad = Keypad(makeKeymap(keyMap), rowPins, colPins, ROWS, COLS );

uint8_t LCD_CursorPosition = 6;  // Start after "Code: "
bool isReady = true;  // Flag to indicate if the system is in ready state
String jwtToken = "";
String inputCode = "";

LiquidCrystal_I2C lcd(0x27, 16, 2);  // set the LCD address to 0x27 for a 16 chars and 2 line display

void setup() {
  Serial.begin(115200);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Connecting WiFi...");

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


//API functions
bool authenticate() {
  HTTPClient http;
  String postData = "{\"username\":\"vending_machine1\",\"password\":\"VKG@1234\"}";

  // HTTPS requires certificate handling
  http.begin(tokenUrl); // This may require additional security setup for HTTPS
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

void fetchVendingSlots() {
  HTTPClient http;
  http.begin(esp32Url);  // Using the base URL without query parameters

  http.addHeader("Content-Type", "application/json");
  http.addHeader("Authorization", "Bearer " + jwtToken);

  String postData = "{\"code\":\"" + inputCode + "\"}";  // Send the code in the body as JSON
  int httpResponseCode = http.POST(postData);

  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.print("Response: "+ response);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Response:");
    lcd.setCursor(0, 1);
    lcd.print(response);  // Display response on LCD
  } else {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Error");
  }
  http.end();
}


void createDispensation(String code){
  //code to control motors and dispenseMedication(prescription.code)
  //Authenticated API call to confirm dispensation after
  delay(1000);
}




//main logic
void processCode(String code) {
  Serial.println("\nProcessing Code: " + code);


  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Code yanu: " + code);

  lcd.setCursor(0, 1);
  lcd.print("Dikilani pangono");

  fetchVendingSlots();
  createDispensation(code);

  // the prescription must have it's is_dispensed flag set to false for it to be available for dispensing

  // API calls will happen here
  // Calls to dispensation functions will happen here too
  // Want to display the name of the medication being dispensed on the LCD as it is being dispensed
  // upon finishing the dispensation, send a request to the server to update the retrieved prescription object's is_dispensed flag to 
  // true, and another request to the dispensations endpoint to log the date and time of the event.

  // Simulate a delay or processing time
  
  delay(5000);  
}


//LCD functions
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

