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

import MaterialCommunityIcon from "react-native-vector-icons/MaterialCommunityIcons";

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
    const [pwdVisible, setPwdVisible] = useState(true);
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

        console.log(`Login response - ${loginResult.status} - ${loginResult.message}`);

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

                    <View className="items-center w-[100%] mt-10 mb-5">
                        <View className="w-[80%] relative mb-4">
                            <Text className="absolute text-sm left-2 -top-6 font-semibold">
                                Email
                            </Text>
                            <TextInput
                                placeholder={"Enter email"}
                                placeholderTextColor="gray"
                                value={username}
                                onChangeText={setUsername}
                                className="border border-gray-400 rounded-lg p-3 bg-white w-[100%]"
                            />
                        </View>

                        <View className="w-[80%] relative my-4">
                            <Text className="absolute text-sm left-2 -top-6 font-semibold">
                                Password
                            </Text>
                            <TextInput
                                placeholder={"Enter password"}
                                placeholderTextColor="gray"
                                value={password}
                                onChangeText={setPassword}
                                secureTextEntry={pwdVisible}
                                className="border border-gray-400 rounded-lg p-3 bg-white w-[100%]"
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
