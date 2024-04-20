#include <Arduino.h>
const int adcPin = A7;
 
void setup() 
{
    Serial.begin(9600);
}
 
void loop() 
{
   int adcValue = analogRead(adcPin);
   float phVoltage = (float)adcValue * 5.0 / 1024;
   Serial.print("ADC = "); 
   Serial.print(adcValue);
   Serial.print("  Po  = "); 
   Serial.println(phVoltage, 3);
   delay(1000);
}