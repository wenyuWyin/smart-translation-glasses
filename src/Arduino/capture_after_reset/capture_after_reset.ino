#include <WiFi.h>
#include <HTTPClient.h>
#include <ESPAsyncWebServer.h>
#include <EEPROM.h>
#include "esp_camera.h"
#include <AsyncTCP.h>  // Required for ESP32 AsyncWebServer

extern "C" {
  uint8_t temprature_sens_read(); // Internal sensor reading (undocumented)
}

// ----------------------------------------------------
// 1. Config Constants
// ----------------------------------------------------
const char* ap_ssid = "ESP32_CAM_AP";
const char* ap_password = "12345678";

// Change these URLs or endpoints to match your server
// const char* serverUrl = "http://192.168.2.15:5000/upload/image";
// const char* statusUrl = "http://192.168.2.15:5000/upload/status";
// const char* heartbeatUrl = "http://192.168.2.15:5000/upload/heartbeat";

const char* serverUrl = "http://192.168.2.13:5000/upload/image";
const char* statusUrl = "http://192.168.2.13:5000/upload/status";
const char* heartbeatUrl = "http://192.168.2.13:5000/upload/heartbeat";
#define EEPROM_SIZE 512
#define SSID_ADDR 0
#define PASS_ADDR 64
#define ACCOUNT_ADDR 128
#define MAX_CREDENTIAL_LENGTH 64

unsigned long captureInterval = 3000;
unsigned long lastCaptureMillis = 0;

bool attemptConnectionFlag = false;
bool connectingInProgress = false;
bool invalidCredentials = false;
bool invalidCredentialsMessagePrinted = false;
bool apModeStarted = false;
bool uploadFailurePrinted = false; 
bool wifiConnected = false;


String pendingSsid = "";
String pendingPass = "";
String pendingAccount = "";
String storedSsid = "";
String storedPassword = "";
String storedAccount = "";

String wifiStatusMessage = "";  
unsigned long connectStartTime = 0;
bool previousWifiStatus = false; // Track previous Wi-Fi status

unsigned long lastStatusMillis = 0;   // Timer for status updates
unsigned long lastHeartbeatMillis = 0;  // Timer for heartbeats
const unsigned long statusInterval = 1000;  // Interval for status updates 
const unsigned long heartbeatInterval = 5000;  // Interval for heartbeat 

// Instead of using WebSockets, we'll still use AsyncWebServer for Wi-Fi config
AsyncWebServer server(80);

// ----------------------------------------------------
// 2. Camera Pin Configuration
// ----------------------------------------------------
#define PWDN_GPIO_NUM 32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27
#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22

// ----------------------------------------------------
// 3. Initialize Camera
// ----------------------------------------------------
void setupCamera() {
    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sscb_sda = SIOD_GPIO_NUM;
    config.pin_sscb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;
    config.frame_size = FRAMESIZE_SXGA;
    config.jpeg_quality = 4;
    config.fb_count = 1;

    if (esp_camera_init(&config) != ESP_OK) {
        Serial.println("Camera initialization failed!");
        return;
    }

    sensor_t* s = esp_camera_sensor_get();
    if (s) {
        s->set_exposure_ctrl(s, 1);
        s->set_aec2(s, 1);
        s->set_aec_value(s, 500);
        s->set_gain_ctrl(s, 1);
        s->set_agc_gain(s, 15);
        s->set_brightness(s, 2);
        s->set_contrast(s, 2);
        s->set_saturation(s, 1);
        s->set_whitebal(s, 1);
        s->set_awb_gain(s, 1);
        s->set_special_effect(s, 0);
        s->set_ae_level(s, -2);
        Serial.println("Camera initialized successfully!");
    }
    // Serial.println("Camera initialized successfully!");
    for (int i = 0; i < 5; i++) {
        camera_fb_t *tmp = esp_camera_fb_get();
        if (tmp) {
            esp_camera_fb_return(tmp);
        }
        delay(100); // brief pause between frames
    }
}

// ----------------------------------------------------
// 4. EEPROM Functions
// ----------------------------------------------------
void clearEEPROM() {
    for (int i = 0; i < EEPROM_SIZE; i++) {
        EEPROM.write(i, 0);
    }
    EEPROM.commit();
}

void initializeEEPROM() {
    bool initialized = false;
    for (int i = 0; i < EEPROM_SIZE; i++) {
        if (EEPROM.read(i) != 0) {
            initialized = true;
            break;
        }
    }
    if (!initialized) {
        clearEEPROM();
    }
}

void saveWiFiCredentials(const String &ssid, const String &password, const String &account) {
    EEPROM.writeString(SSID_ADDR, ssid);
    EEPROM.writeString(PASS_ADDR, password);
    EEPROM.writeString(ACCOUNT_ADDR, account);
    EEPROM.commit();
    Serial.println("Wi-Fi credentials and Account saved to EEPROM.");
}

