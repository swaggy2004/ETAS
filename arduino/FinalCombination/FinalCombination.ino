#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include "GravityTDS.h"
#include "TinyGPS++.h"
#include <ArduinoJson.h>

const int pHPin = A3;
const int temperaturePin = 2;
const int TdsSensorPin = A1;
const int turbidityPin = A0;
int en1 = 7;
int pos = 5;
int neg = 6;

float pHValue = 0.0;
float temperatureValue = 0.0;
float tdsValue = 0.0;
float turbidityValue = 0.0;
float longitude = 0.0;
float latitude = 0.0;
int motorState = 0;
String statusValue = "";
int sendError = 0;


OneWire oneWire(temperaturePin);
DallasTemperature sensors(&oneWire);
GravityTDS gravityTds;
TinyGPSPlus gps;

void errorSms(String message) {
  Serial2.println("AT"); //Handshaking with SIM900
  delay(1000);
  Serial2.println("AT+CMGF=1"); // Configuring TEXT mode
  delay(2000);
  Serial2.println("AT+CMGS=\"+94703412996\"");//change ZZ with country code and xxxxxxxxxxx with phone number to sms
  delay(2000);
  Serial2.print(message); //text content
  delay(4000);
  Serial2.println((char)26);
  delay(5000);
  Serial2.println();
  delay(10000);
}


void readPH() {
  const unsigned long READ_INTERVAL = 5000; // Interval between pH readings attempts (5 seconds in milliseconds)
  const int MAX_READINGS = 10; // Maximum number of pH readings to collect
  
  float Po;
  float m = -0.0081460;
  pHValue = 7 - (2.5 - Po) * m;
  
  // Check if the pH value is accurate
  if (pHValue < 0 || pHValue > 14) {
    // pH value is not accurate, collect multiple readings
    for (int i = 0; i < MAX_READINGS; ++i) {
      // Wait for a short delay before taking the reading
      delay(5000); // 5 seconds delay
      
      // Take a new pH reading
      Po = analogRead(pHPin) * 5.0 / 1024;
      pHValue = 7 - (2.5 - Po) * m;
      // Check if the pH value is within the valid range
      if (pHValue >= 0 && pHValue <= 14) {
        // Valid pH value obtained, exit the loop
        break;
      }
    }
    
    // Check if the pH value is still inaccurate after multiple readings
    if (pHValue < 0 || pHValue > 14) {
      // pH value is still inaccurate, send error SMS
      String msg = "Hey this is ETAS. The pH value is inaccurate. pH Value: " + String(pHValue) + ". My coordinates: " + String(latitude, 6) + ", " + String(longitude, 6) +". The pH sensor could be damaged.";
      errorSms(msg);
      return;
    }
  }
  
  // Check if the pH value is out of range
  if (pHValue < 6 || pHValue > 8) {
    // pH value is out of range, collect multiple readings
    for (int i = 0; i < MAX_READINGS; ++i) {
      // Wait for a short delay before taking the reading
      delay(5000); // 5 seconds delay
      
      // Take a new pH reading
      Po = analogRead(pHPin) * 5.0 / 1024;
      pHValue = 7 - (2.5 - Po) * m;
      
      // Check if the pH value is within the valid range
      if (pHValue >= 6 && pHValue <= 8) {
        // Valid pH value obtained, exit the loop
        break;
      }
    }
    
    // Check if the pH value is still out of range after multiple readings
    if (pHValue < 6 || pHValue > 8) {
      // pH value is still out of range, send error SMS
      String msg = "Hey this is ETAS. The pH value is out of range. pH Value: " + String(pHValue) + ". My coordinates: " + String(latitude, 6) + ", " + String(longitude, 6) +".";
      errorSms(msg);
      return;
    }
  }
  
  // Valid pH value obtained
  Serial.println("Valid pH value obtained: " + String(pHValue));
}


