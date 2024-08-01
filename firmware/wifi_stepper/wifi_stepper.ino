#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <ArduinoJson.h>
#include <ESP32Servo.h>
#include <AccelStepper.h>


//Victor's laptop on Asgard16 network: 192.168.8.168
//ESP32 on Asgard16 network: 192.168.8.124
const char* ssid = "Asgard16";
const char* password = "14MTH0R16";

const int serverPort = 80; //the port on which the server is running to receive requests from the django server
const int servoPin = 11; // put the gpio pin number the servo is attached to

const int LOCK_ANGLE = 180;
const int UNLOCK_ANGLE = 70;

Servo servo;
int lockStatus = 0; // Initial lock status (0 for unlocked, 1 for locked)

const int stepsPerRevolution = 2048; // Number of steps per revolution for 28BYJ-48

// Stepper motor configuration
AccelStepper stepper(AccelStepper::FULL4WIRE, 15, 14, 13, 12); 

// Positions corresponding to slots (in steps)
const int slotPositions[6] = {0, 341, 682, 1023, 1364, 1705}; 

AsyncWebServer server(serverPort);

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

  // Route setup
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "Hello from ESP32!");
  });

  server.on("/lock-status", HTTP_GET, [](AsyncWebServerRequest *request){ //this is the request handler that returns whether the gate is locked
    DynamicJsonDocument doc(100);
    doc["status"] = lockStatus;
    String jsonStr;
    serializeJson(doc, jsonStr);
    request->send(200, "application/json", jsonStr);
  });

  server.on("/lock", HTTP_POST, [](AsyncWebServerRequest *request){ //this handler locks the vending machine
    lockStatus = 1;
    Serial.println("Lock command received. Locking door...");
    servo.write(LOCK_ANGLE);
    request->send(200);
    Serial.println("Locked successfully.");
  });

  server.on("/unlock", HTTP_POST, [](AsyncWebServerRequest *request){ // this handler unlocks the vending machine
    lockStatus = 0;
    Serial.println("Unlock command received. Unlocking door...");
    servo.write(UNLOCK_ANGLE);
    request->send(200);
    Serial.println("Access granted.");
  });


  // Initialize stepper motor
  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(500);



  //JSON must look like this: 
  //{
  // "positions": [0, 2, 4]
  //}
  // Route to handle JSON input
  server.on("/rotate", HTTP_POST, [](AsyncWebServerRequest *request){
    String body;
    if (request->hasParam("body", true)) {
      body = request->getParam("body", true)->value();
    }

    DynamicJsonDocument doc(1024);
    deserializeJson(doc, body);

    JsonArray positions = doc["positions"].as<JsonArray>();

    for (int position : positions) {
      if (position >= 0 && position < 6) { // Validate the position
        servo.write(LOCK_ANGLE);
        Serial.print("Rotating to slot: ");
        Serial.println(position);
        stepper.moveTo(slotPositions[position]);
        stepper.runToPosition(); // Blocking call to move stepper to position
        servo.write(UNLOCK_ANGLE);
        delay(5000);
      } else {
        Serial.println("Invalid slot position received.");
      }
    }

    request->send(200, "application/json", "{\"message\":\"Rotation complete\"}");
  });

  server.begin();
}

void loop(){
  //empty 
}



