const int fd = 6;
const int bd = 7;
int speed = 135;

void setup() {
  // put your setup code here, to run once:
  pinMode(fd, OUTPUT);
  pinMode(bd, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  listner();
  delay(10);
}

void pumpControl(){
  analogWrite(fd, speed);
  analogWrite(bd, LOW);
}

void listner() {
  while (Serial.available()) {
    char incomingByte = Serial.read();

    if (incomingByte == '1') {
      Serial.println(incomingByte);
      speed = 255;
    } else if (incomingByte == '0') {
      Serial.println(incomingByte);
      speed = 100;
    }
  }
  pumpControl();
}