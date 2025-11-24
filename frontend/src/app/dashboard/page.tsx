"use client";

import React, { useState } from 'react';
import SimulationForm from '@/components/SimulationForm';
import GanttChart from '@/components/GanttChart';
import ComparisonTable, { SimulationRun } from '@/components/ComparisonTable';
import { api, SimulationRequest, SimulationResult } from '@/lib/api';
import { Activity, Clock, CheckCircle, AlertTriangle, Terminal, Trash2 } from 'lucide-react';

export default function Dashboard() {
    const [runs, setRuns] = useState<SimulationRun[]>([]);
    const [selectedRunId, setSelectedRunId] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleRunSimulation = async (data: SimulationRequest, meta: { algoName: string, scenarioName: string }) => {
        setLoading(true);
        setError(null);
        try {
            const res = await api.runSimulation(data);
            const newRun: SimulationRun = {
                id: Date.now().toString(),
                timestamp: Date.now(),
                algorithm: meta.algoName,
                scenario: meta.scenarioName,
                result: res
            };

            setRuns(prev => [...prev, newRun]);
            setSelectedRunId(newRun.id);
        } catch (err) {
            console.error(err);
            setError("Failed to run simulation. Please check backend connection.");
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteRun = (runId: string) => {
        setRuns(prev => prev.filter(r => r.id !== runId));
        if (selectedRunId === runId) {
            setSelectedRunId(null);
        }
    };

    const handleClearAll = () => {
        setRuns([]);
        setSelectedRunId(null);
    };

    const selectedRun = runs.find(r => r.id === selectedRunId) || (runs.length > 0 ? runs[runs.length - 1] : null);
    const result = selectedRun?.result;

    return (
        <div className="min-h-screen p-8 font-sans bg-gray-50">
            <header className="mb-10 text-center">
                <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 mb-2 tracking-tight">
                    Scheduling Simulator
                </h1>
                <p className="text-gray-500 text-lg">Professional Cloud & Real-Time Orchestration Engine</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
                {/* Left Panel: Configuration */}
                <div className="lg:col-span-1 space-y-6">
                    <SimulationForm onRun={handleRunSimulation} loading={loading} />

                    {error && (
                        <div className="p-4 bg-red-50 text-red-700 rounded-xl border border-red-200 flex items-center gap-3">
                            <AlertTriangle className="w-5 h-5" />
                            {error}
                        </div>
                    )}

                    {result && (
                        <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                            <h3 className="text-xl font-bold mb-6 flex items-center gap-2 text-gray-800">
                                <Activity className="w-5 h-5 text-green-500" />
                                Performance Metrics
                            </h3>
                            <div className="space-y-4">
                                <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                                    <span className="text-gray-600 flex items-center gap-2">
                                        <Clock className="w-4 h-4" /> Makespan
                                    </span>
                                    <span className="font-mono font-bold text-xl text-blue-600">{result.makespan.toFixed(1)}s</span>
                                </div>
                                <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                                    <span className="text-gray-600">Total Tasks</span>
                                    <span className="font-mono font-bold text-xl text-gray-800">{result.total_tasks}</span>
                                </div>

                                <div className="pt-4 border-t border-gray-100">
                                    <h4 className="font-medium text-sm text-gray-500 mb-3 uppercase tracking-wider">Success Rates</h4>
                                    <div className="space-y-3">
                                        <div className="flex justify-between items-center">
                                            <span className="text-sm text-red-500 font-medium">High Priority</span>
                                            <span className="font-bold text-green-600 bg-green-100 px-2 py-1 rounded text-sm">
                                                {result.high_priority_stats.met_deadline} / {result.high_priority_stats.total}
                                            </span>
                                        </div>
                                        <div className="w-full bg-gray-200 rounded-full h-1.5">
                                            <div
                                                className="bg-red-500 h-1.5 rounded-full transition-all duration-1000"
                                                style={{ width: `${(result.high_priority_stats.met_deadline / (result.high_priority_stats.total || 1)) * 100}%` }}
                                            />
                                        </div>

                                        <div className="flex justify-between items-center mt-2">
                                            <span className="text-sm text-blue-500 font-medium">Low Priority</span>
                                            <span className="font-bold text-green-600 bg-green-100 px-2 py-1 rounded text-sm">
                                                {result.low_priority_stats.met_deadline} / {result.low_priority_stats.total}
                                            </span>
                                        </div>
                                        <div className="w-full bg-gray-200 rounded-full h-1.5">
                                            <div
                                                className="bg-blue-500 h-1.5 rounded-full transition-all duration-1000"
                                                style={{ width: `${(result.low_priority_stats.met_deadline / (result.low_priority_stats.total || 1)) * 100}%` }}
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {/* Right Panel: Visualization */}
                <div className="lg:col-span-2 space-y-8">
                    {/* Comparison Table */}
                    {runs.length > 0 && (
                        <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200 overflow-hidden">
                            <div className="flex justify-between items-center mb-4">
                                <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                                    <Activity className="w-5 h-5 text-blue-500" />
                                    Simulation Comparison
                                </h3>
                                <button
                                    onClick={handleClearAll}
                                    className="text-sm text-red-500 hover:text-red-700 flex items-center gap-1 px-3 py-1 rounded-md hover:bg-red-50 transition-colors"
                                >
                                    <Trash2 className="w-4 h-4" /> Clear All
                                </button>
                            </div>
                            <ComparisonTable
                                runs={runs}
                                onSelect={setSelectedRunId}
                                selectedRunId={selectedRunId || (runs.length > 0 ? runs[runs.length - 1].id : null)}
                                onDelete={handleDeleteRun}
                            />
                        </div>
                    )}

                    {result ? (
                        <div className="bg-white p-1 rounded-xl overflow-hidden shadow-xl border border-gray-200">
                            <div className="p-4 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
                                <h3 className="font-bold text-gray-700">
                                    Visualization: <span className="text-blue-600">{selectedRun?.algorithm}</span> - {selectedRun?.scenario}
                                </h3>
                                <span className="text-xs text-gray-400">Run ID: {selectedRun?.id}</span>
                            </div>
                            <GanttChart result={result} />
                        </div>
                    ) : (
                        <div className="bg-white p-12 rounded-xl text-center text-gray-400 flex flex-col items-center justify-center h-64 border-dashed border-2 border-gray-200 shadow-sm">
                            <Activity className="w-12 h-12 mb-4 opacity-20" />
                            <p>Select a scenario and run simulation to visualize results.</p>
                        </div>
                    )}

                    {result && (
                        <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                            <h3 className="text-xl font-bold mb-4 text-gray-800 flex items-center gap-2">
                                <Terminal className="w-5 h-5 text-yellow-500" />
                                System Logs
                            </h3>
                            <div className="h-64 overflow-y-auto font-mono text-xs bg-gray-900 p-4 rounded-lg border border-gray-200 shadow-inner custom-scrollbar text-gray-300">
                                {result.logs.map((log, i) => (
                                    <div key={i} className="mb-1.5 border-b border-gray-800 pb-1.5 last:border-0 flex gap-3 hover:bg-white/5 p-1 rounded transition-colors">
                                        <span className="text-gray-500 min-w-[60px]">[{log.time.toFixed(1)}s]</span>
                                        <span className={`font-bold min-w-[80px] ${log.event === 'ARRIVAL' ? 'text-blue-400' :
                                            log.event === 'COMPLETION' ? 'text-green-400' :
                                                'text-yellow-400'
                                            }`}>
                                            {log.event}
                                        </span>
                                        <span className="text-gray-300">{log.message}</span>
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
