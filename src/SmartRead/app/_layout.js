import { Stack } from "expo-router";
import { UserProvider } from "./contexts/userContext";

import "./global.css";

const Layout = () => {
    return (
        <UserProvider>
            <Stack>
                <Stack.Screen name="home" options={{ title: "Home" }} />
                <Stack.Screen name="login" options={{ title: "Log In" }} />
            </Stack>
        </UserProvider>
    );
};

export default Layout;
