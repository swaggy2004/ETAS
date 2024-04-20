int en1 = 7;
int pos = 5;
int neg = 6;

void setup() {
  // put your setup code here, to run once:
  pinMode(en1, OUTPUT);
  pinMode(pos, OUTPUT);
  pinMode(neg, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(pos, HIGH);
  digitalWrite(neg, LOW);
  analogWrite(en1, 150);
  delay(3000);
  digitalWrite(pos, HIGH);
  digitalWrite(neg, LOW);
  analogWrite(en1, 200);
  delay(4000);
  digitalWrite(pos, HIGH);
  digitalWrite(neg, LOW);
  analogWrite(en1, 255);
  delay(5000);
  digitalWrite(pos, HIGH);
  digitalWrite(neg, LOW);
  analogWrite(en1, 0);
  delay(1000);
}
