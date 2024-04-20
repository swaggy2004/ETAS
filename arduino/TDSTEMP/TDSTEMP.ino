#include "EEPROM.h"
#include "GravityTDS.h"
#include <OneWire.h>
#include <DallasTemperature.h>
 
#define TdsSensorPin A1
#define ONE_WIRE_BUS 2
GravityTDS gravityTds;
 
float temperature = 0,tdsValue = 0;
OneWire oneWire(ONE_WIRE_BUS);

DallasTemperature sensors(&oneWire);

void setup()
{
    Serial.begin(9600);
    sensors.begin();
    gravityTds.setPin(TdsSensorPin);
    gravityTds.setAref(5.0);  //reference voltage on ADC, default 5.0V on Arduino UNO
    gravityTds.setAdcRange(1024);  //1024 for 10bit ADC;4096 for 12bit ADC
    gravityTds.begin();  //initialization
}
 
void loop()
{
    sensors.requestTemperatures(); 
    Serial.print("Celsius temperature: ");
    temperature = sensors.getTempCByIndex(0);
    Serial.println(temperature);
    //temperature = readTemperature();  //add your temperature sensor and read it
    gravityTds.setTemperature(temperature);  // set the temperature and execute temperature compensation
    gravityTds.update();  //sample and calculate
    tdsValue = gravityTds.getTdsValue();  // then get the value
    Serial.print(tdsValue, 0);
    Serial.println("ppm");
    delay(2000);
}