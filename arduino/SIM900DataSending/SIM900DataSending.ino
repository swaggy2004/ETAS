void testPostRequest() {
    float pH = 7.2;
    float temperature = 25.5;
    float tds = 150.0;
    float turbidity = 10.5;
    float longitude = 80.2456; // Replace with your desired longitude value
    float latitude = 13.0827; // Replace with your desired latitude value

    // Create JSON payload
    String jsonPayload = "{\"pH\":" + String(pH) + ",\"temperature\":" + String(temperature) + ",\"tds\":" + String(tds) + ",\"turbidity\":" + String(turbidity) + ",\"longitude\":" + String(longitude) + ",\"latitude\":" + String(latitude) + "}";

    sendCommand("AT");
    ShowSerialData();

    sendCommand("AT+CIPSHUT");
    ShowSerialData();

    delay(500);

    sendCommand("AT+SAPBR=0,1");
    delay(2000);
    ShowSerialData();

    sendCommand("AT+SAPBR=3,1,\"Contype\",\"GPRS\"");
    ShowSerialData();

    sendCommand("AT+SAPBR=3,1,\"APN\",\"mobitel\"");
    ShowSerialData();

    sendCommand("AT+SAPBR=1,1");
    delay(2000);
    ShowSerialData();

    sendCommand("AT+HTTPINIT");
    delay(1000);
    ShowSerialData();

    sendCommand("AT+HTTPPARA=\"CID\",1");
    ShowSerialData();

    sendCommand("AT+HTTPPARA=\"URL\",\"http://64.227.188.253:80/\"");
    ShowSerialData();

    sendCommand("AT+HTTPPARA=\"CONTENT\",\"application/json\"");
    ShowSerialData();

    sendCommand(("AT+HTTPDATA=" + String(jsonPayload.length()) + ",20000").c_str());
    delay(2000);
    Serial2.println(jsonPayload);
    delay(2000);
    ShowSerialData();

    sendCommand("AT+HTTPACTION=1");
    delay(2000);
    ShowSerialData();

    sendCommand("AT+HTTPREAD");
    ShowSerialData();

    sendCommand("AT+HTTPTERM");
    ShowSerialData();

    sendCommand("AT+CIPSHUT");
    ShowSerialData();
}

void sendCommand(const char* command) {
    Serial.print("C: ");
    Serial.println(command);
    Serial2.println(command);
    delay(1000);
}

String ShowSerialData() {
    String response = "";
    while (Serial2.available()) {
        response = Serial2.readString();
        Serial.println("Res from Serial2:");
        Serial.println(response);
    }
    return response;
}

void setup() {
    int baudRate = 9600;
    Serial.begin(baudRate); // Serial monitor
    Serial2.begin(19200); // GSM module

    // Give some time for the SIM card to register on the network
    delay(7000);

    testPostRequest();
}

void loop() {
    // Your code here, if needed
    testPostRequest();
    delay(20000);
}