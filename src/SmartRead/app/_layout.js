import { Stack } from "expo-router";
import { UserProvider } from "./contexts/userContext";

import "./global.css";

const Layout = () => {
    return (
        <UserProvider>
            <Stack>
                <Stack.Screen name="login" options={{ title: "Log In" }} />
                <Stack.Screen name="signup" options={{ title: "Sign Up" }} />
                
                <Stack.Screen
                    name="(tabs)"
                    options={{ headerShown: false }} // Hides the header for tabs
                />
            </Stack>
        </UserProvider>
    );
};

export default Layout;
