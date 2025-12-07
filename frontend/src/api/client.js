import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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
        const response = await axios.post(`${API_URL}/chat`, { message }, {
            timeout: 120000  // 120 seconds to handle cold start + AI processing
        });
        return response.data;
    } catch (error) {
        console.error("Chat request failed:", error);
        throw error;
    }
};
