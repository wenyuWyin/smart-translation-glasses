import React, { useState, useEffect } from "react";
import {
    View,
    Text,
    TextInput,
    PermissionsAndroid,
    KeyboardAvoidingView,
    ScrollView,
    Platform,
} from "react-native";
import { useRouter } from "expo-router";
import { useFonts } from "expo-font";

import { useUser } from "./contexts/userContext";
import CommonButton from "./components/commonButton";

const LoginScreen = () => {
    console.log("Login Page Rendered");

    const [fontsLoaded, error] = useFonts({
        PlaywriteDEGrund: require("../assets/fonts/PlaywriteDEGrund-VariableFont_wght.ttf"),
    });

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const router = useRouter();
    const { login } = useUser();

    // TODO: Move this to home page (when requesting network information)
    const requestPermissions = async () => {
        if (Platform.OS === "android") {
            try {
                const granted = await PermissionsAndroid.request(
                    PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
                    {
                        title: "Location permission is required for WiFi connections",
                        message:
                            "This app needs location permission as this is required to scan for WiFi networks.",
                        buttonNegative: "DENY",
                        buttonPositive: "ALLOW",
                    }
                );
                if (granted === PermissionsAndroid.RESULTS.GRANTED) {
                    console.log("Location permission granted");
                } else {
                    Alert.alert(
                        "Permission Denied",
                        "Location permission is required to scan WiFi networks."
                    );
                }
            } catch (err) {
                console.warn(err);
            }
        }
    };

    const loginClicked = async () => {
        const name = "User A";
        login(name);

        router.replace({
            pathname: "/home",
        });
    };

    // Load font
    useEffect(() => {
        if (error) {
            throw error;
        }

        if (fontsLoaded) {
            requestPermissions();
        }
    }, [fontsLoaded, error]);

    return (
        <KeyboardAvoidingView
            behavior={Platform.OS === "ios" ? "padding" : "height"}
            style={{ flex: 1 }}
        >
            <ScrollView contentContainerStyle={{ flexGrow: 1 }}>
                {/* Login Form */}
                <View className="flex-1 justify-center items-center bg-blue-100 p-4">
                    <Text
                        style={{
                            fontFamily: "PlaywriteDEGrund",
                            paddingTop: 8,
                            marginBottom: 20,
                        }}
                        className="text-4xl font-bold w-[100%] text-center"
                    >
                        SmartRead
                    </Text>
                    <TextInput
                        placeholder="Enter username"
                        value={username}
                        onChangeText={setUsername}
                        className="border border-gray-400 rounded-lg p-3 w-3/4 mb-4 bg-white"
                    />
                    <TextInput
                        placeholder="Enter password"
                        value={password}
                        onChangeText={setPassword}
                        className="border border-gray-400 rounded-lg p-3 w-3/4 mb-4 bg-white"
                    />
                    <CommonButton
                        title="Login"
                        onPress={loginClicked}
                        atBottom={false}
                    />
                </View>
            </ScrollView>
        </KeyboardAvoidingView>
    );
};

export default LoginScreen;
