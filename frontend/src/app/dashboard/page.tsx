"use client";

import React, { useState } from 'react';
import SimulationForm from '@/components/SimulationForm';
import GanttChart from '@/components/GanttChart';
import { api, SimulationRequest, SimulationResult } from '@/lib/api';
import { Activity, Clock, CheckCircle, AlertTriangle, Terminal } from 'lucide-react';

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
        <div className="min-h-screen p-8 font-sans">
            <header className="mb-10 text-center">
                <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400 mb-2 tracking-tight">
                    Scheduling Simulator
                </h1>
                <p className="text-gray-400 text-lg">Professional Cloud & Real-Time Orchestration Engine</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
                {/* Left Panel: Configuration */}
                <div className="lg:col-span-1 space-y-6">
                    <SimulationForm onRun={handleRunSimulation} loading={loading} />

                    {error && (
                        <div className="p-4 bg-red-500/20 text-red-200 rounded-xl border border-red-500/30 flex items-center gap-3">
                            <AlertTriangle className="w-5 h-5" />
                            {error}
                        </div>
                    )}

                    {result && (
                        <div className="glass-panel p-6 rounded-xl text-white">
                            <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                                <Activity className="w-5 h-5 text-green-400" />
                                Performance Metrics
                            </h3>
                            <div className="space-y-4">
                                <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg">
                                    <span className="text-gray-400 flex items-center gap-2">
                                        <Clock className="w-4 h-4" /> Makespan
                                    </span>
                                    <span className="font-mono font-bold text-xl text-blue-400">{result.makespan.toFixed(1)}s</span>
                                </div>
                                <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg">
                                    <span className="text-gray-400">Total Tasks</span>
                                    <span className="font-mono font-bold text-xl">{result.total_tasks}</span>
                                </div>

                                <div className="pt-4 border-t border-white/10">
                                    <h4 className="font-medium text-sm text-gray-400 mb-3 uppercase tracking-wider">Success Rates</h4>
                                    <div className="space-y-3">
                                        <div className="flex justify-between items-center">
                                            <span className="text-sm text-red-300">High Priority</span>
                                            <span className="font-bold text-green-400 bg-green-400/10 px-2 py-1 rounded text-sm">
                                                {result.high_priority_stats.met_deadline} / {result.high_priority_stats.total}
                                            </span>
                                        </div>
                                        <div className="w-full bg-white/10 rounded-full h-1.5">
                                            <div
                                                className="bg-red-500 h-1.5 rounded-full transition-all duration-1000"
                                                style={{ width: `${(result.high_priority_stats.met_deadline / (result.high_priority_stats.total || 1)) * 100}%` }}
                                            />
                                        </div>

                                        <div className="flex justify-between items-center mt-2">
                                            <span className="text-sm text-blue-300">Low Priority</span>
                                            <span className="font-bold text-green-400 bg-green-400/10 px-2 py-1 rounded text-sm">
                                                {result.low_priority_stats.met_deadline} / {result.low_priority_stats.total}
                                            </span>
                                        </div>
                                        <div className="w-full bg-white/10 rounded-full h-1.5">
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
                    {result ? (
                        <div className="glass-panel p-1 rounded-xl overflow-hidden shadow-2xl">
                            <GanttChart result={result} />
                        </div>
                    ) : (
                        <div className="glass-panel p-12 rounded-xl text-center text-gray-500 flex flex-col items-center justify-center h-64 border-dashed border-2 border-white/10">
                            <Activity className="w-12 h-12 mb-4 opacity-20" />
                            <p>Select a scenario and run simulation to visualize results.</p>
                        </div>
                    )}

                    {result && (
                        <div className="glass-panel p-6 rounded-xl">
                            <h3 className="text-xl font-bold mb-4 text-white flex items-center gap-2">
                                <Terminal className="w-5 h-5 text-yellow-400" />
                                System Logs
                            </h3>
                            <div className="h-64 overflow-y-auto font-mono text-xs bg-black/50 p-4 rounded-lg border border-white/5 shadow-inner custom-scrollbar">
                                {result.logs.map((log, i) => (
                                    <div key={i} className="mb-1.5 border-b border-white/5 pb-1.5 last:border-0 flex gap-3 hover:bg-white/5 p-1 rounded transition-colors">
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
