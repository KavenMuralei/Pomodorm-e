#include <Servo.h>
#include <AFMotor.h> // Requires "Adafruit Motor Shield library"

// --- CONFIGURATION ---
// On the L293D shield, "SERVO_1" is connected to Pin 10
#define SERVO_PIN 10 

Servo myServo;

// Initialize only Motor 1
AF_DCMotor motor1(1); 

void setup() {
  Serial.begin(9600);
  Serial.println("--- DIAGNOSTIC TEST START ---");

  // 1. Attach Servo
  myServo.attach(SERVO_PIN);
  Serial.println("Servo Attached on Pin 10");

  // 2. Setup Motor
  motor1.setSpeed(200); // Speed range: 0 to 255
  motor1.run(RELEASE);  // Ensure it's stopped initially
  Serial.println("Motor 1 Initialized");

  delay(2000); // Wait 2 seconds before starting
}

void loop() {
  // --- TEST SERVO ---
  Serial.println("Servo: Moving to 90 degrees");
  myServo.write(90);
  delay(1000);

  Serial.println("Servo: Moving to 180 degrees");
  myServo.write(110);
  delay(1000);

  // --- TEST MOTOR 1 ---
  Serial.println("Motor 1: Forward");
  motor1.run(FORWARD);
  delay(2000); // Run for 2 seconds

  Serial.println("Motor 1: Stop");
  motor1.run(RELEASE);
  delay(1000);

  Serial.println("Motor 1: Backward");
  motor1.run(BACKWARD);
  delay(2000); // Run for 2 seconds

  Serial.println("Motor 1: Stop");
  motor1.run(RELEASE);
  delay(1000);

  Serial.println("--- LOOP COMPLETE (Repeating) ---");
}
