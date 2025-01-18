import React from "react";
import { View, Text, Modal, TouchableOpacity } from "react-native";

import MaterialCommunityIcon from "react-native-vector-icons/MaterialCommunityIcons";

const TranslationHelpModal = ({ visible, onClose }) => {
    return (
        <Modal
            visible={visible}
            transparent={true}
            animationType="fade"
            onRequestClose={onClose}
        >
            <View className="flex-1 justify-center items-center bg-black/50">
                <View className="bg-white rounded-lg w-4/5 p-3 items-center">
                    <Text className="text-lg font-bold mb-4">
                        Gesture Instructions
                    </Text>
                    <Text className="text-sm mb-2">
                        Tap Once: Toggle background
                    </Text>
                    <Text className="text-sm mb-2">
                        Tap Twice: Resize image
                    </Text>
                    <Text className="text-sm mb-2">
                        Hold and drag: Move image
                    </Text>

                    <TouchableOpacity
                        onPress={onClose}
                        className="absolute py-1 px-1 rounded-md top-[9] right-[6]"
                    >
                        <MaterialCommunityIcon name="close-circle" size={22} />
                    </TouchableOpacity>
                </View>
            </View>
        </Modal>
    );
};

export default TranslationHelpModal;
