import { Tabs } from "expo-router";
import MaterialIcon from "react-native-vector-icons/MaterialIcons";

import { SetupProvider } from "../contexts/setupContext";
import ESP32WebSocket from "../websocket/esp32WebSocket";

export default function TabLayout() {
    return (
        <SetupProvider>
            {/* Keep WebSocket module running in the background */}
            <ESP32WebSocket />
            
            <Tabs
                screenOptions={{
                    tabBarActiveTintColor: "#172554",
                    tabBarInactiveTintColor: "#7E7E7E",
                    tabBarStyle: {
                        backgroundColor: "#FFFFFF",
                        height: 60,
                    },
                }}
            >
                <Tabs.Screen
                    name="home"
                    options={{
                        tabBarLabel: "Setup",
                        title: "Setup",
                        tabBarIcon: ({ color, size }) => (
                            <MaterialIcon
                                name="phonelink-setup"
                                size={size}
                                color={color}
                            />
                        ),
                    }}
                />
                <Tabs.Screen
                    name="result"
                    options={{
                        tabBarLabel: "Translation Result",
                        title: "Translation Result",
                        tabBarIcon: ({ color, size }) => (
                            <MaterialIcon
                                name="translate"
                                size={size}
                                color={color}
                            />
                        ),
                    }}
                />
                <Tabs.Screen
                    name="history"
                    options={{
                        tabBarLabel: "Translation History",
                        title: "Translation History",
                        tabBarIcon: ({ color, size }) => (
                            <MaterialIcon
                                name="history"
                                size={size}
                                color={color}
                            />
                        ),
                    }}
                />
            </Tabs>
        </SetupProvider>
    );
}
