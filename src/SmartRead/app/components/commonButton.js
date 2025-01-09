import React from "react";
import { View, TouchableOpacity, Text } from "react-native";

// Common component - a button to be place at the bottom of the page
const CommonButton = ({ title, onPress, atBottom=true }) => {
    return (
        <View className={`${atBottom ? "absolute bottom-10 left-0 right-0" : ""} items-center`}>
            <View>
                <TouchableOpacity
                    onPress={onPress}
                    className="rounded-lg bg-indigo-200 py-2 px-5 self-center"
                    style={{
                        shadowColor: "#000",
                        shadowOffset: { width: 0, height: 2 },
                        shadowOpacity: 0.2,
                        shadowRadius: 2,
                        elevation: 3,
                        maxWidth: 200,
                    }}
                >
                    <Text className="text-black text-xl font-bold text-center">
                        {title}
                    </Text>
                </TouchableOpacity>
            </View>
        </View>
    );
};

export default CommonButton;