bool readWiFiCredentials(String &ssid, String &password, String &account) {
    ssid = EEPROM.readString(SSID_ADDR);
    password = EEPROM.readString(PASS_ADDR);
    account = EEPROM.readString(ACCOUNT_ADDR);
    return !(ssid.isEmpty() || password.isEmpty() || account.isEmpty());
}

// ----------------------------------------------------
// 5. Non-blocking Wi-Fi Connection
// ----------------------------------------------------
void startWiFiConnect(const String &ssid, const String &pass) {
    if (invalidCredentials) {
        if (!invalidCredentialsMessagePrinted) {
            Serial.println("Invalid credentials. Waiting for new input.");
            invalidCredentialsMessagePrinted = true;
        }
        return;
    }

    WiFi.mode(WIFI_AP_STA);
    WiFi.softAP(ap_ssid, ap_password);
    WiFi.setSleep(false);
    wifiConnected = false;
    Serial.printf("Attempting to connect to Wi-Fi (SSID: %s)...\n", ssid.c_str());
    WiFi.disconnect(true);
    delay(50);
    WiFi.begin(ssid.c_str(), pass.c_str());
    connectStartTime = millis();
    connectingInProgress = true;
}

void processWiFiConnection() {
    if (!connectingInProgress) return;

    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("Connected to Wi-Fi. Saving new credentials...");
        saveWiFiCredentials(pendingSsid, pendingPass, pendingAccount);
        
        storedSsid = pendingSsid;
        storedPassword = pendingPass;
        storedAccount = pendingAccount;
        
        attemptConnectionFlag = false;
        connectingInProgress = false;
        invalidCredentials = false;
        invalidCredentialsMessagePrinted = false;
        uploadFailurePrinted = false;
        wifiStatusMessage = "Connected";
        lastCaptureMillis = millis();
        Serial.println("Connection successful.");
        wifiConnected = true;
    } else if (millis() - connectStartTime > 3000) {
        if (!invalidCredentialsMessagePrinted) {
            Serial.println("Invalid credentials. Waiting for new input.");
            invalidCredentialsMessagePrinted = true;
            invalidCredentials = true;
            connectingInProgress = false;
            wifiStatusMessage = "Fail to connect";
            wifiConnected = false;
        }
    }
}

// ----------------------------------------------------
// 6. Enable AP Mode
// ----------------------------------------------------
void enableAPMode() {
    if (!apModeStarted) {
        WiFi.mode(WIFI_AP_STA);
        WiFi.softAP(ap_ssid, ap_password);
        WiFi.setSleep(false);
        Serial.println("AP mode started!");
        Serial.print("AP IP Address: ");
        Serial.println(WiFi.softAPIP());
        apModeStarted = true;
    }
}

void ensureAPMode() {
    if (WiFi.getMode() != WIFI_AP && WiFi.getMode() != WIFI_AP_STA) {
        WiFi.mode(WIFI_AP_STA);
        WiFi.softAP(ap_ssid, ap_password);
        apModeStarted = false;
    }
}

// ----------------------------------------------------
// 7. Upload Image to Server
// ----------------------------------------------------
void uploadImageToServer() {
    if (!wifiConnected) return;
    
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
        if (!uploadFailurePrinted) {
            Serial.println("Image capture failed. Check the camera.");
            uploadFailurePrinted = true;
        }
        return;
    }
    
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "image/jpeg");
    http.addHeader("Account-Number", storedAccount);
    // Serial.println(storedAccount);
    int httpResponseCode = http.POST(fb->buf, fb->len);
    if (httpResponseCode == 200) {
        Serial.println("Image uploaded successfully.");
        uploadFailurePrinted = false;
    } else {
        if (!uploadFailurePrinted) {
            Serial.printf("Image upload failed. HTTP code: %d\n", httpResponseCode);
            uploadFailurePrinted = true;
        }
        // If you want to allow repeating error messages, comment this out:
        uploadFailurePrinted = false;
    }

    http.end();
    esp_camera_fb_return(fb);
}

// ----------------------------------------------------
// 8. Web Server for Configuration (removed WebSockets)
// ----------------------------------------------------
void setupServer() {
    server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(200, "text/html",
                      "<form action='/addwifi' method='POST'>"
                      "SSID: <input name='ssid'><br>"
                      "Password: <input name='password'><br>"
                      "Account Number: <input name='account'><br>"
                      "<input type='submit' value='Connect'>"
                      "</form>");
    });

    server.on("/addwifi", HTTP_GET, [](AsyncWebServerRequest *request) {
        String response = "<html><body><h2>Wi-Fi Status</h2>";
        response += "<p>" + wifiStatusMessage + "</p>";
        response += "</body></html>";
        request->send(200, "text/html", response);
    });

    server.on("/addwifi", HTTP_POST, [](AsyncWebServerRequest *request) {
        if (request->hasParam("ssid", true) &&
            request->hasParam("password", true) &&
            request->hasParam("account", true)) {
            
            pendingSsid = request->getParam("ssid", true)->value();
            pendingPass = request->getParam("password", true)->value();
            pendingAccount = request->getParam("account", true)->value();

            attemptConnectionFlag = true;
            invalidCredentials = false;
            invalidCredentialsMessagePrinted = false;
            wifiStatusMessage = "";

            unsigned long startTime = millis();
            bool connected = false;
            WiFi.disconnect(true);
            while (millis() - startTime < 3000) {
                if (WiFi.status() == WL_CONNECTED) {
                    connected = true;
                    break;
                }
                connected = false;
                delay(100);
            }
            if (connected) {
                wifiConnected = true;
                request->send(200, "text/plain", "Connected");
            } else {
                wifiConnected = false;
                request->send(400, "text/plain", "Failed to connect. Invalid credentials or network issue.");
            }
        } else {
            if (!(request->hasParam("account", true))){
              request->send(400, "text/plain", "Missing Account Number.");
            }
            else{
              request->send(400, "text/plain", "Missing SSID or Password.");
            }
        }
    });

    // We do NOT set up WebSockets here anymore since we're sending status via HTTP.
    server.begin();
}

