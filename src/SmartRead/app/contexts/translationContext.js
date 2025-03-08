import React, { useState, createContext } from "react";

export const TranslationContext = createContext();

// Shared context for translation status and result
export const TranslationProvider = ({ children }) => {
    const [translationList, setTranslationList] = useState([]);
    const [translationIndex, setTranslationIndex] = useState(0);

    return (
        <TranslationContext.Provider
            value={{
                translationList,
                setTranslationList,
                translationIndex,
                setTranslationIndex,
            }}
        >
            {children}
        </TranslationContext.Provider>
    );
};
