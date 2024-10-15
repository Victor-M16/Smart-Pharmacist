#include <WiFi.h>
#include <WiFiClientSecure.h>

// Replace with your WiFi credentials
const char* ssid = "";
const char* password = "";

// The API endpoint and host details
const char* host = "smart-pharmacist-production.up.railway.app";
const int httpsPort = 443; // Standard HTTPS port

// API endpoint to get JWT 
const char* apiEndpoint = "/api/token/";

// JSON payload
const char* jsonPayload = "{\"username\":\"***\",\"password\":\"***\"}";

// Root certificate (optional, but recommended for SSL/TLS)
const char* rootCACertificate = R"literal(
-----BEGIN CERTIFICATE-----
...
-----END CERTIFICATE-----
)literal";


void setup() {
  Serial.begin(115200);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");

  // Set up a secure client
  WiFiClientSecure client;
  client.setCACert(rootCACertificate);  // Optional: Set root CA certificate for SSL
  //client.setInsecure(); //use this if you want to bypass certificate validation, but it is less secure to MITM attacks despite still being encrypted

  Serial.print("Connecting to host: ");
  Serial.println(host);
  
  // Connect to the server
  if (!client.connect(host, httpsPort)) {
    Serial.println("Connection failed!");
    return;
  }
  
  // Create HTTP POST request
  String postRequest = String("POST ") + apiEndpoint + " HTTP/1.1\r\n" +
                       "Host: " + host + "\r\n" +
                       "Content-Type: application/json\r\n" +
                       "Content-Length: " + String(strlen(jsonPayload)) + "\r\n" +
                       "Connection: close\r\n\r\n" +
                       String(jsonPayload);
  
  // Send the request
  client.print(postRequest);
  
  // Wait for the server to respond
  while (client.connected()) {
    String line = client.readStringUntil('\n');
    if (line == "\r") {
      break;  // Headers received
    }
  }
  
  // Read the response
  String response = client.readString();
  Serial.println("Response:");
  Serial.println(response);
  
  client.stop();  // Close the connection
}

void loop() {
  // Keep the program running
}
