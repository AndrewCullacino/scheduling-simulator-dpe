"use client";

import React, { useEffect, useState } from 'react';
import { api, AlgorithmInfo, ScenarioInfo, SimulationRequest, TaskInput } from '../lib/api';
import TaskBuilder from './TaskBuilder';

interface SimulationFormProps {
    onRun: (data: SimulationRequest) => void;
    loading: boolean;
}

const SimulationForm: React.FC<SimulationFormProps> = ({ onRun, loading }) => {
    const [algorithms, setAlgorithms] = useState<AlgorithmInfo[]>([]);
    const [scenarios, setScenarios] = useState<ScenarioInfo[]>([]);

    const [selectedAlgo, setSelectedAlgo] = useState<string>('');
    const [selectedScenario, setSelectedScenario] = useState<string>('');
    const [numMachines, setNumMachines] = useState<number>(2);
    const [alpha, setAlpha] = useState<number>(0.7);

    // Custom Tasks State
    const [customTasks, setCustomTasks] = useState<TaskInput[]>([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [algosRes, scenariosRes] = await Promise.all([
                    api.getAlgorithms(),
                    api.getScenarios()
                ]);
                setAlgorithms(algosRes);

                // Add "Custom" option to scenarios
                const customScenario: ScenarioInfo = {
                    id: 'custom',
                    name: 'Custom Scenario',
                    description: 'Define your own tasks manually or import from JSON',
                    num_machines: 2,
                    tasks: []
                };

                setScenarios([customScenario, ...scenariosRes]);

                if (algosRes.length > 0) setSelectedAlgo(algosRes[0].id);
                // Default to first real scenario if available
                if (scenariosRes.length > 0) {
                    setSelectedScenario(scenariosRes[0].id);
                    setNumMachines(scenariosRes[0].num_machines);
                } else {
                    setSelectedScenario('custom');
                }
            } catch (err) {
                console.error("Failed to fetch data", err);
            }
        };
        fetchData();
    }, []);

    const handleScenarioChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const scenarioId = e.target.value;
        setSelectedScenario(scenarioId);
        const scenario = scenarios.find(s => s.id === scenarioId);
        if (scenario && scenarioId !== 'custom') {
            setNumMachines(scenario.num_machines);
        }
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        let tasksToRun: TaskInput[] = [];

        if (selectedScenario === 'custom') {
            if (customTasks.length === 0) {
                alert("Please add at least one task for the custom scenario.");
                return;
            }
            tasksToRun = customTasks;
        } else {
            const scenario = scenarios.find(s => s.id === selectedScenario);
            if (!scenario) return;
            tasksToRun = scenario.tasks;
        }

        onRun({
            algorithm: selectedAlgo,
            num_machines: numMachines,
            tasks: tasksToRun,
            alpha: alpha
        });
    };

    return (
        <div className="space-y-6">
            <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl border border-gray-200 shadow-xl space-y-4">
                <h2 className="text-xl font-bold mb-4 text-gray-800">Configuration</h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Algorithm</label>
                        <select
                            value={selectedAlgo}
                            onChange={(e) => setSelectedAlgo(e.target.value)}
                            className="mt-1 block w-full rounded-lg bg-gray-50 border border-gray-300 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2.5"
                        >
                            {algorithms.map(algo => (
                                <option key={algo.id} value={algo.id}>{algo.name}</option>
                            ))}
                        </select>
                        <p className="text-xs text-gray-500 mt-1">
                            {algorithms.find(a => a.id === selectedAlgo)?.description}
                        </p>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700">Scenario</label>
                        <select
                            value={selectedScenario}
                            onChange={handleScenarioChange}
                            className="mt-1 block w-full rounded-lg bg-gray-50 border border-gray-300 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2.5"
                        >
                            {scenarios.map(s => (
                                <option key={s.id} value={s.id}>{s.name}</option>
                            ))}
                        </select>
                        <p className="text-xs text-gray-500 mt-1">
                            {scenarios.find(s => s.id === selectedScenario)?.description}
                        </p>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Number of Machines</label>
                        <input
                            type="number"
                            min="1"
                            max="10"
                            value={numMachines}
                            onChange={(e) => setNumMachines(parseInt(e.target.value))}
                            className="mt-1 block w-full rounded-lg bg-gray-50 border border-gray-300 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2.5"
                        />
                    </div>

                    {selectedAlgo.includes('DPE') && (
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Alpha (DPE Threshold)</label>
                            <input
                                type="number"
                                min="0"
                                max="1"
                                step="0.1"
                                value={alpha}
                                onChange={(e) => setAlpha(parseFloat(e.target.value))}
                                className="mt-1 block w-full rounded-lg bg-gray-50 border border-gray-300 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2.5"
                            />
                        </div>
                    )}
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-bold text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-[1.02]"
                >
                    {loading ? 'Running Simulation...' : 'Run Simulation'}
                </button>
            </form>

            {selectedScenario === 'custom' && (
                <TaskBuilder tasks={customTasks} setTasks={setCustomTasks} />
            )}
        </div>
    );
};

export default SimulationForm;