void readTemperature() {
  const unsigned long READ_INTERVAL = 5000; // Interval between temperature readings attempts (5 seconds in milliseconds)
  const int MAX_READINGS = 3; // Maximum number of temperature readings to collect
  
  // Read temperature sensor
  sensors.requestTemperatures();
  temperatureValue = sensors.getTempCByIndex(0);
  Serial.println(temperatureValue);
  // Check if temperature sensor reading is -127°C (invalid)
  if (temperatureValue == -127.0) {
    // Temperature sensor reading is invalid, collect multiple readings
    for (int i = 0; i < MAX_READINGS; ++i) {
      // Wait for a short delay before taking the reading
      delay(READ_INTERVAL); // 5 seconds delay
      
      // Take a new temperature reading
      sensors.requestTemperatures();
      temperatureValue = sensors.getTempCByIndex(0);
      // Check if the temperature value is valid
      if (temperatureValue != -127.0) {
        // Valid temperature value obtained, exit the loop
        break;
      }
    }
    
    // Check if temperature value is still invalid after multiple readings
    if (temperatureValue == -127.0) {
      // Temperature sensor may be broken, send error SMS
      String msg = "Hey this is ETAS. The temperature sensor could be broken. My coordinates: " + String(latitude, 6) + ", " + String(longitude, 6) +".";
      errorSms(msg);
      return;
    }
  }
  
  // Check if temperature value is out of range (below 25°C or above 50°C)
  if (temperatureValue < 25.0 || temperatureValue > 50.0) {
    // Temperature value is out of range, collect multiple readings
    for (int i = 0; i < MAX_READINGS; ++i) {
      // Wait for a short delay before taking the reading
      delay(READ_INTERVAL); // 5 seconds delay
      
      // Take a new temperature reading
      sensors.requestTemperatures();
      temperatureValue = sensors.getTempCByIndex(0);
      // Check if the temperature value is within the valid range
      if (temperatureValue >= 25.0 && temperatureValue <= 50.0) {
        // Valid temperature value obtained, exit the loop
        break;
      }
    }
    
    // Check if temperature value is still out of range after multiple readings
    if (temperatureValue < 25.0 || temperatureValue > 50.0) {
      // Temperature value is still out of range, send error SMS
      String msg = "Hey this is ETAS. The temperature value is out of range. Temperature: " + String(temperatureValue, 1) + "C. My coordinates: " + String(latitude, 6) + ", " + String(longitude, 6) +".";
      errorSms(msg);
      return;
    }
  }
  
  // Valid temperature value obtained
  Serial.println("Valid temperature value obtained: " + String(temperatureValue) + "°C");
}


void readTDS() {
  gravityTds.setPin(TdsSensorPin);
  gravityTds.setAref(5.0);
  gravityTds.setAdcRange(1024);
  gravityTds.begin();
  temperatureValue = sensors.getTempCByIndex(0);
  gravityTds.setTemperature(temperatureValue);
  gravityTds.update();
  tdsValue = gravityTds.getTdsValue();
  Serial.println(tdsValue);
}

void readTurbidity() {
  float turbidityClearWater = 830;
  float turbidityBlocked = 700;
  int sensorValue = analogRead(turbidityPin);
  turbidityValue = constrain(map(sensorValue, turbidityBlocked, turbidityClearWater, 0, 100), 0, 100);
  Serial.println(turbidityValue);
}

void readGPS() {
  bool gotLocation = false; // Flag to track if a valid location is obtained
  int tries = 0;
  while (tries <= 1000)
  {
    if (Serial3.available())
    {
      Serial.println("Trying to read");
      gps.encode(Serial3.read());

      // Check if the latitude and longitude are not zero
      if (gps.location.lat() != 0.0 && gps.location.lng() != 0.0)
      {
        latitude = gps.location.lat();
        longitude = gps.location.lng();
        // Print the latitude and longitude
        Serial.print("Latitude: ");
        Serial.print(gps.location.lat(), 6);
        Serial.print("  ");
        Serial.print("Longitude: ");
        Serial.println(gps.location.lng(), 6);

        gotLocation = true; // Set the flag to indicate a valid location is obtained
      }
    }
    tries++;
    delay(1);
  }  
  if (gps.location.lat() == 0.0 && gps.location.lng() == 0.0){
    // String msg = "Hey couldn't connect to the GPS coordinates. Going to send dummy values and trying to continue on with the code.";
    // errorSms(msg);
    latitude = 6.931500;
    longitude = 79.848628; 
  }
  delay(8000);
}

