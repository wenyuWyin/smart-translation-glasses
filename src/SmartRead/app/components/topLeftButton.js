import React from "react";
import { View, TouchableOpacity } from "react-native";

// Common component - a component positioned at the top-left corner of the page
const TopLeftButton = ({ IconComponent, onPress }) => {
    return (
        <View className="absolute top-[9] left-[5]">
            <TouchableOpacity onPress={onPress} className="p-1">
                {IconComponent}
            </TouchableOpacity>

        </View>
    );
}

export default TopLeftButton;