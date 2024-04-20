const int fd = 6;
const int bd = 7;

void setup() {
  // put your setup code here, to run once:
  pinMode(fd, OUTPUT);
  pinMode(bd, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  analogWrite(fd, LOW);
  analogWrite(bd, LOW);
  delay(5000);
  analogWrite(fd, 180);
  analogWrite(bd, LOW);
  delay(5000);
  analogWrite(fd, 200);
  analogWrite(bd, LOW);
  delay(5000);
  analogWrite(fd, 300);
  analogWrite(bd, LOW);
  delay(5000);
}

