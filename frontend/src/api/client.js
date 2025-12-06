import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const checkHealth = async () => {
    try {
        const response = await axios.get(`${API_URL}/health`);
        return response.data;
    } catch (error) {
        console.error("Health check failed:", error);
        return null;
    }
};

export const sendMessage = async (message) => {
    try {
        const response = await axios.post(`${API_URL}/chat`, { message });
        return response.data;
    } catch (error) {
        console.error("Chat request failed:", error);
        throw error;
    }
};
