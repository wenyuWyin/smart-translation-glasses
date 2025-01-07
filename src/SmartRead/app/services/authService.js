import auth from "@react-native-firebase/auth";

const handleLogin = async (email, password) => {
    var status = 1;
    var message = "";

    try {
        // Use firebase authentication to sign in
        const userCredential = await auth().signInWithEmailAndPassword(
            email,
            password
        );

        message = "Log in successful!";
    } catch (error) {
        status = 0;
        // Return different status messages for different errors
        if (error.code === "auth/invalid-email") {
            message = "Invalid email format.";
        } else if (error.code === "auth/invalid-credential") {
            message = "Email not found or invalid password.";
        } else {
            message = `Error: ${error.message}`;
        }
    }

    return { status: status, message: message };
};

const handleRegister = async () => {
    
}

export default handleLogin;
