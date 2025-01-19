import React, { useState } from "react";
import {
    Alert,
    View,
    Text,
    TextInput,
    Platform,
    ActivityIndicator,
    KeyboardAvoidingView,
    ScrollView,
    TouchableOpacity,
} from "react-native";
import { useRouter } from "expo-router";
import CommonButton from "./components/commonButton";

import MaterialCommunityIcon from "react-native-vector-icons/MaterialCommunityIcons";

import { handleRegister } from "./services/authService";

const SignupScreen = () => {
    console.log("Signup Page Rendered");

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [pwdVisible, setPwdVisible] = useState(true);

    const [signupWait, setSignupWait] = useState(false);

    const router = useRouter();

    const signupClicked = async () => {
        // Check if any of the fields is empty
        if (!username) {
            Alert.alert("Error", "Username cannot be empty.");
            return;
        }
        if (!email) {
            Alert.alert("Error", "Email cannot be empty.");
            return;
        }
        if (!password) {
            Alert.alert("Error", "Password cannot be empty.");
            return;
        }

        setSignupWait(true);

        // Send signup request to backend
        const signupResponse = await handleRegister(username, email, password);

        setSignupWait(false);
        if (!signupResponse.status) {
            Alert.alert("Error", signupResponse.message);
        } else {
            router.replace("/home");
        }
    };

    return (
        <KeyboardAvoidingView
            behavior={Platform.OS === "ios" ? "padding" : "height"}
            style={{ flex: 1 }}
        >
            <ScrollView contentContainerStyle={{ flexGrow: 1 }}>
                {signupWait && (
                    <View className="absolute inset-0 bg-black/50 justify-center items-center z-10">
                        <ActivityIndicator size="large" color="#ffffff" />
                    </View>
                )}
                <View className="flex-1 justify-center items-center bg-blue-100 p-4">
                    <Text
                        style={{
                            fontFamily: "PlaywriteDEGrund", // Use your custom font
                            paddingTop: 8,
                            marginBottom: 20,
                        }}
                        className="text-4xl font-bold w-[100%] text-center"
                    >
                        Create an Account
                    </Text>
                    <View className="w-[80%] relative mt-10 mb-4">
                        <Text className="absolute text-sm left-2 -top-6 font-semibold">
                            Username
                        </Text>
                        <TextInput
                            placeholder={"Enter username"}
                            placeholderTextColor="gray"
                            value={username}
                            onChangeText={setUsername}
                            className="border border-gray-400 rounded-lg p-3 mb-4 bg-white w-[100%]"
                        />
                    </View>
                    <View className="w-[80%] relative mb-4">
                        <Text className="absolute text-sm left-2 -top-6 font-semibold">
                            Email
                        </Text>
                        <TextInput
                            placeholder={"Enter email"}
                            placeholderTextColor="gray"
                            value={email}
                            onChangeText={setEmail}
                            className="border border-gray-400 rounded-lg p-3 mb-4 bg-white w-[100%]"
                        />
                    </View>
                    <View className="w-[80%] relative mb-5">
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
                    <CommonButton
                        title="Sign Up"
                        onPress={signupClicked}
                        atBottom={false}
                    />
                    <View className="mt-5 flex-row justify-center">
                        <Text className="text-gray-700">
                            Already have an account?{" "}
                        </Text>
                        <Text
                            className="text-blue-500 underline font-bold"
                            onPress={() => router.replace("/login")}
                        >
                            Log in
                        </Text>
                    </View>
                </View>
            </ScrollView>
        </KeyboardAvoidingView>
    );
};

export default SignupScreen;
