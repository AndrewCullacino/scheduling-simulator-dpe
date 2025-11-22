"use client";

import React, { useState } from 'react';
import SimulationForm from '@/components/SimulationForm';
import GanttChart from '@/components/GanttChart';
import { api, SimulationRequest, SimulationResult } from '@/lib/api';

export default function Dashboard() {
    const [result, setResult] = useState<SimulationResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleRunSimulation = async (data: SimulationRequest) => {
        setLoading(true);
        setError(null);
        try {
            const res = await api.runSimulation(data);
            setResult(res);
        } catch (err) {
            console.error(err);
            setError("Failed to run simulation. Please check backend connection.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900">Scheduling Simulator Dashboard</h1>
                <p className="text-gray-600">Real-time scheduling algorithm visualization</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left Panel: Configuration */}
                <div className="lg:col-span-1">
                    <SimulationForm onRun={handleRunSimulation} loading={loading} />

                    {error && (
                        <div className="mt-4 p-4 bg-red-100 text-red-700 rounded-lg border border-red-200">
                            {error}
                        </div>
                    )}

                    {result && (
                        <div className="mt-8 bg-white p-6 rounded-lg shadow">
                            <h3 className="text-lg font-bold mb-4">Metrics</h3>
                            <div className="space-y-2">
                                <div className="flex justify-between">
                                    <span className="text-gray-600">Makespan:</span>
                                    <span className="font-mono font-bold">{result.makespan.toFixed(1)}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-gray-600">Total Tasks:</span>
                                    <span className="font-mono font-bold">{result.total_tasks}</span>
                                </div>
                                <div className="border-t pt-2 mt-2">
                                    <h4 className="font-medium text-sm text-gray-500 mb-1">High Priority</h4>
                                    <div className="flex justify-between text-sm">
                                        <span>Met Deadline:</span>
                                        <span className="font-bold text-green-600">
                                            {result.high_priority_stats.met_deadline} / {result.high_priority_stats.total}
                                        </span>
                                    </div>
                                </div>
                                <div className="border-t pt-2 mt-2">
                                    <h4 className="font-medium text-sm text-gray-500 mb-1">Low Priority</h4>
                                    <div className="flex justify-between text-sm">
                                        <span>Met Deadline:</span>
                                        <span className="font-bold text-green-600">
                                            {result.low_priority_stats.met_deadline} / {result.low_priority_stats.total}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {/* Right Panel: Visualization */}
                <div className="lg:col-span-2 space-y-8">
                    {result ? (
                        <GanttChart result={result} />
                    ) : (
                        <div className="bg-white p-12 rounded-lg shadow text-center text-gray-500">
                            Select a scenario and run simulation to see results.
                        </div>
                    )}

                    {result && (
                        <div className="bg-white p-6 rounded-lg shadow">
                            <h3 className="text-lg font-bold mb-4">Simulation Logs</h3>
                            <div className="h-64 overflow-y-auto font-mono text-xs bg-gray-50 p-4 rounded border">
                                {result.logs.map((log, i) => (
                                    <div key={i} className="mb-1 border-b border-gray-100 pb-1 last:border-0">
                                        <span className="text-gray-500 mr-2">[{log.time.toFixed(1)}]</span>
                                        <span className={`font-bold mr-2 ${log.event === 'ARRIVAL' ? 'text-blue-600' : log.event === 'COMPLETION' ? 'text-green-600' : 'text-yellow-600'}`}>
                                            {log.event}
                                        </span>
                                        <span>{log.message}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
