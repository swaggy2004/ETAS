#define sensor_pin A0

float voltage_min = 0.5; // Voltage when fully clear (adjust this value)
float voltage_max = 3.5; // Voltage when fully obstructed (adjust this value)

void setup() {
  Serial.begin(9600);
}

void loop() {
  int sensorValue = analogRead(sensor_pin);
  float turbidity_clear_water = 830;
  float turbidity_blocked = 700;
  // Constrain the clarity percentage between 0 and 100
  float clarity_percentage = constrain(map(sensorValue, turbidity_blocked, turbidity_clear_water, 0, 100), 0, 100);

  Serial.print("Clarity: ");
  Serial.print(clarity_percentage, 1);
  Serial.println("%");

  delay(200);
}