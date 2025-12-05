import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const chatWithBot = async (question) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/chat`, { question });
        return response.data;
    } catch (error) {
        console.error("Error chatting with bot:", error);
        throw error;
    }
};

export const getGraphData = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/graph/sample`);
        return response.data;
    } catch (error) {
        console.error("Error fetching graph data:", error);
        throw error;
    }
};
