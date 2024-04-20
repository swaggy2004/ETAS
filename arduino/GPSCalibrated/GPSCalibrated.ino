#include "TinyGPSPlus.h"

TinyGPSPlus gps;

void setup()
{
  Serial.begin(9600);
  Serial3.begin(9600);
}

void loop()
{
  getLocation();
  delay(1000); // Delay for 1 minute
}

void getLocation()
{
  bool gotLocation = false; // Flag to track if a valid location is obtained
  while (!gotLocation)
  {
    if (Serial3.available())
    {
      gps.encode(Serial3.read());

      // Check if the latitude and longitude are not zero
      if (gps.location.lat() != 0.0 && gps.location.lng() != 0.0)
      {
        // Print the latitude and longitude
        Serial.print("Latitude: ");
        Serial.print(gps.location.lat(), 6);
        Serial.print("  ");
        Serial.print("Longitude: ");
        Serial.println(gps.location.lng(), 6);

        gotLocation = true; // Set the flag to indicate a valid location is obtained
      }
    }
    delay(1); // Delay for 1 millisecond
  }
}