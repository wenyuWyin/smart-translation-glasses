import React, { useState, useContext } from "react";
import { View, Text, TouchableOpacity } from "react-native";

import Ionicon from "react-native-vector-icons/Ionicons";
import FontAwesomeIcon from "react-native-vector-icons/FontAwesome6";
import MaterialCommunityIcon from "react-native-vector-icons/MaterialCommunityIcons";
import {
    GestureHandlerRootView,
} from "react-native-gesture-handler";

import { SetupContext } from "../contexts/setupContext";
import { TranslationContext } from "../contexts/translationContext";
import convertStateToMessage from "../services/imageProcessState";
import TranslationResult from "../components/translationResult";
import TranslationHelpModal from "../components/translationHelpModal";

const ResultScreen = () => {
    console.log("Result Page Rendered");

    const MAX_ESP32_TEMP = 150;

    const {
        langPrefDone,
        setLangPrefDone,
        deviceConnected,
        setDeviceConnected,
        appConnected,
        setAppConnected,
        temp,
        setTemp,
        battery,
        setBattery,
    } = useContext(SetupContext);
    const {
        trnStateCode,
        setTrnStateCode,
        trnImage,
        setTrnImage,
        trnResult,
        setTrnResult,
    } = useContext(TranslationContext);

    const [showHelp, setShowHelp] = useState(false);

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
            {!(langPrefDone && deviceConnected && appConnected) && (
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
            {langPrefDone && deviceConnected && appConnected && (
                <View className="flex-1 justify-center items-center h-[80%]">
                    <View className="absolute flex-row px-6 mt-2 top-12">
                        <Text className="text-lg font-bold">
                            {convertStateToMessage(trnStateCode)}
                        </Text>
                    </View>
                    {trnImage && (
                        <View className="flex-col w-[95%] h-[29%] rounded-xl">
                            <TranslationResult
                                imageUri={trnImage}
                                result={trnResult || {}}
                            />
                        </View>
                    )}
                </View>
            )}

            {/* Help Icon */}
            {langPrefDone && deviceConnected && appConnected && (
                <TouchableOpacity
                    onPress={() => {
                        console.log("pressed");
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
