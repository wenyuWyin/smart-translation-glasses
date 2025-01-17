import React, { useState, useEffect } from "react";
import {
    View,
    Text,
    Image,
    Dimensions,
    TouchableWithoutFeedback,
} from "react-native";

const TranslationResult = ({ imageUri, result }) => {
    const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
    const [imageRatio, setImageRatio] = useState(1);
    const [blurBackground, setBlurBackground] = useState(false);

    const window_size = Dimensions.get("window");

    useEffect(() => {
        const uri = `data:image/jpeg;base64,${imageUri}`;

        Image.getSize(
            uri,
            (width, height) => {
                setDimensions({ width, height });
                setImageRatio((window_size.width * 0.9) / width);
            },
            (error) => {
                console.error("Failed to get image size:", error);
            }
        );
    }, [imageUri]);

    return (
        <View className="flex-1 justify-center">
            <TouchableWithoutFeedback
                onPressIn={() => setBlurBackground(true)}
                onPressOut={() => setBlurBackground(false)}
            >
                <View className="absolute justify-center items-center mx-3">
                    <Image
                        source={{ uri: `data:image/jpeg;base64,${imageUri}` }}
                        style={{
                            width: dimensions.width * imageRatio,
                            height: dimensions.height * imageRatio,
                        }}
                        className="z-1"
                    />

                    {Object.entries(result).map(([rect, trans_result]) => {
                        const numbers = rect.match(/\d+/g).map(Number);
                        const [x1, x2, y1, y2] = numbers;

                        const left = x1 * imageRatio;
                        const top = y1 * imageRatio;
                        const rectWidth = (x2 - x1) * imageRatio;
                        const rectHeight = (y2 - y1) * imageRatio;

                        return (
                            <View
                                key={rect}
                                className={`absolute`}
                                style={{ left: left, top: top }}
                            >
                                <Text
                                    className={`${
                                        !blurBackground && "bg-gray-200"
                                    } text-blue-800`}
                                    style={{
                                        width: rectWidth,
                                        height: rectHeight * 1.2,
                                    }}
                                    adjustsFontSizeToFit
                                >
                                    {!blurBackground && trans_result.trn_text}
                                </Text>
                            </View>
                        );
                    })}
                </View>
            </TouchableWithoutFeedback>
        </View>
    );
};

export default TranslationResult;
