import axios from 'axios';
import type { GenerateQuestionsRequest, GenerateQuestionsResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000';

export const generateQuestions = async (request: GenerateQuestionsRequest): Promise<GenerateQuestionsResponse> => {
    try {
        const response = await axios.post<GenerateQuestionsResponse>(
            `${API_BASE_URL}/generate`,
            request
        );
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            throw new Error(error.response?.data?.detail || 'Failed to generate questions');
        }
        throw error;
    }
};
