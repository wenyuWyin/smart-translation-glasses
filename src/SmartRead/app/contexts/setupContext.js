import React, { useState, createContext } from "react";

export const SetupContext = createContext();

// Shared context for device set-up and status
export const SetupProvider = ({ children }) => {
    const [langPrefDone, setLangPrefDone] = useState(false);
    const [deviceConnected, setDeviceConnected] = useState(false);
    const [appConnected, setAppConnected] = useState(false);
    const [temp, setTemp] = useState("");
    const [battery, setBattery] = useState("");

    return (
        <SetupContext.Provider
            value={{
                langPrefDone,
                setLangPrefDone,
                deviceConnected,
                setDeviceConnected,
                appConnected,
                setAppConnected,
                temp,
                setTemp,
                battery,
                setBattery,
            }}
        >
            {children}
        </SetupContext.Provider>
    );
};
