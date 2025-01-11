#include <WiFi.h>
#include <HTTPClient.h>
#include <ESPAsyncWebServer.h>
#include <EEPROM.h>
#include "esp_camera.h"

// ----------------------------------------------------
// 1. Config Constants
// ----------------------------------------------------
// AP credentials and server URL for image upload
const char* ap_ssid = "ESP32_CAM_AP";
const char* ap_password = "12345678";
const char* serverUrl = "http://192.168.2.15:5000/upload";

//EEPROM allocation and addresses for storeing Wi-Fi and account number
#define EEPROM_SIZE 512
#define SSID_ADDR 0
#define PASS_ADDR 64
#define ACCOUNT_ADDR 128
#define MAX_CREDENTIAL_LENGTH 64

//Interval and timing variables for image capture
unsigned long captureInterval = 3000;
unsigned long lastCaptureMillis = 0;

// Flags for connection handling
bool attemptConnectionFlag = false;
bool connectingInProgress = false;
bool invalidCredentials = false;
bool invalidCredentialsMessagePrinted = false;
bool apModeStarted = false;
bool uploadFailurePrinted = false; // Flag to track upload failure messages
bool wifiConnected = false; // Flag to control image capturing to check if wifi is connected. 
//Only capturing image when wifi is connected 


// Strings to hold credentials 
String pendingSsid = "";
String pendingPass = "";
String pendingAccount = "";
String storedSsid = "";
String storedPassword = "";
String storedAccount = "";

// Shows final status once: "Connected" or "Fail to connect"
String wifiStatusMessage = "";  

unsigned long connectStartTime = 0;

// Web server instance
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
// Sets up camera parameters, initilizes the camera,
// and configures sensor settings like brightness, contrast, etc
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
    }
    Serial.println("Camera initialized successfully!");
}

// ----------------------------------------------------
// 4. EEPROM Functions
// ----------------------------------------------------
// Responsible for clearing the EEPROM, initilizing and saving 
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
    // clearEEPROM();
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
    return !(ssid.isEmpty() || password.isEmpty()||account.isEmpty());
}

// ----------------------------------------------------
// 5. Non-blocking Wi-Fi Connection
// ----------------------------------------------------
// Attempts to connect using STA mode, while AP mode is always active 
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
// Ensures the device is always in AP mode for user to input credentials 
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
// Captures an image from the camera and uploads its through HTTP POST
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

    int httpResponseCode = http.POST(fb->buf, fb->len);
    // Serial.println(fb->len);
    if (httpResponseCode == 200) {
        Serial.println("Image uploaded successfully.");
        uploadFailurePrinted = false;
    } else {
        if (!uploadFailurePrinted) {
            // Serial.println("Checkpoint2");
            Serial.printf("Image upload failed. HTTP code: %d\n", httpResponseCode);
            uploadFailurePrinted = true;
        } 
        uploadFailurePrinted = false; //NEW SHIT
        
    }

    http.end();
    esp_camera_fb_return(fb);
}

// ----------------------------------------------------
// 8. Web Server
// ----------------------------------------------------
// Hosts a web page where the user can enter SSID password and account
// POST requests attempt to connect the device to provided network
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
            // Actively wait for the Wi-Fi process to complete (3 seconds max)
            while (millis() - startTime < 3000) {
                if (WiFi.status() == WL_CONNECTED) {
                    connected = true;
                    break;
                }
                connected = false;
                delay(100); // Keep the system tasks running
            }
            // Evaluate the connection result and send the response
            if (connected) {
                wifiConnected = true;
                request->send(200, "text/html", "Connected");
            } else {
                wifiConnected = false;
                request->send(400, "text/html", "Failed to connect. Invalid credentials or network issue.");
            }
            
        } else {
            // Missing parameters
            request->send(400, "text/plain", "Missing SSID, Password, or Account Number.");
        }
    });            

    server.begin();
}

// ----------------------------------------------------
// 9. Setup
// ----------------------------------------------------
// Initializes serial, EEPROM, reads stored credentials, sets up camera and AP
// and attempts to connect if saved credentials exists.
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
}

// ----------------------------------------------------
// 10. Main Loop
// ----------------------------------------------------
// Keeps the AP mode active, handles connection process,
// and periodically uploads images if connected. 
void loop() {
    ensureAPMode();

    if (attemptConnectionFlag && !connectingInProgress) {
        startWiFiConnect(pendingSsid, pendingPass);
    }

    processWiFiConnection();

    if (wifiConnected && millis() - lastCaptureMillis >= captureInterval) {
        lastCaptureMillis = millis();
        uploadImageToServer();
    }

    delay(10);
}

