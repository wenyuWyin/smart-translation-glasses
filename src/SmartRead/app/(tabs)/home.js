import React, { useState, useEffect, useContext } from "react";
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

import { Dropdown } from "react-native-element-dropdown";
import Ionicon from "react-native-vector-icons/Ionicons";
import MaterialIcon from "react-native-vector-icons/MaterialIcons";
import MaterialCommunityIcon from "react-native-vector-icons/MaterialCommunityIcons";
import WifiManager from "react-native-wifi-reborn";
import NetInfo from "@react-native-community/netinfo";
import auth from "@react-native-firebase/auth";

import styles from "../styles/styles";
import { SetupContext } from "../contexts/setupContext";
import { UserContext } from "../contexts/userContext";

const HomeScreen = () => {
    console.log("Home Page Rendered");

    const router = useRouter();

    const {
        langPrefDone,
        setLangPrefDone,
        deviceConnected,
        setDeviceConnected,
        appConnected,
        setAppConnected,
        deviceNetwork,
        setDeviceNetwork,
    } = useContext(SetupContext);
    const { user, login, logout } = useContext(UserContext);

    const onAuthStateChanged = (user) => {
        if (!user) {
            console.error(
                "Error",
                "Unable to fetch user data. Please try again later."
            );
        } else {
            console.log(`Got user from db - ${user.uid}`);
            login(user.uid);
        }
    };

    // Check log in state
    useEffect(() => {
        const subscriber = auth().onAuthStateChanged(onAuthStateChanged);
        return subscriber; // unsubscribe on unmount
    }, []);

    // Fetch language preferences from database when a user is set
    useEffect(() => {
        const fetchLanguagePref = async () => {
            if (user) {
                try {
                    setLangLoading(true);
                    const response = await fetch(
                        process.env.EXPO_PUBLIC_SERVER_IP_ADDRESS +
                            `/lang-pref?uid=${user.user_id}`,
                        {
                            method: "GET",
                        }
                    );
                    setLangLoading(false);

                    if (response.ok) {
                        const data = await response.json();
                        const source = data["source-lang"];
                        const target = data["target-lang"];
                        // Set relevant properties for the selection dropdowns
                        if (source && target) {
                            console.log(
                                `Got language preferences from db - ${source} to ${target}`
                            );
                            const sourceIndex =
                                languageOptions.findIndex(
                                    (lang) => lang.label === source
                                ) + 1;
                            const targetIndex =
                                languageOptions.findIndex(
                                    (lang) => lang.label === target
                                ) + 1;
                            setSourceLang(sourceIndex.toString());
                            setTargetLang(targetIndex.toString());
                            setLangPrefDone(true);
                        }
                    } else {
                        if (response.status === 404) {
                            throw new Error(
                                "Server is down. Please try again later."
                            );
                        }
                        throw new Error(
                            "Unknown error. Please try again later."
                        );
                    }
                } catch (error) {
                    Alert.alert("Error", `${error.message}`);
                }
            }
        };
        fetchLanguagePref();
    }, [user]);

    // Define event listener for Wi-Fi state changes
    useEffect(() => {
        const unsubscribe = NetInfo.addEventListener(async (state) => {
            if (state.type === "wifi") {
                setTimeout(async () => {
                    try {
                        const currentSSID =
                            await WifiManager.getCurrentWifiSSID();
                        console.log("Current SSID:", currentSSID);

                        if (!currentSSID.includes("ESP32_CAM_AP")) {
                            console.log("User connected to a local network!");
                            setAppConnected(true);
                        } else {
                            setAppConnected(false);
                        }
                    } catch (error) {
                        console.error("Error getting SSID:", error);
                    }
                }, 1000); // Delay for 1 second after the event to ensure SSID is ready
            }
        });

        return () => unsubscribe();
    }, []);

    // Language preference settings
    const [langLoading, setLangLoading] = useState(false);
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
        if (!user) {
            Alert.alert(
                "Error",
                "You must login to submit language preferences."
            );
            return;
        }
        if (!sourceLang) {
            Alert.alert("Error", "Please select a source language.");
            return;
        }
        if (!targetLang) {
            Alert.alert("Error", "Please select a target language.");
            return;
        }
        if (sourceLang === targetLang) {
            Alert.alert(
                "Error",
                "Source and target languages need to be different."
            );
            return;
        }

        try {
            // Store language preferences in the database
            setLangLoading(true);

            // Create AbortController and set a timeout for the post request
            const controller = new AbortController();
            const fetchTimeout = setTimeout(() => {
                controller.abort();
            }, 4000);

            const response = await fetch(
                process.env.EXPO_PUBLIC_SERVER_IP_ADDRESS + "/lang-pref",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        uid: user.user_id,
                        sourceLang: languageOptions[sourceLang - 1].label,
                        targetLang: languageOptions[targetLang - 1].label,
                    }),
                    signal: controller.signal,
                }
            );

            clearTimeout(fetchTimeout);
            setLangLoading(false);

            if (response.ok) {
                setLangPrefDone(true);
                Alert.alert("Success", "Successfully updated language preferences!")
            } else {
                if (response.status === 404) {
                    throw new Error("Server is down. Please try again later.");
                }
                throw new Error("Unknown error. Please try again later.");
            }
        } catch (error) {
            if (error.name === "AbortError") {
                Alert.alert(
                    "Error",
                    "Request timed out. Please try again later."
                );
            } else {
                Alert.alert("Error", `${error.message}`);
            }
        }
    };

    // Swap target language with source language
    const swapLanguagePreference = () => {
        const source = sourceLang;
        const target = targetLang;

        setSourceLang(target);
        setTargetLang(source);
    }

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
        if (appConnected) {
            Alert.alert("Error", "Please connect your phone to ESP32_CAM_AP.");
            return;
        }

        // Send the configuration only when the phone is connected to the camera access point
        console.log("Device succesffully connected to the device.");

        // Attempt to send the network configurations
        try {
            setCameraConnecting(true);

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
                )}&account=${encodeURIComponent(user.user_id)}`,
            });

            setCameraConnecting(false);

            if (response.ok) {
                setDeviceConnected(true);
                Alert.alert("Success", "Credentials are sent to your device!");
                router.push("/result");
            } else {
                const message = await response.text();
                throw new Error(`${response.status} - ${message}`);
            }
        } catch (error) {
            setCameraConnecting(false);
            console.error("Failed to send credentials.", error);
            Alert.alert(
                "Error",
                `Could not send credentials to your device. ${error.message}`
            );
        }
    };

    return (
        <KeyboardAvoidingView
            behavior={Platform.OS === "ios" ? "padding" : "height"}
            keyboardVerticalOffset={Platform.OS === "ios" ? 100 : 120}
            style={{ flex: 1 }}
        >
            <ScrollView
                contentContainerStyle={{ flexGrow: 1 }}
                keyboardShouldPersistTaps="handled"
            >
                <View className="flex-1 bg-blue-100 h-[100%] items-center">
                    {/* Step 1 - Specify Language Preferences */}
                    <View className="w-[90%] flex-col items-center py-3">
                        <View className="flex-row items-start mb-4 mt-4">
                            <Text className="text-lg font-bold">
                                Specify your Language Preferences
                            </Text>
                        </View>

                        {/* Selection Dropdowns */}
                        <View className="flex-col w-[80%] mb-4">
                            <Text className="text-left text-lg mb-2">
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

                        {/* Swap target and source languages */}
                        {sourceLang && targetLang && (
                            <TouchableOpacity
                                className="px-3 rounded-xl w-[14%] items-center"
                                onPress={swapLanguagePreference}
                            >
                                <MaterialCommunityIcon
                                    className=""
                                    name="swap-vertical"
                                    size={20}
                                />
                            </TouchableOpacity>
                        )}

                        <View className="flex-col w-[80%] mb-4">
                            <Text className="text-left text-lg mb-2">To: </Text>
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
                            {langLoading ? (
                                <ActivityIndicator
                                    size="large"
                                    color="#ffffff"
                                />
                            ) : (
                                <TouchableOpacity
                                    className="px-3 py-2 bg-blue-950 rounded-lg w-[50%] items-center"
                                    onPress={submitLanguagePreference}
                                >
                                    <Text className="text-white font-bold">
                                        {langPrefDone ? "Update" : "Save"}
                                    </Text>
                                </TouchableOpacity>
                            )}
                        </View>
                    </View>

                    <View className="border-b-2 border-black w-[90%] my-5" />

                    {/* Step 2 - Connect Microcontroller to Wifi */}
                    <View className="w-[90%] flex-col items-center mb-4">
                        <Text className="text-lg font-bold">
                            Connect your Device to a Wi-Fi
                        </Text>
                    </View>

                    {deviceConnected && deviceNetwork && (
                        <View className="flex-col items-center mb-4 bg-white rounded-lg border border-gray-300 shadow-md p-3">
                            <View className="flex-col items-center">
                                <View className="flex-row items-center">
                                    <Ionicon
                                        name="checkmark-circle"
                                        size={20}
                                        className="mr-2 mt-[2]"
                                        color="#02b34b"
                                    />
                                    <Text className="text-base text-gray-700">
                                        The device is connected to{" "}
                                        <Text className="font-bold text-black">
                                            {deviceNetwork}
                                        </Text>
                                    </Text>
                                </View>

                                <Text className="text-sm text-gray-500 mt-1">
                                    You are free to reconnect to a different
                                    network
                                </Text>
                            </View>
                        </View>
                    )}

                    <View className="w-[90%] flex-col items-center">
                        <View className="flex-row items-center mb-4 min-w-[90%]">
                            <MaterialIcon
                                name="looks-one"
                                size={20}
                                className="mr-2"
                            />
                            <Text className="text-lg">
                                Connect to "ESP32_CAM_AP" Wi-Fi
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

                        <View className="flex-row items-center mb-4 mt-8 min-w-[90%]">
                            <MaterialIcon
                                name="looks-two"
                                size={20}
                                className="mr-2"
                            />
                            <Text className="text-lg">
                                Send a Wi-Fi to your Device
                            </Text>
                        </View>

                        {/* Input Fields for Network Configurations */}
                        <View className="items-center w-[100%]">
                            <TextInput
                                placeholder={
                                    deviceConnected && deviceNetwork
                                        ? "Enter new network name"
                                        : "Enter network name"
                                }
                                value={networkName}
                                onChangeText={setNetworkName}
                                className="border border-gray-400 rounded-lg p-3 mb-4 bg-white w-[80%]"
                            />

                            <View className="w-[80%] relative mb-4">
                                <TextInput
                                    placeholder={
                                        deviceConnected && deviceNetwork
                                            ? "Enter new network password"
                                            : "Enter network password"
                                    }
                                    value={networkPwd}
                                    onChangeText={setNetworkPwd}
                                    secureTextEntry={pwdVisible}
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

                        <View className="w-[80%] items-center">
                            {cameraConnecting ? (
                                <ActivityIndicator
                                    size="large"
                                    color="#ffffff"
                                />
                            ) : (
                                <TouchableOpacity
                                    className="px-3 py-2 bg-blue-950 rounded-lg w-[50%] items-center"
                                    onPress={sendCredentialsToCamera}
                                >
                                    <Text className="text-white font-bold">
                                        {deviceConnected && deviceNetwork
                                            ? "Reconnect"
                                            : "Connect"}
                                    </Text>
                                </TouchableOpacity>
                            )}
                        </View>
                    </View>

                    <View className="border-b-2 border-black w-[90%] my-5" />

                    <TouchableOpacity
                        className="px-3 py-2 bg-[#993a25]  rounded-lg w-[50%] items-center"
                        onPress={() => {
                            logout();
                            router.replace("/login");
                        }}
                    >
                        <Text className="text-white font-bold">Logout</Text>
                    </TouchableOpacity>

                    <View className="w-[90%] flex-col items-center py-5" />
                </View>
            </ScrollView>
        </KeyboardAvoidingView>
    );
};

export default HomeScreen;
