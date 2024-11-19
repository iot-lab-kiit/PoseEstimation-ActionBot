#include <Servo.h> // Include the Servo library

Servo myServo; // Create a Servo object

void setup() {
  // Initialize Serial communication at 9600 baud rate
  Serial.begin(9600);
  Serial.println("Waiting for data...");
  
  // Attach the servo to pin 9
  myServo.attach(11);
  
  // Set servo to the initial position
  myServo.write(0);
}

void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    // Read the incoming data
    String receivedData = Serial.readString(); // Read as a string
    receivedData.trim(); // Remove any leading/trailing whitespace
    Serial.print("Received: ");
    Serial.println(receivedData); // Print the received data
    
    // Convert the string to an integer
    int inputData = receivedData.toInt();
    
    // Check if the input is a valid number
    if (inputData >= 0 && inputData <= 255) {
      // Map the input value (0-255) to servo angle (0-180)
      int servoAngle = map(inputData, 0, 255, 0, 180);
      
      // Move the servo to the mapped angle
      myServo.write(servoAngle);
      Serial.print("Servo Angle: ");
      Serial.println(servoAngle); // Print the servo angle
    } else {
      Serial.println("Invalid data! Please send a number between 0 and 255.");
    }
  }
}
