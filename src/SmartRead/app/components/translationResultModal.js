import React from "react";
import { Modal, View, TouchableOpacity } from "react-native";
import TranslationResult from "./translationResult";

import MaterialCommunityIcon from "react-native-vector-icons/MaterialCommunityIcons";

const TranslationResultModel = ({
    imageUri,
    result,
    modalVisible,
    closeModal,
}) => {
    return (
        <Modal
            visible={modalVisible}
            animationType="slide"
            transparent={true}
            onRequestClose={closeModal}
        >
            <View className="flex-1 justify-center items-center bg-black/50">
                <View className="w-[95%] h-[34%] bg-gray-100 rounded-xl">
                    {/* Close Button */}
                    <TouchableOpacity
                        onPress={closeModal}
                        className="absolute right-3 top-2"
                    >
                        <MaterialCommunityIcon name="close-circle" size={22} />
                    </TouchableOpacity>

                    {/* TranslationResult Component */}
                    <TranslationResult imageUri={imageUri} result={result} />
                </View>
            </View>
        </Modal>
    );
};

export default TranslationResultModel;
