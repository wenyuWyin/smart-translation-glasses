#include <WiFi.h>
#include <HTTPClient.h>
#include <ESPAsyncWebServer.h>
#include <EEPROM.h>
#include "esp_camera.h"

// CAMERA MODEL AI THINKER PINS
#define PWDN_GPIO_NUM    32
#define RESET_GPIO_NUM   -1
#define XCLK_GPIO_NUM    0
#define SIOD_GPIO_NUM    26
#define SIOC_GPIO_NUM    27
#define Y9_GPIO_NUM      35
#define Y8_GPIO_NUM      34
#define Y7_GPIO_NUM      39
#define Y6_GPIO_NUM      36
#define Y5_GPIO_NUM      21
#define Y4_GPIO_NUM      19
#define Y3_GPIO_NUM      18
#define Y2_GPIO_NUM      5
#define VSYNC_GPIO_NUM   25
#define HREF_GPIO_NUM    23
#define PCLK_GPIO_NUM    22

// AP Mode credentials
const char* ap_ssid = "ESP32_CAM_AP";
const char* ap_password = "12345678";

// Server URL for image upload
const char* serverUrl = "http://192.168.2.15:5000/upload"; // Replace with your server URL

// EEPROM settings
#define EEPROM_SIZE 256
#define SSID_ADDR 0
#define PASS_ADDR 64
#define MAX_CREDENTIAL_LENGTH 64

// Timing variables
unsigned long previousCaptureMillis = 0;
const unsigned long captureInterval = 3000; // Capture every 3 seconds

// Web server instance for AP mode
AsyncWebServer server(80);

// Function to initialize the camera
void setupCamera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer   = LEDC_TIMER_0;
  config.pin_d0       = Y2_GPIO_NUM;
  config.pin_d1       = Y3_GPIO_NUM;
  config.pin_d2       = Y4_GPIO_NUM;
  config.pin_d3       = Y5_GPIO_NUM;
  config.pin_d4       = Y6_GPIO_NUM;
  config.pin_d5       = Y7_GPIO_NUM;
  config.pin_d6       = Y8_GPIO_NUM;
  config.pin_d7       = Y9_GPIO_NUM;
  config.pin_xclk     = XCLK_GPIO_NUM;
  config.pin_pclk     = PCLK_GPIO_NUM;
  config.pin_vsync    = VSYNC_GPIO_NUM;
  config.pin_href     = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn     = PWDN_GPIO_NUM;
  config.pin_reset    = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size   = FRAMESIZE_SXGA;  // Use SXGA for balanced quality and speed
  config.jpeg_quality = 4;              // 0 = best quality, 63 = worst
  config.fb_count     = 1;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed 0x%x\n", err);
    return;
  }

  // Adjust sensor settings
  sensor_t* s = esp_camera_sensor_get();
  if (s) {
    s->set_exposure_ctrl(s, 1);   // Enable auto exposure
    s->set_aec2(s, 1);            // Enable advanced exposure control
    s->set_aec_value(s, 500);     // Reduce exposure time
    s->set_gain_ctrl(s, 1);       // Enable auto gain control
    s->set_agc_gain(s, 15);       // Increase gain
    s->set_brightness(s, 2);      // Adjust brightness (-2 to 2)
    s->set_contrast(s, 2);        // Adjust contrast (-2 to 2)
    s->set_saturation(s, 1);      // Adjust saturation (-2 to 2)
    s->set_whitebal(s, 1);        // Enable auto white balance
    s->set_awb_gain(s, 1);        // Enable AWB gain
    s->set_special_effect(s, 0);  // No effect
  }

  Serial.println("Camera initialized and settings applied!");
}

// Save Wi-Fi credentials to EEPROM
void saveWiFiCredentials(String ssid, String password) {
  Serial.println("Saving Wi-Fi credentials to EEPROM...");
  
  // Save SSID
  for (int i = 0; i < ssid.length(); i++) {
    EEPROM.write(SSID_ADDR + i, ssid[i]);
  }
  EEPROM.write(SSID_ADDR + ssid.length(), '\0'); // Null terminator

  // Save Password
  for (int i = 0; i < password.length(); i++) {
    EEPROM.write(PASS_ADDR + i, password[i]);
  }
  EEPROM.write(PASS_ADDR + password.length(), '\0'); // Null terminator

  // Commit changes
  EEPROM.commit();
  Serial.println("Wi-Fi credentials saved.");
}

