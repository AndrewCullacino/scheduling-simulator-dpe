import React from 'react';
import { SimulationResult } from '../lib/api';
import { CheckCircle, XCircle, Trash2 } from 'lucide-react';

export interface SimulationRun {
    id: string;
    timestamp: number;
    algorithm: string;
    scenario: string;
    result: SimulationResult;
}

interface ComparisonTableProps {
    runs: SimulationRun[];
    onSelect: (runId: string) => void;
    selectedRunId: string | null;
    onDelete: (runId: string) => void;
}

const ComparisonTable: React.FC<ComparisonTableProps> = ({ runs, onSelect, selectedRunId, onDelete }) => {
    if (runs.length === 0) return null;

    return (
        <div className="overflow-x-auto">
            <table className="w-full text-sm text-left text-gray-500">
                <thead className="text-xs text-gray-700 uppercase bg-gray-100">
                    <tr>
                        <th scope="col" className="px-6 py-3 rounded-tl-lg">Metric</th>
                        {runs.map((run, index) => (
                            <th key={run.id} scope="col" className={`px-6 py-3 min-w-[200px] ${index === runs.length - 1 ? 'rounded-tr-lg' : ''}`}>
                                <div className="flex justify-between items-start">
                                    <div>
                                        <div className="font-bold text-blue-600 text-base">Run {index + 1}</div>
                                        <div className="text-xs text-gray-500">{new Date(run.timestamp).toLocaleTimeString()}</div>
                                    </div>
                                    <button
                                        onClick={(e) => { e.stopPropagation(); onDelete(run.id); }}
                                        className="text-gray-400 hover:text-red-500 transition-colors"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                </div>
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    <tr className="bg-white border-b">
                        <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">Algorithm</th>
                        {runs.map(run => (
                            <td key={run.id} className="px-6 py-4 font-medium">{run.algorithm}</td>
                        ))}
                    </tr>
                    <tr className="bg-gray-50 border-b">
                        <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">Scenario</th>
                        {runs.map(run => (
                            <td key={run.id} className="px-6 py-4">{run.scenario}</td>
                        ))}
                    </tr>
                    <tr className="bg-white border-b">
                        <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">Makespan</th>
                        {runs.map(run => (
                            <td key={run.id} className="px-6 py-4 font-mono text-blue-600 font-bold">
                                {run.result.makespan.toFixed(1)}s
                            </td>
                        ))}
                    </tr>
                    <tr className="bg-gray-50 border-b">
                        <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">Total Tasks</th>
                        {runs.map(run => (
                            <td key={run.id} className="px-6 py-4">{run.result.total_tasks}</td>
                        ))}
                    </tr>
                    <tr className="bg-white border-b">
                        <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">High Priority Success</th>
                        {runs.map(run => {
                            const stats = run.result.high_priority_stats;
                            const rate = stats.total > 0 ? (stats.met_deadline / stats.total) * 100 : 0;
                            return (
                                <td key={run.id} className="px-6 py-4">
                                    <div className="flex items-center gap-2">
                                        <span className={`font-bold ${rate === 100 ? 'text-green-600' : rate >= 80 ? 'text-yellow-600' : 'text-red-600'}`}>
                                            {rate.toFixed(0)}%
                                        </span>
                                        <span className="text-xs text-gray-400">({stats.met_deadline}/{stats.total})</span>
                                    </div>
                                </td>
                            );
                        })}
                    </tr>
                    <tr className="bg-gray-50 border-b">
                        <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">Low Priority Success</th>
                        {runs.map(run => {
                            const stats = run.result.low_priority_stats;
                            const rate = stats.total > 0 ? (stats.met_deadline / stats.total) * 100 : 0;
                            return (
                                <td key={run.id} className="px-6 py-4">
                                    <div className="flex items-center gap-2">
                                        <span className={`font-bold ${rate === 100 ? 'text-green-600' : rate >= 80 ? 'text-yellow-600' : 'text-red-600'}`}>
                                            {rate.toFixed(0)}%
                                        </span>
                                        <span className="text-xs text-gray-400">({stats.met_deadline}/{stats.total})</span>
                                    </div>
                                </td>
                            );
                        })}
                    </tr>
                    <tr className="bg-white">
                        <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">Action</th>
                        {runs.map(run => (
                            <td key={run.id} className="px-6 py-4">
                                <button
                                    onClick={() => onSelect(run.id)}
                                    className={`px-4 py-2 rounded-lg text-sm font-bold transition-all ${selectedRunId === run.id
                                            ? 'bg-blue-600 text-white shadow-lg'
                                            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                        }`}
                                >
                                    {selectedRunId === run.id ? 'Viewing Details' : 'View Details'}
                                </button>
                            </td>
                        ))}
                    </tr>
                </tbody>
            </table>
        </div>
    );
};

export default ComparisonTable;
