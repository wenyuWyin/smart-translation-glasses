import { useEffect, useContext, useRef } from "react";
import { SetupContext } from "../contexts/setupContext";

import { WEB_SOCKET_ADDRESS } from "@env";

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

    // Use a ref to store the WebSocket instance and heartbeat timeout
    const wsRef = useRef(null);
    const heartbeatTimeoutRef = useRef(null);

    const startHeartbeatTimeout = () => {
        clearTimeout(heartbeatTimeoutRef.current); // Clear any existing timeout
        heartbeatTimeoutRef.current = setTimeout(() => {
            console.log(`disconnected at -> ${Math.floor(Date.now() / 1000)}`);
            console.log("Heartbeat not received. Assuming ESP32 disconnected.");
            setDeviceConnected(false); // Mark device as disconnected
        }, 8000); // Timeout after 8 seconds
    };

    useEffect(() => {
        // Create a new WebSocket connection when both this app and ESP 32 is connected to internet
        if (!(appConnected && deviceConnected)) {
            return;
        }
        console.log("Attempting to connect WebSocket...");
        const ws = new WebSocket(WEB_SOCKET_ADDRESS);
        wsRef.current = ws;

        ws.onopen = () => {
            console.log("Websocket connected.");
        };

        // Event handler when a WebSocket message arrives
        ws.onmessage = (e) => {
            try {
                const message = JSON.parse(e.data);

                // Check for heartbeat message
                if (message["status"] === "alive") {
                    console.log(
                        `Heartbeat received at ${Math.floor(
                            Date.now() / 1000
                        )}.`
                    );
                    startHeartbeatTimeout(); // Reset the timeout on heartbeat
                    return;
                }

                setTemp(message["temperature"]);
                setDeviceConnected(message["wifiStatus"] === "Connected");
                setBattery(message["battery"]);
                console.log("Message received from ESP32", message);
            } catch (error) {
                console.error("Erroor parsing WebSocket message: ", error);
            }
        };

        // Assuming the device's network is disconnected when an error occurs or the WebSocket is closed
        ws.onerror = (error) => {
            setDeviceConnected(false);
            console.error("WebSocket error: ", error.message);
        };

        ws.onclose = () => {
            setDeviceConnected(false);
            console.log("WebSocket connection closed.");
        };

        return () => {
            clearTimeout(heartbeatTimeoutRef.current); // Clear heartbeat timeout on cleanup
            if (wsRef.current) {
                wsRef.current.close();
            }
        };
    }, [deviceConnected, appConnected]);
};

export default ESP32WebSocket;
