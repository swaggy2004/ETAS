#include <Arduino.h>
const int adcPin = A3;

// This can change depending on the volatage I get again. 
/*
  m = x2 - x1 / y2 - y1;
*/
const float m = -0.0081460; 

void setup()
{
   Serial.begin(9600);
}

void loop() 
{
   float Po = analogRead(adcPin) * 5.0 / 1024;
   float phValue = 7 - (2.5 - Po) * m;
   Serial.print("p h value = "); 
   Serial.println(phValue);
   delay(100);
}