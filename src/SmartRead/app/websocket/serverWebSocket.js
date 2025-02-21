import { useEffect, useContext, useRef } from "react";

import io from "socket.io-client";
import * as FileSystem from "expo-file-system";

import { UserContext } from "../contexts/userContext";
import { SetupContext } from "../contexts/setupContext";
import { TranslationContext } from "../contexts/translationContext";

const ServerWebSocket = () => {
    const {
        setDeviceConnected,
        appConnected,
        setTemp,
        setBattery,
        setDeviceNetwork,
    } = useContext(SetupContext);
    const { user } = useContext(UserContext);
    const {
        setTrnStateCode,
        setTrnImage,
        setTrnResult,
    } = useContext(TranslationContext);

    // Use a ref to store the WebSocket instance and heartbeat timeout
    const socketRef = useRef(null);

    useEffect(() => {
        // Create a new WebSocket connection when both this app and ESP 32 is connected to internet
        if (!appConnected) {
            return;
        }
        console.log("Attempting to connect WebSocket...");
        const socket = io(process.env.EXPO_PUBLIC_SERVER_IP_ADDRESS);
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

        // Event handler when a WebSocket status update message arrives
        socket.on("status_update", (data) => {
            try {
                console.log("Message received from server", data);

                setTemp(data.temperature);
                setDeviceConnected(data.wifiStatus === "Connected");
                setBattery(data.battery);
                setDeviceNetwork(data.wifiName)
            } catch (error) {
                console.error("Error parsing WebSocket message: ", error);
            }
        });

        // Event handler when a WebSocket image progress update message arrives
        socket.on("image_progress_update", async (data) => {
            try {
                console.log("Message received from server", data);

                setTrnStateCode(data.state);
                if (data.image) {
                    setTrnImage(data.image);
                    setTrnResult(null);
                }
                if (data.result) {
                    setTrnResult(data.result);
                }
            } catch (error) {
                console.error("Error parsing WebSocket message: ", error);
            }
        });

        socket.on("esp32_disconnect", () => {
            setDeviceConnected(false);
            setDeviceNetwork("");
            console.log("WebSocket disconnected");
        });

        return () => {
            if (socketRef.current) {
                socketRef.current.disconnect();
            }
        };
    }, [appConnected]);
};

export default ServerWebSocket;
