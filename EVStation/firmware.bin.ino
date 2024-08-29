#include <WiFi.h>
#include <HTTPClient.h>
#include <Update.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

//const char* firmwareUrl = "http://10.154.209.2:8080/firmware.bin";
const char* firmwareUrl = "hhttps://raw.githubusercontent.com/lchokunl01/EGAT/main/EVStation/firmware.bin";

unsigned long previousMillis = 0;
const long interval = 60000;  // ตรวจสอบทุกๆ 60 วินาที

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    checkForUpdates();
  }

  print('hello')
  // ส่วนอื่นๆ ของโปรแกรม
}

void checkForUpdates() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(firmwareUrl);
    int httpCode = http.GET();

    if (httpCode == 200) {
      int contentLength = http.getSize();
      bool canBegin = Update.begin(contentLength);

      if (canBegin) {
        WiFiClient* client = http.getStreamPtr();
        size_t written = Update.writeStream(*client);

        if (written == contentLength) {
          Serial.println("Update Success");
        } else {
          Serial.println("Update Failed");
        }

        if (Update.end()) {
          Serial.println("Update complete");
          if (Update.isFinished()) {
            Serial.println("Update successfully completed. Rebooting...");
            ESP.restart();
          } else {
            Serial.println("Update not finished? Something went wrong!");
          }
        } else {
          Serial.printf("Update failed. Error: %d\n", Update.getError());
        }
      } else {
        Serial.println("Not enough space to begin OTA");
      }
    } else {
      Serial.printf("HTTP GET failed. Error: %d\n", httpCode);
    }

    http.end();
  }
}