// Read Wi-Fi credentials from EEPROM
void readWiFiCredentials(String &ssid, String &password) {
  Serial.println("Reading Wi-Fi credentials from EEPROM...");

  char ssidBuffer[MAX_CREDENTIAL_LENGTH];
  char passBuffer[MAX_CREDENTIAL_LENGTH];

  for (int i = 0; i < MAX_CREDENTIAL_LENGTH; i++) {
    ssidBuffer[i] = EEPROM.read(SSID_ADDR + i);
    if (ssidBuffer[i] == '\0') break;
  }
  ssid = String(ssidBuffer);

  for (int i = 0; i < MAX_CREDENTIAL_LENGTH; i++) {
    passBuffer[i] = EEPROM.read(PASS_ADDR + i);
    if (passBuffer[i] == '\0') break;
  }
  password = String(passBuffer);

  Serial.println("Read Wi-Fi credentials:");
  Serial.println("SSID: " + ssid);
  Serial.println("Password: " + password);
}

// Handle Wi-Fi credentials submission in AP mode
void handleCredentials(AsyncWebServerRequest* request) {
  if (request->hasParam("ssid", true) && request->hasParam("password", true)) {
    String ssid = request->getParam("ssid", true)->value();
    String password = request->getParam("password", true)->value();

    saveWiFiCredentials(ssid, password);

    request->send(200, "text/plain", "Credentials received. Rebooting...");
    delay(2000);
    ESP.restart();
  } else {
    request->send(400, "text/plain", "Missing SSID or Password");
  }
}

// Start in AP mode to receive Wi-Fi credentials
void startAPMode() {
  WiFi.softAP(ap_ssid, ap_password);
  Serial.println("Access Point started");
  Serial.print("AP IP Address: ");
  Serial.println(WiFi.softAPIP());

  server.on("/", HTTP_GET, [](AsyncWebServerRequest* request) {
    request->send(200, "text/html",
                  "<form action='/connect' method='post'>"
                  "SSID: <input type='text' name='ssid'><br>"
                  "Password: <input type='password' name='password'><br>"
                  "<input type='submit' value='Connect'>"
                  "</form>");
  });

  server.on("/connect", HTTP_POST, handleCredentials);
  server.begin();
}

// Connect to Wi-Fi in Station mode
void connectToWiFi() {
  String ssid, password;
  readWiFiCredentials(ssid, password);

  if (ssid.isEmpty() || password.isEmpty()) {
    Serial.println("No Wi-Fi credentials found. Starting AP mode...");
    startAPMode();
    return;
  }

  WiFi.begin(ssid.c_str(), password.c_str());
  Serial.print("Connecting to Wi-Fi...");
  int retries = 20; // Try for 10 seconds (500ms x 20)
  while (WiFi.status() != WL_CONNECTED && retries > 0) {
    delay(500);
    Serial.print(".");
    retries--;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected to Wi-Fi!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
    setupCamera(); // Initialize the camera after connecting to Wi-Fi
  } else {
    Serial.println("\nFailed to connect to Wi-Fi. Restarting AP mode...");
    startAPMode(); // Restart AP mode if connection fails
  }
}

void setup() {
  Serial.begin(115200);
  EEPROM.begin(EEPROM_SIZE); // Initialize EEPROM
  connectToWiFi();
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    unsigned long currentMillis = millis();
    if (currentMillis - previousCaptureMillis >= captureInterval) {
      previousCaptureMillis = currentMillis;
      camera_fb_t* fb = esp_camera_fb_get();
      if (fb) {
        HTTPClient http;
        http.begin(serverUrl);
        http.addHeader("Content-Type", "image/jpeg");
        http.POST(fb->buf, fb->len);
        http.end();
        esp_camera_fb_return(fb);
      }
    }
  }
}
