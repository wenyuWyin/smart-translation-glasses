import React, { useContext } from "react";
import { View, Text } from "react-native";

import Ionicon from "react-native-vector-icons/Ionicons";

import { SetupContext } from "../contexts/setupContext";

const ResultScreen = () => {
    const { step1Done, setStep1Done, step2Done, setStep2Done } =
        useContext(SetupContext);

    return (
        <View className="flex-1 bg-blue-100 h-[100%] items-center justify-center">
            {!(step1Done && step2Done) && (
                <View className="flex-col items-start">
                    <View className="flex-row items-center mb-4">
                        <Text className="text-lg font-bold mr-2">Step 1</Text>
                        <Ionicon
                            name={
                                step1Done ? "checkmark-circle" : "close-circle"
                            }
                            size={20}
                            className="mr-2"
                            color={step1Done ? "#02b34b" : "#a1061e"}
                        />
                        <Text className="text-lg font-medium">
                            Select language preference
                        </Text>
                    </View>
                    <View className="flex-row items-center mb-4">
                        <Text className="text-lg font-bold mr-2">Step 2</Text>
                        <Ionicon
                            name={
                                step2Done ? "checkmark-circle" : "close-circle"
                            }
                            size={20}
                            className="mr-2"
                            color={step2Done ? "#02b34b" : "#a1061e"}
                        />
                        <Text className="text-lg font-medium">
                            Connect your camera to a network
                        </Text>
                    </View>
                </View>
            )}
        </View>
    );
};

export default ResultScreen;
