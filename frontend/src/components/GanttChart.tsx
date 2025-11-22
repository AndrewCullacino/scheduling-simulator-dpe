import React from 'react';
import { TaskResult, SimulationResult } from '../lib/api';

interface GanttChartProps {
    result: SimulationResult;
}

const GanttChart: React.FC<GanttChartProps> = ({ result }) => {
    const machines = Array.from(new Set(result.logs.filter(l => l.machine_id !== undefined).map(l => l.machine_id!))).sort((a, b) => a - b);
    const maxTime = result.makespan * 1.1; // Add some padding

    const getTaskColor = (priority: string) => {
        return priority === 'HIGH' ? 'bg-red-500' : 'bg-blue-500';
    };

    return (
        <div className="w-full overflow-x-auto p-4 bg-white rounded-lg shadow">
            <h2 className="text-xl font-bold mb-4">Schedule Visualization</h2>
            <div className="relative" style={{ minWidth: '800px' }}>
                {/* Time Axis */}
                <div className="flex border-b border-gray-300 pb-2 mb-2">
                    <div className="w-24 font-bold">Machine</div>
                    <div className="flex-1 relative h-6">
                        {Array.from({ length: Math.ceil(maxTime / 5) + 1 }).map((_, i) => (
                            <div
                                key={i}
                                className="absolute text-xs text-gray-500 transform -translate-x-1/2"
                                style={{ left: `${(i * 5 / maxTime) * 100}%` }}
                            >
                                {i * 5}
                            </div>
                        ))}
                    </div>
                </div>

                {/* Machines */}
                {machines.map(machineId => (
                    <div key={machineId} className="flex items-center mb-4 h-12 border-b border-gray-100">
                        <div className="w-24 font-medium">Machine {machineId}</div>
                        <div className="flex-1 relative h-full bg-gray-50 rounded">
                            {result.tasks
                                .filter(t => {
                                    // Find the machine this task ran on from logs or if we added machine_id to TaskResult (we didn't yet, but we can infer or use logs)
                                    // Wait, TaskResult doesn't have machine_id. I should add it to TaskResult in backend or infer from logs.
                                    // For now, let's use logs to find machine_id for each task.
                                    const startLog = result.logs.find(l => l.event === 'START' && l.task_id === t.id);
                                    return startLog?.machine_id === machineId;
                                })
                                .map(task => (
                                    <div
                                        key={task.id}
                                        className={`absolute h-8 top-2 rounded px-2 text-xs text-white flex items-center justify-center overflow-hidden whitespace-nowrap ${getTaskColor(task.priority)}`}
                                        style={{
                                            left: `${(task.start_time! / maxTime) * 100}%`,
                                            width: `${((task.completion_time! - task.start_time!) / maxTime) * 100}%`,
                                        }}
                                        title={`Task ${task.id} (${task.priority})\nStart: ${task.start_time}\nEnd: ${task.completion_time}`}
                                    >
                                        T{task.id}
                                    </div>
                                ))}
                        </div>
                    </div>
                ))}
            </div>

            {/* Legend */}
            <div className="mt-4 flex gap-4 text-sm">
                <div className="flex items-center gap-2">
                    <div className="w-4 h-4 bg-red-500 rounded"></div>
                    <span>High Priority</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-4 h-4 bg-blue-500 rounded"></div>
                    <span>Low Priority</span>
                </div>
            </div>
        </div>
    );
};

export default GanttChart;
