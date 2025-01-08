import React, { useState, useEffect } from "react";
import {
    View,
    Text,
    TextInput,
    Alert,
    ActivityIndicator,
    Linking,
    KeyboardAvoidingView,
    ScrollView,
    Platform,
    TouchableOpacity,
} from "react-native";
import { useRouter } from "expo-router";

import { SERVER_IP_ADDRESS } from "@env";
import { Dropdown } from "react-native-element-dropdown";
import MaterialIcon from "react-native-vector-icons/MaterialIcons";
import MaterialCommunityIcon from "react-native-vector-icons/MaterialCommunityIcons";
import WifiManager from "react-native-wifi-reborn";
import auth from "@react-native-firebase/auth";

import styles from "./styles/styles";
import TopLeftButton from "./components/topLeftButton";

const HomeScreen = () => {
    console.log("Home Page Rendered");

    const router = useRouter();

    // Initialize a user
    const [user, setUser] = useState();

    const onAuthStateChanged = (user) => {
        if (!user) {
            console.error(
                "Error",
                "Unable to fetch user data. Please try again later."
            );
        } else {
            setUser(user);
        }
    };

    // Check log in state
    useEffect(() => {
        const subscriber = auth().onAuthStateChanged(onAuthStateChanged);
        return subscriber; // unsubscribe on unmount
    }, []);

    // Language preference settings
    const [sourceLang, setSourceLang] = useState(null);
    const [targetLang, setTargetLang] = useState(null);
    const [isSourceFocus, setIsSourceFocus] = useState(false);
    const [isTargetFocus, setIsTargetFocus] = useState(false);

    // Camera network configurations
    const [cameraConnecting, setCameraConnecting] = useState(false);
    const [networkName, setNetworkName] = useState("");
    const [networkPwd, setNetworkPwd] = useState("");
    const [pwdVisible, setPwdVisible] = useState(false);

    // All language options
    const languageOptions = [
        { label: "English", value: "1" },
        { label: "French", value: "2" },
        { label: "Chinese", value: "3" },
        { label: "Japanese", value: "4" },
        { label: "Italian", value: "5" },
    ];

    // Send language preference to Firebase database through backend server
    const submitLanguagePreference = async () => {
        try {
            console.log(SERVER_IP_ADDRESS + "/lang-pref");
            const response = await fetch(SERVER_IP_ADDRESS + "/lang-pref", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    sourceLang: languageOptions[sourceLang - 1].label,
                    targetLang: languageOptions[targetLang - 1].label,
                }),
            });
        } catch (error) {
            console.log(
                `An error occurred when saving language preferences - ${error}`
            );
        }
    };

    // Navigate to system setting page for users to connect to the camera access point
    const connectToCamera = async () => {
        try {
            if (Platform.OS === "android") {
                Linking.sendIntent("android.settings.WIFI_SETTINGS");
            } else if (Platform.OS === "ios") {
                Linking.openURL("App-Prefs:root=WIFI");
            }
        } catch (error) {
            Alert.alert("Error", "Unable to open Wi-Fi settings.");
            console.error("Failed to open Wi-Fi settings:", error);
        }
    };

    // Send network configurations to camera
    const sendCredentialsToCamera = async () => {
        setCameraConnecting(true);
        const currentSSID = await WifiManager.getCurrentWifiSSID();
        console.log(currentSSID);

        // Send the configuration only when the phone is connected to the camera access point
        if (currentSSID === "ESP32_CAM_AP") {
            console.log("Device succesffully connected to the device.");

            // Attempt to send the network configurations
            try {
                const cameraUrl = "http://192.168.4.1/addwifi";

                // Send the configurations using an HTTPS POST request
                const response = await fetch(cameraUrl, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    body: `ssid=${encodeURIComponent(
                        networkName
                    )}&password=${encodeURIComponent(
                        networkPwd
                    )}&account=${encodeURIComponent(user.uid)}`,
                });

                setCameraConnecting(false);
                if (response.ok) {
                    Alert.alert(
                        "Success",
                        "Credentials are sent to your device!"
                    );
                } else {
                    throw new Error(
                        `${response.status} - ${response.statusText}`
                    );
                }
            } catch (error) {
                setCameraConnecting(false);
                console.error("Failed to send credentials.", error);
                Alert.alert(
                    "Error",
                    `Could not send credentials to your device. ${error.message}`
                );
            }
        } else {
            setCameraConnecting(false);
            console.log("Cannot connect");
            Alert.alert(
                "Error",
                "You must first connect to the device's network!"
            );
        }
    };

    return (
        <KeyboardAvoidingView
            behavior={Platform.OS === "ios" ? "padding" : "height"}
            keyboardVerticalOffset={Platform.OS === "ios" ? 60 : 0}
            style={{ flex: 1 }}
        >
            <ScrollView
                contentContainerStyle={{ flexGrow: 1 }}
                keyboardShouldPersistTaps="handled"
            >
                <View className="flex-1 bg-blue-100 h-[100%] items-center">
                    {/* Left Menu Button */}
                    <TopLeftButton
                        IconComponent={
                            <MaterialCommunityIcon name="menu" size={30} />
                        }
                        onPress={() => {
                            router.replace("/login");
                        }}
                    />

                    {/* Page Title */}
                    <View className="flex-row justify-center w-[72%] mt-5">
                        <Text className="text-xl font-bold">
                            Getting Started
                        </Text>
                    </View>

                    {/* Step 1 - Specify Language Preferences */}
                    <View className="w-[90%] flex-col items-center py-3">
                        <View className="flex-row items-center mb-4">
                            <MaterialIcon
                                name="looks-one"
                                size={20}
                                className="mr-2"
                            />
                            <Text className="text-lg font-medium">
                                Specify your language preferences
                            </Text>
                        </View>

                        {/* Selection Dropdowns */}
                        <View className="flex-col w-[80%] mb-4">
                            <Text className="text-left text-xl mb-2">
                                From:{" "}
                            </Text>
                            <Dropdown
                                style={[
                                    styles.dropdown,
                                    isSourceFocus && { borderColor: "blue" },
                                ]}
                                placeholderStyle={styles.placeholderStyle}
                                selectedTextStyle={styles.selectedTextStyle}
                                inputSearchStyle={styles.inputSearchStyle}
                                iconStyle={styles.iconStyle}
                                data={languageOptions}
                                maxHeight={300}
                                labelField="label"
                                valueField="value"
                                placeholder={
                                    !isSourceFocus ? "Select a language" : "..."
                                }
                                searchPlaceholder="Search..."
                                value={sourceLang}
                                onFocus={() => setIsSourceFocus(true)}
                                onBlur={() => setIsSourceFocus(false)}
                                onChange={(item) => {
                                    setSourceLang(item.value);
                                    setIsSourceFocus(false);
                                }}
                                renderLeftIcon={() => (
                                    <MaterialIcon
                                        className="mr-3"
                                        name="language"
                                        size={20}
                                    />
                                )}
                            />
                        </View>

                        <View className="flex-col w-[80%] mb-4">
                            <Text className="text-left text-xl mb-2">To: </Text>
                            <Dropdown
                                style={[
                                    styles.dropdown,
                                    isTargetFocus && { borderColor: "blue" },
                                ]}
                                placeholderStyle={styles.placeholderStyle}
                                selectedTextStyle={styles.selectedTextStyle}
                                inputSearchStyle={styles.inputSearchStyle}
                                iconStyle={styles.iconStyle}
                                data={languageOptions}
                                maxHeight={300}
                                labelField="label"
                                valueField="value"
                                placeholder={
                                    !isTargetFocus ? "Select a language" : "..."
                                }
                                searchPlaceholder="Search..."
                                value={targetLang}
                                onFocus={() => setIsTargetFocus(true)}
                                onBlur={() => setIsTargetFocus(false)}
                                onChange={(item) => {
                                    setTargetLang(item.value);
                                    setIsTargetFocus(false);
                                }}
                                renderLeftIcon={() => (
                                    <MaterialIcon
                                        className="mr-3"
                                        name="language"
                                        size={20}
                                    />
                                )}
                            />
                        </View>

                        <View className="w-[80%] items-center">
                            <TouchableOpacity
                                className="px-3 py-2 bg-blue-950 rounded-lg w-[50%] items-center"
                                onPress={submitLanguagePreference}
                            >
                                <Text className="text-white font-bold">
                                    Save
                                </Text>
                            </TouchableOpacity>
                        </View>
                    </View>

                    <View className="border-b-2 border-black w-[90%] my-5" />

                    {/* Step 2 - Connect Phone to Camera (Microcontroller) */}
                    <View className="w-[90%] flex-col items-center py-5">
                        <View className="flex-row items-center mb-4 w-[87%]">
                            <MaterialIcon
                                name="looks-two"
                                size={20}
                                className="mr-2"
                            />
                            <Text className="text-lg font-medium">
                                Connect this app to your device
                            </Text>
                        </View>

                        <View className="w-[80%] items-center">
                            <TouchableOpacity
                                className="px-3 py-2 bg-blue-950 rounded-lg w-[50%] items-center"
                                onPress={connectToCamera}
                            >
                                <Text className="text-white font-bold">
                                    Connect
                                </Text>
                            </TouchableOpacity>
                        </View>
                    </View>

                    <View className="border-b-2 border-black w-[90%] my-5" />

                    {/* Step 3 - Send Network Name and Password to Camera */}
                    <View className="w-[90%] flex-col items-center py-5">
                        <View className="flex-row items-center mb-4">
                            <MaterialIcon
                                name="looks-3"
                                size={20}
                                className="mr-2"
                            />
                            <Text className="text-lg font-medium">
                                Connect your device to a network
                            </Text>
                        </View>

                        {/* Input Fields for Network Configurations */}
                        <View className="items-center w-[100%]">
                            <TextInput
                                placeholder="Enter network name"
                                value={networkName}
                                onChangeText={setNetworkName}
                                className="border border-gray-400 rounded-lg p-3 mb-4 bg-white w-[80%]"
                            />

                            <View className="w-[80%] relative mb-4">
                                <TextInput
                                    placeholder="Enter network password"
                                    value={networkPwd}
                                    onChangeText={setNetworkPwd}
                                    secureTextEntry={!pwdVisible}
                                    className="border border-gray-400 rounded-lg p-3 pr-12 bg-white w-[100%]"
                                />
                                <TouchableOpacity
                                    onPress={() => setPwdVisible(!pwdVisible)}
                                    className="absolute right-3 top-2"
                                >
                                    <MaterialCommunityIcon
                                        name={pwdVisible ? "eye-off" : "eye"}
                                        size={24}
                                        color="#888"
                                    />
                                </TouchableOpacity>
                            </View>
                        </View>

                        <View className="w-[80%] items-center mb-5">
                            {cameraConnecting ? (
                                <ActivityIndicator size="large" color="#ffffff" />
                            ) : (
                                <TouchableOpacity
                                    className="px-3 py-2 bg-blue-950 rounded-lg w-[50%] items-center"
                                    onPress={sendCredentialsToCamera}
                                >
                                    <Text className="text-white font-bold">
                                        Connect
                                    </Text>
                                </TouchableOpacity>
                            )}
                        </View>
                    </View>
                </View>
            </ScrollView>
        </KeyboardAvoidingView>
    );
};

export default HomeScreen;
