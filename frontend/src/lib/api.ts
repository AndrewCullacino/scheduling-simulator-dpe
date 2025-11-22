import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export interface TaskInput {
    id: number;
    arrival_time: number;
    processing_time: number;
    priority: 'HIGH' | 'LOW';
    deadline: number;
}

export interface SimulationRequest {
    algorithm: string;
    num_machines: number;
    tasks: TaskInput[];
    alpha?: number;
}

export interface LogEntry {
    time: number;
    event: string;
    task_id?: number;
    machine_id?: number;
    message: string;
    completion_time?: number;
}

export interface TaskResult {
    id: number;
    priority: string;
    arrival_time: number;
    start_time: number | null;
    completion_time: number | null;
    deadline: number;
    meets_deadline: boolean;
}

export interface PriorityStats {
    total: number;
    met_deadline: number;
}

export interface SimulationResult {
    makespan: number;
    total_tasks: number;
    high_priority_stats: PriorityStats;
    low_priority_stats: PriorityStats;
    tasks: TaskResult[];
    logs: LogEntry[];
}

export interface AlgorithmInfo {
    id: string;
    name: string;
    description: string;
}

export interface ScenarioInfo {
    id: string;
    name: string;
    description: string;
    num_machines: number;
    tasks: TaskInput[];
}

export const api = {
    getAlgorithms: async () => {
        const response = await axios.get<AlgorithmInfo[]>(`${API_URL}/algorithms`);
        return response.data;
    },
    getScenarios: async () => {
        const response = await axios.get<ScenarioInfo[]>(`${API_URL}/scenarios`);
        return response.data;
    },
    runSimulation: async (data: SimulationRequest) => {
        const response = await axios.post<SimulationResult>(`${API_URL}/simulate`, data);
        return response.data;
    }
};
