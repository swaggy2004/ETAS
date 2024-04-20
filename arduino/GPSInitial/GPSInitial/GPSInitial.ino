void setup() {
  Serial.begin(9600);
  Serial3.begin(19200);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');  // Read data from Serial until newline
    Serial3.println(data);                       // Send data to Serial3
  }

  if (Serial3.available()) {
    String data = Serial3.readStringUntil('\n');  // Read data from Serial3 until newline
    Serial.println(data);                         // Send data to Serial
  }
}