void sendPostRequest() {
  Serial.println("Sending data");
  String jsonPayload = "{\"pH\":" + String(pHValue) + 
                    ",\"temperature\":" + String(temperatureValue) + 
                    ",\"tds\":" + String(tdsValue) + 
                    ",\"turbidity\":" + String(turbidityValue) + 
                    ",\"longitude\":" + String(longitude, 6) + 
                    ",\"latitude\":" + String(latitude, 6) + 
                    ",\"motorState\":" + String(motorState) + "}";
  // Check if the module is responsive, expected value OK
  Serial2.println("AT");
  delay(1000);
  
  // Close or turn off network connection in case it was left open, expected value OK
  Serial2.println("AT+CIPSHUT");
  delay(1000);
  
  // Close GPRS context bearer in case it was left open, expected value OK
  Serial2.println("AT+SAPBR=0,1");
  delay(2000);
  
  // Open GPRS context and establish GPRS connection
  Serial2.println("AT+SAPBR=3,1,\"Contype\",\"GPRS\"");
  delay(2000);
  
  // Set the Access Point Name (APN) for the network provider
  Serial2.println("AT+SAPBR=3,1,\"APN\",\"mobitel\"");
  delay(1000);
  
  // Open GPRS context bearer
  Serial2.println("AT+SAPBR=1,1");
  delay(2000);
  
  // Initiate HTTP request
  Serial2.println("AT+HTTPINIT");
  delay(1000);
  
  // Set parameters for HTTP session, HTTP context identifier
  Serial2.println("AT+HTTPPARA=\"CID\",1");
  delay(1000);
  
  // Set the URL to your server endpoint
  Serial2.println("AT+HTTPPARA=\"URL\",\"http://64.227.188.253:80\"");
  delay(1000);
  
  // Set content type as application/json
  Serial2.println("AT+HTTPPARA=\"CONTENT\",\"application/json\"");
  delay(1000);
  
  // Set the length of the payload
  Serial2.println("AT+HTTPDATA=" + String(jsonPayload.length()) + ",20000");
  delay(6000);
  
  // Send the JSON payload
  Serial2.println(jsonPayload);
  delay(16000);
  
  // Send the POST request
  Serial2.println("AT+HTTPACTION=1");
  delay(40000); 
}

void sendGetRequest() {
  Serial.println("Sending get");
  // Check if the module is responsive
  sendCommand("AT");
  // Close or turn off network connection in case it was left open
  sendCommand("AT+CIPSHUT");
  // Close GPRS context bearer in case it was left open
  sendCommand("AT+SAPBR=0,1");
  // Open GPRS context and establish GPRS connection
  sendCommand("AT+SAPBR=3,1,\"Contype\",\"GPRS\"");
  // Set the Access Point Name (APN) for the network provider
  sendCommand("AT+SAPBR=3,1,\"APN\",\"mobitel\"");
  // Open GPRS context bearer
  sendCommand("AT+SAPBR=1,1");
  // Initiate HTTP request
  sendCommand("AT+HTTPINIT");
  // Set parameters for HTTP session, HTTP context identifier
  sendCommand("AT+HTTPPARA=\"CID\",1");
  // Set the URL to your server endpoint
  sendCommand("AT+HTTPPARA=\"URL\",\"http://64.227.188.253:80\"");
  // Initiate the HTTP GET request
  sendCommand("AT+HTTPACTION=0");
  // Wait for the response
  delay(30000); // Adjust delay as needed based on server response time
  // Read the HTTP response
  sendCommand("AT+HTTPREAD");
  delay(2000);
  // Terminate the HTTP service
  sendCommand("AT+HTTPTERM");
  // Close or turn off network connection
  sendCommand("AT+CIPSHUT");
  // Close GPRS context bearer
  sendCommand("AT+SAPBR=0,1");

  Serial.print("Status Value: ");
  Serial.println(statusValue);
  Serial.println(sendError);
  if (statusValue == "Error" && sendError <= 5){
    ++sendError;
    sendPostRequest();
    sendGetRequest();
  }
  else if (sendError > 2){
    String msg = "Hey this is ETAS, I detected that the data I'm sending isn't properly sent to the server. These are my coordinates: " + String(latitude, 6) + ", " + String(longitude, 6) +".";
    errorSms(msg);
    sendError = 0; // Reset sendError
  }
  else {
    sendError = 0; // Reset sendError if statusValue is not "Error"
  }
  Serial.println("Motor State: ");
  Serial.println(motorState);
}

