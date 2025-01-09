import React, { useState, useEffect } from "react";
import {
    View,
    Text,
    TextInput,
    TouchableOpacity,
    ActivityIndicator,
    PermissionsAndroid,
    KeyboardAvoidingView,
    ScrollView,
    Platform,
    Alert,
} from "react-native";
import { useRouter } from "expo-router";
import { useFonts } from "expo-font";

import { useUser } from "./contexts/userContext";
import CommonButton from "./components/commonButton";
import { handleLogin } from "./services/authService";

const LoginScreen = () => {
    console.log("Login Page Rendered");

    const [fontsLoaded, error] = useFonts({
        PlaywriteDEGrund: require("../assets/fonts/PlaywriteDEGrund-VariableFont_wght.ttf"),
    });

    const [loginWait, setLoginWait] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const router = useRouter();

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
        if (!username || !password) {
            Alert.alert("Error", "Please enter both username and password.");
            return;
        }

        setLoginWait(true);
        const loginResult = await handleLogin(username, password);
        setLoginWait(false);

        console.log(`Login response - ${loginResult}`);

        if (loginResult.status === 1) {
            console.log("Log in successful using Firebase!");
            router.replace({
                pathname: "/home",
            });
        } else {
            Alert.alert("Error", loginResult.message);
        }
    };

    const registerClicked = async () => {
        router.replace("/signup");
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
                {/* Login In Progress Overlay */}
                {loginWait && (
                    <View className="absolute inset-0 bg-black/50 justify-center items-center z-10">
                        <ActivityIndicator size="large" color="#ffffff" />
                    </View>
                )}
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
                    <View className="mt-5 pb-10 flex-row justify-center">
                        <Text className="text-gray-700">
                            Don't have an account?{" "}
                        </Text>
                        <TouchableOpacity onPress={registerClicked}>
                            <Text className="text-blue-500 underline font-bold">
                                Sign up
                            </Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </ScrollView>
        </KeyboardAvoidingView>
    );
};

export default LoginScreen;
