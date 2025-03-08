import React, { useContext } from "react";
import {
    Modal,
    View,
    Text,
    Image,
    FlatList,
    TouchableOpacity,
} from "react-native";

import MaterialIcons from "react-native-vector-icons/MaterialIcons";

import { TranslationContext } from "../contexts/translationContext";
import { convertStateToIcon } from "../services/imageProcessState";

export default function ResultListModal({ visible, onClose }) {
    const {
        translationList,
        setTranslationList,
        translationIndex,
        setTranslationIndex,
    } = useContext(TranslationContext);

    if (!visible) {
        return null;
    }

    // Handle remove button click from the modal
    const handleRemove = (index) => {
        setTranslationList((prev) => {
            // Remove the item from the translation list
            const updated = [...prev];
            updated.splice(index, 1);

            // Move the translation index to the next item
            var newIndex = translationIndex;

            if (updated.length === 0) {
                newIndex = 0;
            } else if (index < updated.length) {
                newIndex = index;
            } else {
                newIndex = updated.length - 1;
            }

            setTranslationIndex(newIndex);
            return updated;
        });
    };

    return (
        <Modal
            visible={visible}
            animationType="slide"
            onRequestClose={onClose}
            transparent={true}
        >
            <View className="flex-1 justify-center items-center bg-black/50">
                <View className="w-[80%] bg-white p-5 rounded-lg shadow-lg max-h-[70%]">
                    {/* Title */}
                    <Text className="text-lg mb-2 px-4 font-bold text-center">
                        Translation List
                    </Text>

                    {/* List of Translation Items */}
                    {translationList.length > 0 ? (
                        <FlatList
                            data={translationList}
                            keyExtractor={(item, index) => index.toString()}
                            showsVerticalScrollIndicator={true}
                            style={{ maxHeight: 300 }}
                            renderItem={({ item, index }) => (
                                <View className="flex-row justify-between items-center w-full p-1 rounded-lg">
                                    {/* Image */}
                                    <Image
                                        source={{
                                            uri: `data:image/jpeg;base64,${item.image}`,
                                        }}
                                        className="h-[60px] w-[60px] rounded-md"
                                        resizeMode="contain"
                                    />

                                    {/* State Icon */}
                                    <Text className="text-black font-medium text-lg">
                                        {convertStateToIcon(item.status)}
                                    </Text>

                                    {/* Removal Button */}
                                    <TouchableOpacity
                                        onPress={() => {
                                            handleRemove(index);
                                        }}
                                        className="p-2 items-center"
                                        disabled={item.status < 5}
                                    >
                                        <MaterialIcons
                                            name="delete"
                                            size={25}
                                            color={
                                                item.status >= 5
                                                    ? "#8f2d11"
                                                    : "#b0b0b0"
                                            }
                                        />
                                    </TouchableOpacity>
                                </View>
                            )}
                        />
                    ) : (
                        <Text className="text-gray-600 text-center">
                            No translations available
                        </Text>
                    )}

                    {/* Button to Close the Modal */}
                    <TouchableOpacity
                        onPress={onClose}
                        className="flex-row justify-center px-4 py-1 mt-4 rounded-lg bg-white"
                        style={{
                            shadowColor: "#000",
                            shadowOffset: { width: 0, height: 4 },
                            shadowOpacity: 0.3,
                            shadowRadius: 4,
                            elevation: 5,
                        }}
                    >
                        <Text className="text-black text-base font-semibold">
                            CLOSE
                        </Text>
                    </TouchableOpacity>
                </View>
            </View>
        </Modal>
    );
}