void sendCommand(const char* command) {
  Serial2.println(command);
  ShowSerialData();
}

void ShowSerialData() {
  Serial.println("Response from Serial2:");
  String response = "";
  char c;
  
  // Read the response until a complete response is received or a timeout occurs
  unsigned long startTime = millis(); // Record the start time
  while (millis() - startTime < 5000) { 
    if (Serial2.available()) { 
      c = Serial2.read(); 
      response += c; 
      if (c == '}') { 
        break; 
      }
    }
  }

  // Print the complete response
  Serial.println(response);

  // Parse the response to extract status value and motor state
  parseStatusValue(response);
  parseMotorState(response);
}


void parseStatusValue(String response) {
  // Check if the response contains the status key
  int statusIndex = response.indexOf("\"status\"");
  if (statusIndex != -1) {
    // Extract the value of the status key
    int colonIndex = response.indexOf(':', statusIndex);
    int startQuoteIndex = response.indexOf('"', colonIndex); // Find the opening quote
    int endQuoteIndex = response.indexOf('"', startQuoteIndex + 1); // Find the closing quote
    statusValue = response.substring(startQuoteIndex + 1, endQuoteIndex);
  }
}
void parseMotorState(String response) {
  // Check if the response contains the motorState key
  int motorStateIndex = response.indexOf("\"motorState\"");
  if (motorStateIndex != -1) {
    // Extract the value of the motorState key
    int colonIndex = response.indexOf(':', motorStateIndex);
    int startQuoteIndex = response.indexOf('"', colonIndex); // Find the opening quote
    int endQuoteIndex = response.indexOf('"', startQuoteIndex + 1); // Find the closing quote
    String ms = response.substring(startQuoteIndex + 1, endQuoteIndex);

    // Convert the motorState string to an integer
    if (ms == "ON") {
      motorState = 1;
    } 
    else {
      motorState = 0;
    }
  }
}


void motorStart(){
  if (motorState == 0){
    digitalWrite(pos, HIGH);
    digitalWrite(neg, LOW);
    analogWrite(en1, 200);
  }
  else{
    digitalWrite(pos, HIGH);
    digitalWrite(neg, LOW);
    analogWrite(en1, 255);
  }
}

void motorStop(){
  digitalWrite(pos, LOW);
  digitalWrite(neg, LOW);
  analogWrite(en1, 0);
}

void setup() {
  Serial.begin(9600); // For serial monitor
  Serial2.begin(19200); // For Serial2 module
  Serial3.begin(9600);
  pinMode(en1, OUTPUT);
  pinMode(pos, OUTPUT);
  pinMode(neg, OUTPUT);
  sensors.begin();
  delay(10000); 
}

void loop() {
  motorStop();
  Serial.println(motorState);
  delay(2000); 
  Serial.println("Reading GPS");
  readGPS();
  readPH();
  readTemperature();
  readTDS();
  readTurbidity();
  sendPostRequest();
  sendGetRequest();
  motorStart();
  delay(60000);
}
