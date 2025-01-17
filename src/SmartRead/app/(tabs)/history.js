import React, { useState, useContext, useEffect } from "react";
import {
    View,
    Text,
    FlatList,
    ActivityIndicator,
    TouchableOpacity,
} from "react-native";

import TranslationResultModal from "../components/translationResultModal";
import fetchTranslationHistory from "../services/historyService";
import { UserContext } from "../contexts/userContext";

const HistoryScreen = () => {
    console.log("History Page Rendered");

    const { user, login, logout } = useContext(UserContext);

    const [modalVisible, setModalVisible] = useState(false);
    const [selectedItem, setSelectedItem] = useState(null);
    const [loadingHistory, setLoadingHistory] = useState(false);
    const [history, setHistory] = useState([]);

    // Fetch translation history when entering the page
    useEffect(() => {
        const fetchHistory = async () => {
            try {
                console.log("Fetching translation history...");
                setLoadingHistory(true);
                const fetchedHistory = await fetchTranslationHistory(
                    user.user_id
                );

                setHistory(fetchedHistory || []);
            } catch (error) {
                console.error("Error fetching translation history:", error);
            } finally {
                setLoadingHistory(false);
            }
        };

        fetchHistory();
    }, [user.user_id]);

    const getPreview = (result) => {
        const firstKey = Object.keys(result)[0]; // Get the first key (a tuple)
        const { org_text, trn_text } = result[firstKey];
        return {
            orgTextPreview: org_text.substring(0, 30), // Limit to 50 characters
            trnTextPreview: trn_text.substring(0, 30),
        };
    };

    const formatDateString = (dateString) => {
        const [year, month, day, hour, minute] = dateString.split("-");
        const date = new Date(`${year}-${month}-${day}T${hour}:${minute}`);

        const options = {
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        };

        return date.toLocaleString("en-US", options);
    };

    const renderItem = ({ item }) => {
        const { orgTextPreview, trnTextPreview } = getPreview(item.result);

        return (
            <TouchableOpacity onPress={() => openModal(item)}>
                <View className="border-b border-gray-300 p-4">
                    <Text className="font-bold text-lg">
                        {formatDateString(item.translate_time)}
                    </Text>

                    <Text className="mt-2 text-gray-500">
                        Original: {orgTextPreview}...
                    </Text>

                    <Text className="mt-1 text-blue-950">
                        Translated: {trnTextPreview}...
                    </Text>
                </View>
            </TouchableOpacity>
        );
    };

    const openModal = (item) => {
        setSelectedItem(item);
        setModalVisible(true);
    };

    const closeModal = () => {
        setModalVisible(false);
        setSelectedItem(null);
    };

    return loadingHistory ? (
        <View className="flex-1 justify-center items-center bg-blue-100 px-4">
            <Text className="text-lg">
                Loading translation history. This might take a while...
            </Text>
            <ActivityIndicator size="large" color="#ffffff" />
        </View>
    ) : (
        <View className="flex-1 justify-center items-center bg-blue-100 px-4">
            {selectedItem && (
                <TranslationResultModal
                    imageUri={selectedItem.image}
                    result={selectedItem.result}
                    modalVisible={modalVisible}
                    closeModal={closeModal}
                />
            )}
            <FlatList
                data={history}
                keyExtractor={(item, index) => index.toString()}
                renderItem={renderItem}
                className="p-4 bg-blue-100"
            />
        </View>
    );
};

export default HistoryScreen;
