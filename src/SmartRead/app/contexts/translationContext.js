import React, { useState, createContext } from "react";

export const TranslationContext = createContext();

// Shared context for translation status and result
export const TranslationProvider = ({ children }) => {
    const [trnStateCode, setTrnStateCode] = useState(1);
    const [trnImage, setTrnImage] = useState(null);
    const [trnResult, setTrnResult] = useState(null);

    return (
        <TranslationContext.Provider
            value={{
                trnStateCode,
                setTrnStateCode,
                trnImage,
                setTrnImage,
                trnResult,
                setTrnResult,
            }}
        >
            {children}
        </TranslationContext.Provider>
    );
};
