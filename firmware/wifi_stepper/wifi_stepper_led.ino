#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <ArduinoJson.h>
#include <ESP32Servo.h>
#include <AccelStepper.h>
#include <queue>

// WiFi credentials
const char* ssid = "Asgard16";
const char* password = "14MTH0R16";

const int serverPort = 80; // the port on which the server is running to receive requests from the Django server
const int servoPin = 11; // GPIO pin number the servo is attached to

const int LOCK_ANGLE = 180;
const int UNLOCK_ANGLE = 70;

Servo servo;
int lockStatus = 0; // Initial lock status (0 for unlocked, 1 for locked)

const int stepsPerRevolution = 2048; // Number of steps per revolution for 28BYJ-48

// Stepper motor configuration
AccelStepper stepper(AccelStepper::FULL4WIRE, 19, 18, 5, 17); 

// Positions corresponding to slots (in steps)
const int slotPositions[6] = {0, 341, 682, 1023, 1364, 1705}; 

// LED pin
const int ledPin = 4; // You can choose any available GPIO pin

AsyncWebServer server(serverPort);

// Queue to hold rotation requests
std::queue<int> rotationQueue;
bool isProcessing = false;

void setup() {
  Serial.begin(115200);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Initialize servo
  servo.setPeriodHertz(50);  // Standard 50 Hz servo
  servo.attach(servoPin, 1000, 2000); // min/max pulse width

  // Initialize LED
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW); // Ensure LED is off initially

  // Route setup
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "Hello from ESP32!");
  });

  server.on("/lock-status", HTTP_GET, [](AsyncWebServerRequest *request){
    DynamicJsonDocument doc(100);
    doc["status"] = lockStatus;
    String jsonStr;
    serializeJson(doc, jsonStr);
    request->send(200, "application/json", jsonStr);
  });

  server.on("/lock", HTTP_POST, [](AsyncWebServerRequest *request){
    lockStatus = 1;
    Serial.println("Lock command received. Locking door...");
    servo.write(LOCK_ANGLE);
    request->send(200);
    Serial.println("Locked successfully.");
  });

  server.on("/unlock", HTTP_POST, [](AsyncWebServerRequest *request){
    lockStatus = 0;
    Serial.println("Unlock command received. Unlocking door...");
    servo.write(UNLOCK_ANGLE);
    request->send(200);
    Serial.println("Access granted.");
  });

  // Initialize stepper motor
  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(500);

  // Endpoints for each slot
  server.on("/rotate-slot-0", HTTP_POST, [](AsyncWebServerRequest *request){
    addRotationToQueue(0);
    request->send(200, "application/json", "{\"message\":\"Request to rotate to slot 0 added to queue\"}");
  });

  server.on("/rotate-slot-1", HTTP_POST, [](AsyncWebServerRequest *request){
    addRotationToQueue(1);
    request->send(200, "application/json", "{\"message\":\"Request to rotate to slot 1 added to queue\"}");
  });

  server.on("/rotate-slot-2", HTTP_POST, [](AsyncWebServerRequest *request){
    addRotationToQueue(2);
    request->send(200, "application/json", "{\"message\":\"Request to rotate to slot 2 added to queue\"}");
  });

  server.on("/rotate-slot-3", HTTP_POST, [](AsyncWebServerRequest *request){
    addRotationToQueue(3);
    request->send(200, "application/json", "{\"message\":\"Request to rotate to slot 3 added to queue\"}");
  });

  server.on("/rotate-slot-4", HTTP_POST, [](AsyncWebServerRequest *request){
    addRotationToQueue(4);
    request->send(200, "application/json", "{\"message\":\"Request to rotate to slot 4 added to queue\"}");
  });

  server.on("/rotate-slot-5", HTTP_POST, [](AsyncWebServerRequest *request){
    addRotationToQueue(5);
    request->send(200, "application/json", "{\"message\":\"Request to rotate to slot 5 added to queue\"}");
  });

  server.begin();
}

void loop(){
  // Check if there is a rotation request being processed
  if (!isProcessing && !rotationQueue.empty()) {
    int slot = rotationQueue.front();
    rotationQueue.pop();
    isProcessing = true;
    handleRotation(slot);
    isProcessing = false;
  }
}

// Function to add a rotation request to the queue
void addRotationToQueue(int slot) {
  if (slot >= 0 && slot < 6) {
    rotationQueue.push(slot);
  } else {
    Serial.println("Invalid slot position received.");
  }
}

// Function to handle rotation to a specific slot
void handleRotation(int slot) {
  // Turn on the LED
  digitalWrite(ledPin, HIGH);

  servo.write(LOCK_ANGLE);
  Serial.print("Rotating to slot: ");
  Serial.println(slot);
  stepper.moveTo(slotPositions[slot]);
  stepper.runToPosition(); // Blocking call to move stepper to position

  // Turn off the LED after rotation is complete
  digitalWrite(ledPin, LOW);
  Serial.println("Rotation Complete");
  servo.write(UNLOCK_ANGLE);
  delay(5000); // Wait for 5 seconds before processing the next request
}
