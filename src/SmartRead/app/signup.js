import React, { useState } from "react";
import { View, Text, TextInput, Platform,KeyboardAvoidingView, ScrollView } from "react-native";
import { useRouter } from "expo-router";
import CommonButton from "./components/commonButton";

const SignupScreen = () => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const router = useRouter();

    const signupClicked = () => {
        console.log("Signup details:", { username, email, password });
        // Add your signup logic here
    };

    return (
        <KeyboardAvoidingView
            behavior={Platform.OS === "ios" ? "padding" : "height"}
            style={{ flex: 1 }}
        >
            <ScrollView contentContainerStyle={{ flexGrow: 1 }}>
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
                    <TextInput
                        placeholder="Enter username"
                        value={username}
                        onChangeText={setUsername}
                        className="border border-gray-400 rounded-lg p-3 w-3/4 mb-4 bg-white"
                    />
                    <TextInput
                        placeholder="Enter email"
                        value={email}
                        onChangeText={setEmail}
                        className="border border-gray-400 rounded-lg p-3 w-3/4 mb-4 bg-white"
                    />
                    <TextInput
                        placeholder="Enter password"
                        value={password}
                        secureTextEntry
                        onChangeText={setPassword}
                        className="border border-gray-400 rounded-lg p-3 w-3/4 mb-4 bg-white"
                    />
                    <CommonButton
                        title="Sign Up"
                        onPress={signupClicked}
                        atBottom={false}
                    />
                    <View className="mt-5 flex-row justify-center">
                        <Text className="text-gray-700">Already have an account? </Text>
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
