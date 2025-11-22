import React, { useEffect, useState } from 'react';
import { api, AlgorithmInfo, ScenarioInfo, SimulationRequest } from '../lib/api';

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

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [algosRes, scenariosRes] = await Promise.all([
                    api.getAlgorithms(),
                    api.getScenarios()
                ]);
                setAlgorithms(algosRes);
                setScenarios(scenariosRes);
                if (algosRes.length > 0) setSelectedAlgo(algosRes[0].id);
                if (scenariosRes.length > 0) {
                    setSelectedScenario(scenariosRes[0].id);
                    setNumMachines(scenariosRes[0].num_machines);
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
        if (scenario) {
            setNumMachines(scenario.num_machines);
        }
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        const scenario = scenarios.find(s => s.id === selectedScenario);
        if (!scenario) return;

        onRun({
            algorithm: selectedAlgo,
            num_machines: numMachines,
            tasks: scenario.tasks,
            alpha: alpha
        });
    };

    return (
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow space-y-4">
            <h2 className="text-xl font-bold mb-4">Configuration</h2>

            <div>
                <label className="block text-sm font-medium text-gray-700">Algorithm</label>
                <select
                    value={selectedAlgo}
                    onChange={(e) => setSelectedAlgo(e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
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
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                >
                    {scenarios.map(s => (
                        <option key={s.id} value={s.id}>{s.name}</option>
                    ))}
                </select>
                <p className="text-xs text-gray-500 mt-1">
                    {scenarios.find(s => s.id === selectedScenario)?.description}
                </p>
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700">Number of Machines</label>
                <input
                    type="number"
                    min="1"
                    max="10"
                    value={numMachines}
                    onChange={(e) => setNumMachines(parseInt(e.target.value))}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
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
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                    />
                </div>
            )}

            <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-gray-400"
            >
                {loading ? 'Running...' : 'Run Simulation'}
            </button>
        </form>
    );
};

export default SimulationForm;
