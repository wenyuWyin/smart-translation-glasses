import React, { createContext, useState, useContext } from "react";

// Create user context to hold user data and authentication methods
export const UserContext = createContext();

// Provide the user context to components within app
export const UserProvider = ({ children }) => {
    // store user information
    const [user, setUser] = useState(null);

    const login = (id) => {
        setUser({ user_id: id });
    };

    const logout = () => {
        setUser(null);
    };

    return (
        // Pass user data and authentication functions to context consumer
        <UserContext.Provider value={{ user, login, logout }}>
            {children}
        </UserContext.Provider>
    );
};

// Hook to access the UserContext values within app components
export const useUser = () => useContext(UserContext);
