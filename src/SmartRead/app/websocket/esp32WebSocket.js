import { useEffect, useContext, useRef } from "react";
import { SetupContext } from "../contexts/setupContext";

import io from "socket.io-client";

import { SERVER_IP_ADDRESS } from "@env";
import { UserContext } from "../contexts/userContext";

const ESP32WebSocket = () => {
    const {
        langPrefDone,
        setLangPrefDone,
        deviceConnected,
        setDeviceConnected,
        appConnected,
        SetAppConnected,
        temp,
        setTemp,
        battery,
        setBattery,
    } = useContext(SetupContext);
    const { user, login, logout } = useContext(UserContext);

    // Use a ref to store the WebSocket instance and heartbeat timeout
    const socketRef = useRef(null);

    useEffect(() => {
        // Create a new WebSocket connection when both this app and ESP 32 is connected to internet
        if (!(appConnected && deviceConnected)) {
            return;
        }
        console.log("Attempting to connect WebSocket...");
        const socket = io(SERVER_IP_ADDRESS);
        socketRef.current = socket;

        socket.on("connect", () => {
            console.log("Websocket connected.");

            // Send a registration message after connecting to the WebSocket
            const registrationMessage = {
                event: "register_user",
                user_id: user.user_id,
            };
            socket.emit("register_user", registrationMessage);

            // Define handlers for registration status
            socket.on("registration_success", (data) => {
                console.log("Registration successful:", data);
            });

            socket.on("registration_error", (error) => {
                console.error("Registration error:", error);
            });
        });

        // Event handler when a WebSocket message arrives
        socket.on("status_update", (data) => {
            try {
                console.log("Message received from ESP32", data);

                setTemp(data.temperature);
                setDeviceConnected(data.wifiStatus === "Connected");
                setBattery(data.battery);
            } catch (error) {
                console.error("Erroor parsing WebSocket message: ", error);
            }
        });

        socket.on("esp32_disconnect", () => {
            setDeviceConnected(false);
            console.log("WebSocket disconnected");
        });

        return () => {
            if (socketRef.current) {
                socketRef.current.disconnect();
            }
        };
    }, [deviceConnected, appConnected]);
};

export default ESP32WebSocket;
