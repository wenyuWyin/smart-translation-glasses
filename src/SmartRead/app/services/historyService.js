export default fetchTranslationHistory = async (uid) => {
    try {
        const response = await fetch(
            process.env.EXPO_PUBLIC_SERVER_IP_ADDRESS + `/history?uid=${uid}`,
            {
                method: "GET",
            }
        );
        const data = await response.json();
        const history = data.data;

        return history;
    } catch (error) {
        throw Error(error);
    }
};
