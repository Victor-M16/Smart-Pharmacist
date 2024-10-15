#include <Stepper.h>

const int steps_per_rev = 200; // Set to 200 for NEMA 17
const int num_slots = 6; // Number of slots in your setup
const int steps_per_slot = steps_per_rev / num_slots; // Steps needed to move to the next slot

#define IN1 14
#define IN2 27
#define IN3 26
#define IN4 25

Stepper motor(steps_per_rev, IN1, IN2, IN3, IN4);

int current_slot = 0; // Start at slot 0

void setup() {
  motor.setSpeed(30);  // Set a moderate speed for testing
  Serial.begin(115200);
}

void loop() {
  // Move to slot 1
  Serial.println("Rotating to Slot 1...");
  moveToSlot(1); // Move to slot 1
  delay(2000); // Delay to observe

  // Move to slot 2
  Serial.println("Rotating to Slot 2...");
  moveToSlot(2); // Move to slot 2
  delay(2000); // Delay to observe

  // Move to slot 4 (skipping slot 3)
  Serial.println("Rotating to Slot 4...");
  moveToSlot(4); // Move to slot 4
  delay(2000); // Delay to observe

  // Move back to slot 2
  Serial.println("Rotating Back to Slot 2...");
  moveToSlot(2); // Move back to slot 2
  delay(2000); // Delay to observe

  // Move back to slot 1
  Serial.println("Rotating Back to Slot 1...");
  moveToSlot(1); // Move back to slot 1
  delay(2000); // Delay to observe
}

// Function to move the motor to the desired slot
void moveToSlot(int target_slot) {
  int slot_difference = target_slot - current_slot; // Calculate slot difference
  int steps_to_move = slot_difference * steps_per_slot; // Calculate steps needed
  
  motor.step(steps_to_move); // Rotate motor to target slot
  current_slot = target_slot; // Update current slot
  
  // Print the action to the serial monitor for logging
  Serial.println("Moved to slot: " + String(current_slot));
}
