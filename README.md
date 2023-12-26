# GPS Tracking System Structure

## Components

### Hardware
- ESP32
  - Integrated WiFi module
  - Serial communication for GPS module

### External Modules
- GPS Module

### Libraries
- `TinyGPS++`: For parsing GPS data
- `HardwareSerial`: For serial communication
- `WiFi`: For managing WiFi connections
- `HTTPClient`: For sending HTTP requests

## Configuration
- **GPS Module and ESP32 Serial Communication**
  - `HardwareSerial SerialGPS(1)`
- **WiFi Settings**
  - SSID: `const char* ssid = "yourSSID"`
  - Password: `const char* password = "yourPASSWORD"`
- **Server Address**
  - `const char* serverUrl = "http://yourserver.com/api/location"`

## Initialization
- `TinyGPSPlus gps`: GPS data processing object

## Main Functions

### `setup()`
- Initialize serial communication
- Connect to WiFi

### `loop()`
- Continuously read data from GPS
- Check if location data is valid
- Calculate carbon saved (if location is valid)
- Send data to the server (if location is valid)

## Helper Functions

### `calculateCarbonSaved(float distance)`
- Calculate the carbon saving based on distance

### `sendLocationToServer(float lat, float lng, float carbonSaved)`
- Check WiFi connection
- Send data (latitude, longitude, carbonSaved) to the server in JSON format
- Handle server response

