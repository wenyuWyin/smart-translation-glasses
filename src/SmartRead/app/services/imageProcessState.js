stateMessageMapping = {
    1: "Waiting for an image.",
    2: "Image received. Analyzing in progress.",
    3: "Text extracted from the image. Translating in progress.",
    4: "Text translated. Please be patient while we preparing the result for you.",
    5: "Something goes wrong. Please take another image."
}

// Convert an image processing state to a message that will be displayed
export default convertStateToMessage = (state) => {
    if (state in stateMessageMapping) {
        return stateMessageMapping[state];
    } else {
        return "State not found.";
    }
}