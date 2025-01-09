import React, { useState, createContext } from 'react';

export const SetupContext = createContext();

export const SetupProvider = ({ children }) => {
    const [step1Done, setStep1Done] = useState(false);
    const [step2Done, setStep2Done] = useState(false);

    return (
        <SetupContext.Provider value={{ step1Done, setStep1Done, step2Done, setStep2Done }}>
            {children}
        </SetupContext.Provider>
    )
}