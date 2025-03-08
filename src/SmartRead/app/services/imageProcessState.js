import { ActivityIndicator } from "react-native";
import MaterialIcons from "react-native-vector-icons/MaterialIcons";

stateMessageMapping = {
    1: "Waiting for an image.",
    2: "Image queued. Waiting for processing.",
    3: "Image received. Analyzing in progress.",
    4: "Text extracted from the image. Translating in progress.",
    5: "Translation completed.",
    6: "Something goes wrong. Please take another image.",
};

// Convert an image processing state to a message that will be displayed
export default convertStateToMessage = (state) => {
    if (state in stateMessageMapping) {
        return stateMessageMapping[state];
    } else {
        return "State not found.";
    }
};

// Convert an image processing state to an icon
export const convertStateToIcon = (state) => {
    if (state === 2) {
        return <MaterialIcons name="hourglass-empty" size={25} color="black" />;
    } else if (state === 3 || state === 4) {
        return <ActivityIndicator size="small" color="#007AFF" />;
    } else if (state === 5) {
        return <MaterialIcons name="done" size={25} color="green" />;
    } else if (state === 6) {
        return (
            <MaterialIcons name="report-gmailerrorred" size={25} color="red" />
        );
    }
};
