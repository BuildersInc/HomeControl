#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>
#include <Sodaq_SHT2x.h>


// Configuration

const int id = 0b00110001;  //ID: 49 (unique in Network)



// Wifi
const char* ssid     = "Wlan";
const char* password = "hrmp1143";
const char* hostIP = "192.168.99.197";  //Change to static IP
const int udpPort = 1337;

// UDP
WiFiUDP UDP;
char packet[255];


// Pins
const int heartbeatLED = 14;  // D5
const int failureLED = 12;  // D6


// Helper
const int heartbeatPulse = 500;

const bool wifiConnect = true;



void heartbeat() {
  delay(heartbeatPulse);
  digitalWrite(heartbeatLED, LOW);
  delay(heartbeatPulse);
  digitalWrite(heartbeatLED, HIGH);
}


void logError(int code) {
  Serial.println(code);
  digitalWrite(heartbeatLED, LOW);
  switch (code) {
    case 1 :
      Serial.println("No Wifi connection");
      for (int i = 1; i < 3; i++) {
        digitalWrite(failureLED, LOW);
        delay(125);

        digitalWrite(failureLED, HIGH);
        delay(125);
      }
      break;
    }

  logError(code);
}

void buildResult() {
  snprintf(packet, sizeof(packet), "%0.5f;%0.5f;%i", SHT2x.GetHumidity(), SHT2x.GetTemperature(), id);
  packet[sizeof(packet) - 1] = '\0';
}

void setup() {
  // put your setup code here, to run once:
  pinMode(heartbeatLED, OUTPUT);
  pinMode(failureLED, OUTPUT);

  Wire.begin();

  Serial.begin(9600);
  if (wifiConnect) {
    WiFi.begin(ssid, password);

    int i = 0;
    while (WiFi.status() != WL_CONNECTED && i++ < 10)
    {
      heartbeat();
    }


    if (WiFi.status() != WL_CONNECTED && i >= 10) logError(1);
    Serial.println(WiFi.localIP());
  }

}

void loop() {

  buildResult();

  Serial.println(packet);

  if (wifiConnect) {
    if (WiFi.status() != WL_CONNECTED) logError(1);
    UDP.beginPacket(hostIP, udpPort);
    UDP.write(packet);
    UDP.endPacket();
  }

  heartbeat();

}
