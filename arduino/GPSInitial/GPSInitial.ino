#include "TinyGPSPlus.h"

TinyGPSPlus gps;

void setup()
{
  Serial.begin(9600);
  Serial3.begin(9600);
}

void loop()
{
  if (Serial3.available())
  {
    gps.encode(Serial3.read());
    Serial.print("Latitude: ");
    Serial.print(gps.location.lat(), 6);
    Serial.print("  ");
    Serial.print("Longitude: ");
    Serial.println(gps.location.lng(), 6);
  }
  delay(1);
}