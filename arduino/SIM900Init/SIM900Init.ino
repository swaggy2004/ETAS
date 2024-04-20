void setup() {
  // Open the serial communication
  Serial3.begin(19200);
}

void loop() {
  Serial3.println("AT+CSCLK=0");
  Serial3.println("AT+CSCLK=?");
  Serial.println(Serial3.readStringUntil('\n'));
}

