#include <Servo.h>

Servo myservo;  // create Servo object to control a servo

void setup() {
  myservo.attach(9);           // attaches the servo on pin 9 to the Servo object
  pinMode(LED_BUILTIN, OUTPUT); // set the built-in LED pin as output
  Serial.begin(9600);          // initialize serial communication
}

void loop() {
  // Check if any data is available on the Serial port
  if (Serial.available()) {
    int value = Serial.parseInt(); // Read the integer value from Serial
    if (value >= 0 && value <= 180) { // Ensure value is within servo range
      myservo.write(value);          // Move servo to specified position
      //Serial.print("Servo position set to: ");
      //Serial.println(value);         // Provide feedback
      digitalWrite(LED_BUILTIN, HIGH); // Turn on the LED
    } else {
      //Serial.println("Invalid position! Enter a value between 0 and 180.");
    }
  } else {
    digitalWrite(LED_BUILTIN, LOW); // Turn off the LED if no data
  }
}
