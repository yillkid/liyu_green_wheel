#include <TinyGPS++.h>
#include <HardwareSerial.h>
#include <WiFi.h>
#include <HTTPClient.h>

// GPS模組和ESP32的串口設定
HardwareSerial SerialGPS(1);

// Wi-Fi設定
const char* ssid = "yourSSID";
const char* password = "yourPASSWORD";

// 伺服器地址
const char* serverUrl = "http://yourserver.com/api/location";

// 初始化TinyGPS++物件
TinyGPSPlus gps;

void setup() {
  // 開始串口通信
  Serial.begin(115200);
  SerialGPS.begin(9600, SERIAL_8N1, 16, 17);

  // 連接Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  // 持續讀取GPS數據
  while (SerialGPS.available() > 0) {
    if (gps.encode(SerialGPS.read())) {
      if (gps.location.isValid()) {
        // 獲取緯度和經度
        float latitude = gps.location.lat();
        float longitude = gps.location.lng();

        // 計算碳排放減少量（示例計算，需根據實際情況調整）
        float carbonSaved = calculateCarbonSaved(gps.distanceBetween(startLat, startLon, latitude, longitude));

        // 發送數據到伺服器
        sendLocationToServer(latitude, longitude, carbonSaved);
      }
    }
  }
}

float calculateCarbonSaved(float distance) {
  // 根據距離計算節省的碳排放量（示例值）
  return distance * 0.21; // 假設每公里節省0.21公斤的CO2
}

void sendLocationToServer(float lat, float lng, float carbonSaved) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // 創建JSON數據
    String jsonPayload = "{\"latitude\":" + String(lat, 6) + ",\"longitude\":" + String(lng, 6) + ",\"carbonSaved\":" + String(carbonSaved) + "}";

    // 發送POST請求
    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Server Response: " + response);
    } else {
      Serial.println("Error in sending POST: " + String(httpResponseCode));
    }

    http.end();
  }
}
