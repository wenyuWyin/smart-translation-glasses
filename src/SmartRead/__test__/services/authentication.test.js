import { handleLogin } from "../../app/services/authService";
import auth from "@react-native-firebase/auth";

// Mock Firebase authentication
const mockSignInWithEmailAndPassword = jest.fn();

// Mock Firebase authentication to use the shared mock function
jest.mock("@react-native-firebase/auth", () => ({
    __esModule: true,
    default: () => ({
        signInWithEmailAndPassword: mockSignInWithEmailAndPassword,
    }),
}));

describe("handleLogin", () => {
    var mockAuth;

    beforeEach(() => {
        jest.clearAllMocks();
        mockAuth = auth();
    });

    test("successful login", async () => {
        mockAuth.signInWithEmailAndPassword.mockResolvedValue({
            user: { uid: "12345" },
        });

        const result = await handleLogin("test@example.com", "password123");

        expect(result).toEqual({ status: 1, message: "Log in successful!" });
        expect(mockAuth.signInWithEmailAndPassword).toHaveBeenCalledWith(
            "test@example.com",
            "password123"
        );
    });

    test("invalid email format", async () => {
        mockAuth.signInWithEmailAndPassword.mockRejectedValue({
            code: "auth/invalid-email",
        });

        const result = await handleLogin("invalid-email", "password123");

        expect(result).toEqual({ status: 0, message: "Invalid email format." });
    });

    test("invalid credentials", async () => {
        mockAuth.signInWithEmailAndPassword.mockRejectedValue({
            code: "auth/invalid-credential",
        });

        const result = await handleLogin("test@example.com", "wrongpassword");

        expect(result).toEqual({
            status: 0,
            message: "Email not found or invalid password.",
        });
    });

    test("unexpected error", async () => {
        mockAuth.signInWithEmailAndPassword.mockRejectedValue(
            new Error("Network error")
        );

        const result = await handleLogin("test@example.com", "password123");

        expect(result.status).toBe(0);
        expect(result.message).toContain("Error: Network error");
    });
});
