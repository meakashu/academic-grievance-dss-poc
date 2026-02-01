/**
 * API Service for Academic Grievance DSS
 * Handles all HTTP requests to the backend
 */
import axios, { AxiosInstance, AxiosError } from 'axios';
import {
    GrievanceCreate,
    GrievanceSubmissionResponse,
    Grievance,
    Decision,
    RuleTrace,
    APIResponse
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class APIService {
    private client: AxiosInstance;

    constructor() {
        this.client = axios.create({
            baseURL: API_BASE_URL,
            timeout: 30000, // 30 seconds
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Request interceptor
        this.client.interceptors.request.use(
            (config) => {
                console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
                return config;
            },
            (error) => {
                return Promise.reject(error);
            }
        );

        // Response interceptor
        this.client.interceptors.response.use(
            (response) => {
                console.log(`API Response: ${response.status} ${response.config.url}`);
                return response;
            },
            (error: AxiosError) => {
                console.error('API Error:', error.message);
                if (error.response) {
                    console.error('Response data:', error.response.data);
                }
                return Promise.reject(error);
            }
        );
    }

    /**
     * Submit a new grievance
     */
    async submitGrievance(grievance: GrievanceCreate): Promise<GrievanceSubmissionResponse> {
        try {
            const response = await this.client.post<GrievanceSubmissionResponse>(
                '/api/grievances',
                grievance
            );
            return response.data;
        } catch (error) {
            throw this.handleError(error);
        }
    }

    /**
     * Get grievance by ID
     */
    async getGrievance(grievanceId: string): Promise<Grievance> {
        try {
            const response = await this.client.get<APIResponse<Grievance>>(
                `/api/grievances/${grievanceId}`
            );
            return response.data.data!;
        } catch (error) {
            throw this.handleError(error);
        }
    }

    /**
     * Get all grievances for a student
     */
    async getStudentGrievances(studentId: string): Promise<Grievance[]> {
        try {
            const response = await this.client.get<APIResponse<Grievance[]>>(
                `/api/grievances/student/${studentId}`
            );
            return response.data.data || [];
        } catch (error) {
            throw this.handleError(error);
        }
    }

    /**
     * Get decision by ID
     */
    async getDecision(decisionId: string): Promise<Decision> {
        try {
            const response = await this.client.get<APIResponse<Decision>>(
                `/api/decisions/${decisionId}`
            );
            return response.data.data!;
        } catch (error) {
            throw this.handleError(error);
        }
    }

    /**
     * Get decision for a grievance
     */
    async getDecisionByGrievance(grievanceId: string): Promise<Decision> {
        try {
            const response = await this.client.get<APIResponse<Decision>>(
                `/api/decisions/grievance/${grievanceId}`
            );
            return response.data.data!;
        } catch (error) {
            throw this.handleError(error);
        }
    }

    /**
     * Get rule trace by ID
     */
    async getRuleTrace(traceId: string): Promise<RuleTrace> {
        try {
            const response = await this.client.get<APIResponse<RuleTrace>>(
                `/api/trace/${traceId}`
            );
            return response.data.data!;
        } catch (error) {
            throw this.handleError(error);
        }
    }

    /**
     * Get rule trace for a grievance
     */
    async getRuleTraceByGrievance(grievanceId: string): Promise<RuleTrace & { summary?: any }> {
        try {
            const response = await this.client.get<APIResponse<RuleTrace & { summary?: any }>>(
                `/api/trace/grievance/${grievanceId}`
            );
            return response.data.data!;
        } catch (error) {
            throw this.handleError(error);
        }
    }

    /**
     * Get fairness metrics
     */
    async getFairnessMetrics(): Promise<any> {
        try {
            const response = await this.client.get<APIResponse>(
                '/api/fairness/consistency'
            );
            return response.data.data;
        } catch (error) {
            throw this.handleError(error);
        }
    }

    /**
     * Health check
     */
    async healthCheck(): Promise<any> {
        try {
            const response = await this.client.get('/health');
            return response.data;
        } catch (error) {
            throw this.handleError(error);
        }
    }

    /**
     * Handle API errors
     */
    private handleError(error: any): Error {
        if (axios.isAxiosError(error)) {
            const axiosError = error as AxiosError<any>;

            if (axiosError.response) {
                // Server responded with error
                const message = axiosError.response.data?.detail
                    || axiosError.response.data?.error
                    || axiosError.response.data?.message
                    || `Server error: ${axiosError.response.status}`;
                return new Error(message);
            } else if (axiosError.request) {
                // Request made but no response
                return new Error('No response from server. Please check your connection.');
            }
        }

        return new Error('An unexpected error occurred');
    }
}

// Export singleton instance
export const apiService = new APIService();
export default apiService;
