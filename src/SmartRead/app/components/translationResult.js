import React, { useEffect, useState } from "react";
import { View, Text, Image, Dimensions } from "react-native";
import {
    Gesture,
    GestureDetector,
    GestureHandlerRootView,
} from "react-native-gesture-handler";
import Animated, {
    useSharedValue,
    useAnimatedStyle,
    withSpring,
    runOnJS,
} from "react-native-reanimated";

const TranslationResult = ({ imageUri, result }) => {
    const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
    const [imageRatio, setImageRatio] = useState(1);
    const [hideBackground, setHideBackground] = useState(false);
    const window_size = Dimensions.get("window");

    // Shared values for zoom and translation
    const scale = useSharedValue(1);
    const translateX = useSharedValue(0);
    const translateY = useSharedValue(0);
    // Record the position of previous translation
    const translateBeginX = useSharedValue(0);
    const translateBeginY = useSharedValue(0);

    // Get image's dimension
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

    // Safe state update with `runOnJS`
    const toggleHideBackground = () => {
        console.log("single tap deteced");
        setHideBackground((prev) => !prev);
    };

    // Single tap gesture - toggle background
    const singleTapGesture = Gesture.Tap().onEnd(() => {
        runOnJS(toggleHideBackground)();
    });

    // Double tap gesture - zoom-in/zoom-out
    const doubleTapGesture = Gesture.Tap()
        .numberOfTaps(2)
        .onEnd(() => {
            console.log("double tap deteced");
            // Use withSpring for a spring animation
            if (scale.value === 1) {
                scale.value = withSpring(2); // Enlarge image
            } else {
                scale.value = withSpring(1); // Shrink back to normal
                translateBeginX.value = 0; // Reset translations
                translateBeginY.value = 0;
                translateX.value = 0;
                translateY.value = 0;
            }
        });

    // Pan gesture - move the image
    const panGesture = Gesture.Pan()
        .onBegin(() => {
            // Recall the location of the previous pan gesture
            translateBeginX.value = translateX.value;
            translateBeginY.value = translateY.value;
        })
        .onUpdate((event) => {
            const newTranslateX = translateBeginX.value + event.translationX;
            const newTranslateY = translateBeginY.value + event.translationY;

            // Restrict X translation within window width
            translateX.value = Math.min(
                Math.max(newTranslateX, -window_size.width * 0.5),
                window_size.width * 0.5
            );

            // Restrict Y translation
            translateY.value = Math.min(
                Math.max(newTranslateY, -window_size.height * 0.08),
                window_size.height * 0.08
            );
        })
        .onEnd(() => {
            translateX.value = translateX.value; // Keep the final position
            translateY.value = translateY.value; // Keep the final position
        });

    // Animated styles for the image and overlays
    const animatedStyle = useAnimatedStyle(() => {
        return {
            transform: [
                { translateX: translateX.value },
                { translateY: translateY.value },
                { scale: scale.value },
            ],
        };
    });

    return (
        // Use GestureHandlerRootView to detect gestures in a modal
        <GestureHandlerRootView className="flex-1">
            <GestureDetector
                gesture={Gesture.Exclusive(
                    panGesture,
                    doubleTapGesture,
                    singleTapGesture
                )}
            >
                <View className="flex-1 justify-center items-center">
                    <Animated.View
                        style={[
                            animatedStyle,
                            {
                                width: dimensions.width * imageRatio,
                                height: dimensions.height * imageRatio,
                                overflow: "hidden",
                            },
                        ]}
                    >
                        {/* Image */}
                        <Image
                            source={{
                                uri: `data:image/jpeg;base64,${imageUri}`,
                            }}
                            style={{
                                width: "100%",
                                height: "100%",
                            }}
                            resizeMode="contain"
                        />

                        {/* Translated Text Overlays */}
                        {Object.entries(result).map(([rect, trans_result]) => {
                            const numbers = rect.match(/\d+/g).map(Number);
                            const [x1, x2, y1, y2] = numbers;

                            const left = x1 * imageRatio;
                            const top = y1 * imageRatio;
                            const rectWidth = (x2 - x1) * imageRatio;
                            const rectHeight = (y2 - y1) * imageRatio;

                            const fontSize =
                                Math.max(rectWidth, rectHeight) / 5;

                            return (
                                <View
                                    key={rect}
                                    className={`absolute ${
                                        hideBackground && "bg-gray-200"
                                    }`}
                                    style={{
                                        left,
                                        top,
                                    }}
                                >
                                    <Text
                                        className="text-blue-800 text-center"
                                        style={{
                                            width: rectWidth,
                                            height: rectHeight,
                                            fontSize,
                                        }}
                                        adjustsFontSizeToFit
                                    >
                                        {hideBackground &&
                                            trans_result.trn_text}
                                    </Text>
                                </View>
                            );
                        })}
                    </Animated.View>
                </View>
            </GestureDetector>
        </GestureHandlerRootView>
    );
};

export default TranslationResult;
