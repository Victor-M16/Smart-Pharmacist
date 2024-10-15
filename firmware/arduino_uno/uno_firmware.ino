#include <Arduino.h>
#include <Stepper.h>

// Number of steps per output rotation
const int steps_per_rev = 200; // Number of steps for a full revolution (depends on your stepper motor)
const int steps_per_slot = steps_per_rev / 6; // Steps per 60-degree rotation

// Create Instance of Stepper library
Stepper myStepper(steps_per_rev, 8, 9, 10, 11);

int currentSlot = 6;
void setup() {

    // Set the speed at 20 rpm:
    myStepper.setSpeed(20);
    // Initialize the serial port:
    Serial.begin(9600);

    if (Serial.available()) {
      String dataFromESP = Serial.readStringUntil('\n');
      Serial.println("Booting Data received from ESP32: " + dataFromESP); // Output received data

      currentSlot = parseSlot(dataFromESP); // Initialize the current slot from the server
    }
    Serial.println("Setup complete");
}

void loop() {
    // Check if data is available from ESP32
    if (Serial.available()) {
        String dataFromESP = Serial.readStringUntil('\n');
        Serial.println("Data received from ESP32: " + dataFromESP); // Output received data

        // Parse the received string into an integer
        int targetSlot = parseSlot(dataFromESP);
        
        // Rotate the motor to the specified slot
        rotateMotorToSlot(targetSlot);

        delay(2000); // Delay to allow collection 
    }
}

// Function to parse the received string into an integer
int parseSlot(const String& data) {
    // Convert the received string to an integer
    return data.toInt(); // Return parsed integer
}

// Function to rotate the motor to the target slot
void rotateMotorToSlot(int targetSlot) {
    // Ensure the targetSlot is valid (0 to 5 for 6 slots)
    if (targetSlot < 1 || targetSlot >= 7) {
        Serial.println("Invalid slot number. Must be between 1 and 6.");
        return;
    }

    if (targetSlot == currentSlot) {
        // If the target slot is the same as the current slot, no need to move
        Serial.println("Motor is already at the target slot.");
        return;
    }

    // Calculate the shortest direction to rotate
    int slotDifference = targetSlot - currentSlot;
    
    // If the difference is negative, the motor needs to rotate backward
    if (slotDifference < 0) {
        slotDifference += 6;  // Adjust for circular behavior (6 slots)
    }

    // Check if rotating forward or backward is shorter
    int stepsForward = slotDifference * steps_per_slot;
    int stepsBackward = (6 - slotDifference) * steps_per_slot;

    if (stepsForward <= stepsBackward) {
        // Rotate forward
        myStepper.step(stepsForward);
        Serial.println("Rotating forward by " + String(stepsForward) + " steps to slot " + String(targetSlot));
    } else {
        // Rotate backward
        myStepper.step(-stepsBackward);
        Serial.println("Rotating backward by " + String(stepsBackward) + " steps to slot " + String(targetSlot));
    }

    // Update the current slot
    currentSlot = targetSlot;

    // Send the current slot back to the ESP32
    Serial.println("Current slot: " + String(currentSlot));
    delay(1000); // Optional delay after sending the current slot
}
