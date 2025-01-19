import auth from "@react-native-firebase/auth";

export const handleLogin = async (email, password) => {
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

export const handleRegister = async (username, email, password) => {
    var status = 1;
    var message = "";

    var userCredential;
    var uid;

    try {
        // Use firebase authentication to create a user
        userCredential = await auth().createUserWithEmailAndPassword(
            email,
            password
        );
        uid = userCredential.user.uid;
    } catch (error) {
        status = 0;
        if (error.code === "auth/invalid-email") {
            message = "Invalid email format.";
        } else if (error.code === "auth/weak-password") {
            message = "Password has to be more than 6 characters.";
        } else if (error.code === "auth/email-already-in-use") {
            message = "Email already in use.";
        } else {
            message = `Error: ${error.message}`;
        }

        return { status: status, message: message };
    }

    // If sign up successful, connect to backend to create a database for the user
    if (uid) {
        try {
            const response = await fetch(
                process.env.EXPO_PUBLIC_SERVER_IP_ADDRESS + "/signup",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        uid,
                        username,
                    }),
                }
            );

            if (!response.ok) {
                status = 0;
                message = "Signed up failed. Please try again later.";
            } else {
                message = "Sign up successful";
            }
        } catch (error) {
            status = 0;
            message = `Signed up failed: ${error.message}`;
            console.log(error);
        }
    }

    if (status) {
        const loginResponse = await handleLogin(email, password);

        if (loginResponse.status === 1) {
            console.log("Log in successful using Firebase!");
        } else {
            status = 0;
            message = `Cannot login with the username and email: ${loginResponse.message}`
            Alert.alert("Error", loginResponse.message);
        }
    
    }
    
    return { status: status, message: message };
};
