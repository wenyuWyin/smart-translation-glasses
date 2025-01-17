import React, { useState } from "react";
import { View, Text, Modal, TouchableOpacity } from "react-native";
import TranslationResult from "./translationResult";

import MaterialCommunityIcon from "react-native-vector-icons/MaterialCommunityIcons";

// Modal component for translation results
const TranslationResultModal = ({
    imageUri,
    result,
    modalVisible,
    closeModal,
}) => {
    const [showHelp, setShowHelp] = useState(false);

    return (
        <Modal
            visible={modalVisible}
            animationType="slide"
            transparent={true}
            onRequestClose={closeModal}
        >
            <View className="flex-1 justify-center items-center bg-black/50">
                <View className="flex-col w-[95%] h-[29%] bg-gray-100 rounded-xl">
                    <View className="flex-row justify-between mt-1">
                        {/* Help Icons */}
                        {showHelp ? (
                            <TouchableOpacity
                                onPress={() => {
                                    setShowHelp(!showHelp);
                                }}
                            >
                                <View className="flex-row items-center ml-4">
                                    <Text>Toggle</Text>
                                    <MaterialCommunityIcon
                                        name="gesture-tap"
                                        size={22}
                                        className="mr-2"
                                    />
                                    <Text>Resize</Text>
                                    <MaterialCommunityIcon
                                        name="gesture-double-tap"
                                        size={22}
                                        className="mr-2"
                                    />
                                    <Text>Move</Text>
                                    <MaterialCommunityIcon
                                        name="gesture-swipe-horizontal"
                                        size={22}
                                    />
                                </View>
                            </TouchableOpacity>
                        ) : (
                            <TouchableOpacity
                                onPress={() => {
                                    setShowHelp(!showHelp);
                                }}
                            >
                                <View className="flex-row items-center mx-4">
                                    <MaterialCommunityIcon
                                        name="help-circle"
                                        size={22}
                                        className="mr-2"
                                    />
                                </View>
                            </TouchableOpacity>
                        )}

                        <TouchableOpacity
                            onPress={closeModal}
                            className="items-end mr-3"
                        >
                            <MaterialCommunityIcon
                                name="close-circle"
                                size={22}
                            />
                        </TouchableOpacity>
                    </View>
                    {/* TranslationResult Component */}
                    <TranslationResult imageUri={imageUri} result={result} />
                </View>
            </View>
        </Modal>
    );
};

export default TranslationResultModal;
