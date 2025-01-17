import { Stack } from "expo-router";
import { GestureHandlerRootView } from "react-native-gesture-handler";

import { UserProvider } from "./contexts/userContext";

import "./global.css";

const Layout = () => {
    return (
        <GestureHandlerRootView style={{ flex: 1 }}>
            <UserProvider>
                <Stack>
                    <Stack.Screen name="login" options={{ title: "Log In" }} />
                    <Stack.Screen
                        name="signup"
                        options={{ title: "Sign Up" }}
                    />

                    <Stack.Screen
                        name="(tabs)"
                        options={{ headerShown: false }} // Hides the header for tabs
                    />
                </Stack>
            </UserProvider>
        </GestureHandlerRootView>
    );
};

export default Layout;
