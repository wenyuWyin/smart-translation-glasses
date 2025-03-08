import React, { useState, useContext, useEffect, useRef } from "react";
import { View, Text, TouchableOpacity, Alert } from "react-native";

import Ionicon from "react-native-vector-icons/Ionicons";
import FontAwesomeIcon from "react-native-vector-icons/FontAwesome6";
import MaterialCommunityIcon from "react-native-vector-icons/MaterialCommunityIcons";
import MaterialIcons from "react-native-vector-icons/MaterialIcons";
import { GestureHandlerRootView } from "react-native-gesture-handler";

import { SetupContext } from "../contexts/setupContext";
import { TranslationContext } from "../contexts/translationContext";
import convertStateToMessage from "../services/imageProcessState";
import TranslationResult from "../components/translationResult";
import TranslationHelpModal from "../components/translationHelpModal";
import ResultListModal from "../components/ResultListModal";

const ResultScreen = () => {
    console.log("Result Page Rendered");

    const MAX_ESP32_TEMP = 150;

    const previousAlertState = useRef(null);

    const { langPrefDone, deviceConnected, appConnected, temp, battery } =
        useContext(SetupContext);
    const {
        translationList,
        setTranslationList,
        translationIndex,
        setTranslationIndex,
    } = useContext(TranslationContext);

    const [showHelp, setShowHelp] = useState(false);
    const [showResultList, setShowResultList] = useState(false);

    const [translationResultSize, setTranslationResultSize] = useState({
        width: 0,
        height: 0,
    });

    const ready = langPrefDone && deviceConnected && appConnected;

    // Convert a temperature string to an icon name
    const convertToTemperatureIcon = (input) => {
        const number = Math.round(parseFloat(input));

        if (number && number > (MAX_ESP32_TEMP * 4) / 5) {
            return "temperature-high";
        } else if (number && number > (MAX_ESP32_TEMP * 3) / 4) {
            return "temperature-full";
        } else if (number && number > (MAX_ESP32_TEMP * 2) / 4) {
            return "temperature-three-quarters";
        } else if (number && number > (MAX_ESP32_TEMP * 1) / 4) {
            return "temperature-half";
        } else {
            return "temperature-quarter";
        }
    };

    // Convert a battery string to an icon name
    const convertToBatteryIcon = (input) => {
        const number = Math.round(parseFloat(input));

        if (number && number > 10) {
            return `battery-${Math.floor(number / 10) * 10}`;
        } else if (number && number <= 10) {
            return "battery-alert-variant-outline";
        } else {
            return "battery";
        }
    };

    useEffect(() => {
        if (temp < 30 && deviceConnected && appConnected) {
            if (previousAlertState.current !== "low") {
                Alert.alert("Warning", "Device temperature too low!");
                previousAlertState.current = "low";
            }
        } else if (temp > 80 && deviceConnected && appConnected) {
            if (previousAlertState.current !== "high") {
                Alert.alert("Warning", "Device temperature too high!");
                previousAlertState.current = "high";
            }
        } else {
            previousAlertState.current = null; // Reset when temp is normal
        }
    }, [temp]);

    // Switch to the next translation item
    const handleNext = () => {
        setTranslationIndex((prevIndex) =>
            prevIndex < translationList.length - 1 ? prevIndex + 1 : prevIndex
        );
    };

    // Switch to the previous translation item
    const handlePrevious = () => {
        setTranslationIndex((prevIndex) =>
            prevIndex > 0 ? prevIndex - 1 : prevIndex
        );
    };

    // Remove the current translation item
    const handleRemove = () => {
        setTranslationList((prev) => {
            const updated = [...prev];
            updated.splice(translationIndex, 1); // Remove the item

            var newIndex = translationIndex;

            if (updated.length === 0) {
                newIndex = 0; // Reset if empty
            } else if (translationIndex >= updated.length) {
                newIndex = updated.length - 1; // Move to the previous item if at the end
            }

            setTranslationIndex(newIndex);
            return updated;
        });
    };

    return (
        <View className="flex-1 bg-blue-100 h-[100%] items-center justify-center">
            {/* Status bar for device temperature, remaining battery, and internet connection status */}
            <View className="absolute top-0 bg-blue-900 h-[8%] w-full flex-row items-center justify-between px-[4%]">
                {/* Device temperature and battery */}
                {appConnected && deviceConnected && (
                    <View className="flex-row">
                        <View className="flex-row">
                            <FontAwesomeIcon
                                name={convertToTemperatureIcon(temp)}
                                size={20}
                                color="white"
                                className="mr-2"
                            />
                            <Text className="text-white mr-3">
                                {temp ? `${temp}°C` : "..."}
                            </Text>
                        </View>

                        <View className="flex-row">
                            <MaterialCommunityIcon
                                name={`${convertToBatteryIcon(battery)}`}
                                size={20}
                                color="white"
                                className="mr-1"
                            />
                            <Text className="text-white">
                                {battery ? `${battery}%` : "..."}
                            </Text>
                        </View>
                    </View>
                )}

                {/* Device internet connectivity status */}
                <View className="flex-row">
                    <MaterialCommunityIcon
                        name={deviceConnected ? "wifi" : "wifi-alert"}
                        size={20}
                        color="white"
                        className="mr-2"
                    />
                    <Text className="text-white">
                        {deviceConnected ? "Connected" : "Disconnected"}
                    </Text>
                </View>
            </View>

            {/* Steps to take before receiving translation results */}
            {!ready && (
                <View className="flex-col items-start">
                    <View className="flex-row items-center mb-4">
                        <Text className="text-lg font-bold mr-2">Step 1</Text>
                        <Ionicon
                            name={
                                langPrefDone
                                    ? "checkmark-circle"
                                    : "close-circle"
                            }
                            size={20}
                            className="mr-2"
                            color={langPrefDone ? "#02b34b" : "#a1061e"}
                        />
                        <Text className="text-lg font-medium">
                            Select language preference
                        </Text>
                    </View>
                    <View className="flex-row items-baseline mb-4">
                        <Text className="text-lg font-bold mr-2">Step 2</Text>
                        <Ionicon
                            name={
                                deviceConnected
                                    ? "checkmark-circle"
                                    : "close-circle"
                            }
                            size={20}
                            className="mr-2 pt-[4]"
                            color={deviceConnected ? "#02b34b" : "#a1061e"}
                        />
                        <Text className="text-lg font-medium max-w-[70%]">
                            Connect your camera to a network
                        </Text>
                    </View>
                    <View className="flex-row items-baseline mb-4">
                        <Text className="text-lg font-bold mr-2">Step 3</Text>
                        <Ionicon
                            name={
                                appConnected
                                    ? "checkmark-circle"
                                    : "close-circle"
                            }
                            size={20}
                            className="mr-2 pt-[4]"
                            color={appConnected ? "#02b34b" : "#a1061e"}
                        />
                        <Text className="text-lg font-medium max-w-[70%]">
                            Connect your phone to an available network
                        </Text>
                    </View>
                </View>
            )}

            {/* Translation Result Display */}
            {ready && (
                <View className="flex-1 flex-col items-center align-top h-[92%] w-full top-[8%]">
                    <View className="absolute top-[4%] flex-row justify-center w-[90%] mt-6 ">
                        {/* Button to Open the Translation Result List Modal */}
                        {translationList.length > 0 && (
                            <TouchableOpacity
                                onPress={() => {
                                    setShowResultList(true);
                                }}
                                className="flex-row items-center"
                            >
                                <View className="flex-row items-center mx-4">
                                    <MaterialCommunityIcon
                                        name="format-list-bulleted"
                                        size={22}
                                        className="mr-2"
                                    />
                                </View>
                            </TouchableOpacity>
                        )}
                        {/* Translation Status Message */}
                        <View className="flex-row justify-center text-center w-[80%]">
                            <Text className="text-lg font-bold">
                                {convertStateToMessage(
                                    translationList[translationIndex]?.status ??
                                        1
                                )}
                            </Text>
                        </View>
                    </View>
                    {/* Translation Result and Relevant Controls */}
                    {translationList[translationIndex]?.image && (
                        <View
                            className="absolute top-[10%] flex-col w-[90%] h-[76%] items-center justify-center rounded-xl"
                            onLayout={(event) => {
                                const { width, height } =
                                    event.nativeEvent.layout;
                                setTranslationResultSize({ width, height });
                                console.log(`${width} - ${height}`);
                            }}
                        >
                            <TranslationResult
                                imageUri={
                                    translationList[translationIndex].image
                                }
                                result={
                                    translationList[translationIndex].result ||
                                    {}
                                }
                                containerSize={translationResultSize}
                            />
                            {/* Panel for Translation Result Navigation Buttons */}
                            <View className="flex-row justify-between">
                                {/* Previous Button */}
                                <TouchableOpacity
                                    onPress={handlePrevious}
                                    className="flex-row items-center"
                                    disabled={
                                        translationIndex <= 0
                                    }
                                >
                                    <View className="flex-row items-center mx-4">
                                        <MaterialIcons
                                            name="navigate-before"
                                            size={22}
                                            className="p-2"
                                            color={
                                                translationIndex > 0
                                                    ? "#000000"
                                                    : "#b0b0b0"
                                            }
                                        />
                                    </View>
                                </TouchableOpacity>
                                {/* Remove Button */}
                                <TouchableOpacity
                                    onPress={handleRemove}
                                    className="flex-row items-center"
                                    disabled={
                                        translationList[translationIndex]
                                            .status < 4
                                    }
                                >
                                    <View className="flex-row items-center mx-4">
                                        <MaterialIcons
                                            name="delete"
                                            size={22}
                                            className="p-2"
                                            color={
                                                translationList[
                                                    translationIndex
                                                ].status >= 5
                                                    ? "#8f2d11"
                                                    : "#b0b0b0"
                                            }
                                        />
                                    </View>
                                </TouchableOpacity>
                                {/* Next Button */}
                                <TouchableOpacity
                                    onPress={handleNext}
                                    className="flex-row items-center"
                                    disabled={translationIndex >= translationList.length - 1}
                                >
                                    <View className="flex-row items-center mx-4">
                                        <MaterialIcons
                                            name="navigate-next"
                                            size={22}
                                            className="p-2"
                                            color={
                                                translationIndex < translationList.length - 1
                                                    ? "#000000"
                                                    : "#b0b0b0"
                                            }
                                        />
                                    </View>
                                </TouchableOpacity>
                            </View>
                        </View>
                    )}
                </View>
            )}

            {/* Help Icon */}
            {ready && (
                <TouchableOpacity
                    onPress={() => {
                        setShowHelp(true);
                    }}
                    className="absolute bottom-5 right-3 flex-row items-center"
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

            {ready && (
                <View className="absolute top-[20%] left-[5%] w-[90%] h-[60%] flex-col justify-center items-center">
                    <ResultListModal
                        visible={showResultList}
                        onClose={() => {
                            setShowResultList(false);
                        }}
                    />
                </View>
            )}

            {/* Add the gesture handler root view such that the modal can work with TranslationResult's gesture detection */}
            <GestureHandlerRootView style={{ width: "1%", height: "1%" }}>
                <TranslationHelpModal
                    visible={showHelp}
                    onClose={() => setShowHelp(false)}
                />
            </GestureHandlerRootView>
        </View>
    );
};

export default ResultScreen;
