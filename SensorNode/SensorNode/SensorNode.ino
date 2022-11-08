#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>
#include <Sodaq_SHT2x.h>



// Wifi
const char* ssid     = "Wlan";
const char* password = "hrmp1143";
const char* hostIP = "192.168.63.197";
const int udpPort = 1337;

// UDP
WiFiUDP UDP;
char packet[255];
char reply[255];


// Pins
const int heartbeatLED = 14;  // D5
const int failureLED = 12;  // D6

const int trigPin = 2;  // D4
const int echoPin = 4;  // D3

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
  snprintf(reply, sizeof(reply), "%0.5f;%0.5f", SHT2x.GetHumidity(), SHT2x.GetTemperature());
  reply[sizeof(reply) - 1] = '\0';
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

  Serial.println(reply);

  if (wifiConnect) {
    if (WiFi.status() != WL_CONNECTED) logError(1);
    UDP.beginPacket(hostIP, udpPort);
    UDP.write(reply);
    UDP.endPacket();
  }
  
  heartbeat();

}