// ----------------------------------------------------
// 9. Setup
// ----------------------------------------------------

// ----------------------------------------------------
// 10. Internal Temperature (Unofficial)
// ----------------------------------------------------
float getInternalTemperature() {
    // Very rough approximation. Not guaranteed accurate.
    // Formula can differ by module and environment.
    uint8_t raw = temprature_sens_read();
    float tempC = ((float)raw - 32)/(5.6);
    return tempC;
}

// ----------------------------------------------------
// 10.1. Send Status via HTTP (New Function)
// ----------------------------------------------------
void sendStatusToServer() {
    if (!wifiConnected) return;  // Only send if connected

    // Gather data
    float temperature = getInternalTemperature();
    String wifiStatus = (WiFi.status() == WL_CONNECTED) ? "Connected" : "Disconnected";
    // String batteryPercent = String(random(0, 100));  // Replace with actual battery level if available
    String batteryPercent = "64";
    // Build JSON
    String message = "{";
    message += "\"temperature\":\"" + String(temperature, 2) + "\",";
    message += "\"wifiStatus\":\"" + wifiStatus + "\",";
    message += "\"battery\":\"" + batteryPercent + "\",";
    message += "\"account\":\"" + storedAccount + "\"";
    message += "}";
    // Serial.println(storedAccount);
    // Send it to your server
    HTTPClient http;
    http.begin(statusUrl);  // Replace with your server's status endpoint
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(message);
    if (httpResponseCode == 200) {
        Serial.println("Status posted successfully");
    } else {
        Serial.printf("Status post failed HTTP code: %d\n", httpResponseCode);
    }
    http.end();
}

// ----------------------------------------------------
// 2. Send Heartbeat via HTTP
// ----------------------------------------------------
void sendHeartbeatToServer() {
    if (!wifiConnected) return;  // Only send if connected

    // Build heartbeat JSON with account number
    String message = "{";
    message += "\"status\":\"alive\",";
    message += "\"account\":\"" + storedAccount + "\"";
    message += "}";
    // Serial.println(storedAccount);
    // Send it to your server
    HTTPClient http;
    http.begin(heartbeatUrl);  
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(message);
    if (httpResponseCode == 200) {
        Serial.println("Heartbeat posted successfully");
    } else {
        Serial.printf("Heartbeat post failed HTTP code: %d\n", httpResponseCode);
    }
    http.end();
}


void setup() {
    Serial.begin(115200);
    EEPROM.begin(EEPROM_SIZE);
    initializeEEPROM();

    if (readWiFiCredentials(storedSsid, storedPassword, storedAccount)) {
        Serial.printf("Stored credentials found: SSID=%s\n", storedSsid.c_str());
    }

    setupCamera();
    enableAPMode();
    setupServer();

    if (!storedSsid.isEmpty()) {
        pendingSsid = storedSsid;
        pendingPass = storedPassword;
        pendingAccount = storedAccount;
        startWiFiConnect(storedSsid, storedPassword);
    }
    while(!wifiConnected){
      if (attemptConnectionFlag && !connectingInProgress) {
        startWiFiConnect(pendingSsid, pendingPass);
      }
      processWiFiConnection();
    }
    for (int i = 0; i < 10; i++) {
        camera_fb_t *tmp = esp_camera_fb_get();
        if (tmp) {
            esp_camera_fb_return(tmp);
        }
        delay(500); // brief pause between frames
    }
    uploadImageToServer();
}

// ----------------------------------------------------
// 11. Main Loop
// ----------------------------------------------------

void loop() {
    ensureAPMode();

    // Periodic status update 
    if (wifiConnected && millis() - lastStatusMillis >= statusInterval) {
        lastStatusMillis = millis();
        sendStatusToServer();
    }

    // Periodic heartbeat 
    if (wifiConnected && millis() - lastHeartbeatMillis >= heartbeatInterval) {
        lastHeartbeatMillis = millis();
        sendHeartbeatToServer();
    }

    delay(10);
}
