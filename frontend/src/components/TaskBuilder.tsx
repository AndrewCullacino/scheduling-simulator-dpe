import React, { useState, useRef } from 'react';
import { TaskInput } from '../lib/api';
import { Plus, Trash2, Upload, Download, FileJson } from 'lucide-react';

interface TaskBuilderProps {
    tasks: TaskInput[];
    setTasks: (tasks: TaskInput[]) => void;
}

const TaskBuilder: React.FC<TaskBuilderProps> = ({ tasks, setTasks }) => {
    const [newTask, setNewTask] = useState<TaskInput>({
        id: tasks.length + 1,
        arrival_time: 0,
        processing_time: 1,
        priority: 'LOW',
        deadline: 10,
        cpu_required: 1,
        ram_required: 1,
    });

    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleAddTask = () => {
        setTasks([...tasks, { ...newTask, id: tasks.length > 0 ? Math.max(...tasks.map(t => t.id)) + 1 : 1 }]);
        setNewTask({
            ...newTask,
            id: newTask.id + 1,
        });
    };

    const handleRemoveTask = (id: number) => {
        setTasks(tasks.filter((t) => t.id !== id));
    };

    const handleImport = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            try {
                const importedTasks = JSON.parse(event.target?.result as string);
                if (Array.isArray(importedTasks)) {
                    // Basic validation could go here
                    setTasks(importedTasks);
                } else {
                    alert("Invalid JSON format: Expected an array of tasks.");
                }
            } catch (error) {
                alert("Error parsing JSON file.");
            }
        };
        reader.readAsText(file);
    };

    const handleExport = () => {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(tasks, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "tasks.json");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    };

    return (
        <div className="space-y-6 p-6 bg-white/5 backdrop-blur-md rounded-xl border border-white/10 shadow-xl">
            <div className="flex justify-between items-center">
                <h3 className="text-xl font-semibold text-white flex items-center gap-2">
                    <FileJson className="w-5 h-5 text-blue-400" />
                    Custom Task Builder
                </h3>
                <div className="flex gap-2">
                    <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleImport}
                        className="hidden"
                        accept=".json"
                    />
                    <button
                        onClick={() => fileInputRef.current?.click()}
                        className="flex items-center gap-2 px-3 py-1.5 text-sm bg-blue-600/20 text-blue-300 hover:bg-blue-600/30 rounded-lg transition-colors border border-blue-500/30"
                    >
                        <Upload className="w-4 h-4" /> Import
                    </button>
                    <button
                        onClick={handleExport}
                        className="flex items-center gap-2 px-3 py-1.5 text-sm bg-purple-600/20 text-purple-300 hover:bg-purple-600/30 rounded-lg transition-colors border border-purple-500/30"
                    >
                        <Download className="w-4 h-4" /> Export
                    </button>
                </div>
            </div>

            {/* Add Task Form */}
            <div className="grid grid-cols-2 md:grid-cols-6 gap-4 bg-black/20 p-4 rounded-lg border border-white/5">
                <div>
                    <label className="block text-xs text-gray-400 mb-1">Arrival</label>
                    <input
                        type="number"
                        value={newTask.arrival_time}
                        onChange={(e) => setNewTask({ ...newTask, arrival_time: parseFloat(e.target.value) })}
                        className="w-full bg-black/40 border border-white/10 rounded px-2 py-1 text-sm text-white focus:border-blue-500 outline-none"
                    />
                </div>
                <div>
                    <label className="block text-xs text-gray-400 mb-1">Processing</label>
                    <input
                        type="number"
                        value={newTask.processing_time}
                        onChange={(e) => setNewTask({ ...newTask, processing_time: parseFloat(e.target.value) })}
                        className="w-full bg-black/40 border border-white/10 rounded px-2 py-1 text-sm text-white focus:border-blue-500 outline-none"
                    />
                </div>
                <div>
                    <label className="block text-xs text-gray-400 mb-1">Deadline</label>
                    <input
                        type="number"
                        value={newTask.deadline}
                        onChange={(e) => setNewTask({ ...newTask, deadline: parseFloat(e.target.value) })}
                        className="w-full bg-black/40 border border-white/10 rounded px-2 py-1 text-sm text-white focus:border-blue-500 outline-none"
                    />
                </div>
                <div>
                    <label className="block text-xs text-gray-400 mb-1">Priority</label>
                    <select
                        value={newTask.priority}
                        onChange={(e) => setNewTask({ ...newTask, priority: e.target.value as 'HIGH' | 'LOW' })}
                        className="w-full bg-black/40 border border-white/10 rounded px-2 py-1 text-sm text-white focus:border-blue-500 outline-none"
                    >
                        <option value="HIGH">HIGH</option>
                        <option value="LOW">LOW</option>
                    </select>
                </div>
                <div className="col-span-2 grid grid-cols-2 gap-2">
                    <div>
                        <label className="block text-xs text-gray-400 mb-1">CPU</label>
                        <input
                            type="number"
                            value={newTask.cpu_required}
                            onChange={(e) => setNewTask({ ...newTask, cpu_required: parseInt(e.target.value) })}
                            className="w-full bg-black/40 border border-white/10 rounded px-2 py-1 text-sm text-white focus:border-blue-500 outline-none"
                        />
                    </div>
                    <div>
                        <label className="block text-xs text-gray-400 mb-1">RAM (GB)</label>
                        <input
                            type="number"
                            value={newTask.ram_required}
                            onChange={(e) => setNewTask({ ...newTask, ram_required: parseInt(e.target.value) })}
                            className="w-full bg-black/40 border border-white/10 rounded px-2 py-1 text-sm text-white focus:border-blue-500 outline-none"
                        />
                    </div>
                </div>
                <div className="col-span-2 md:col-span-6 flex justify-end">
                    <button
                        onClick={handleAddTask}
                        className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-500 text-white rounded-lg text-sm font-medium transition-colors"
                    >
                        <Plus className="w-4 h-4" /> Add Task
                    </button>
                </div>
            </div>

            {/* Task List */}
            <div className="overflow-x-auto">
                <table className="w-full text-sm text-left text-gray-300">
                    <thead className="text-xs text-gray-400 uppercase bg-black/30">
                        <tr>
                            <th className="px-4 py-3 rounded-tl-lg">ID</th>
                            <th className="px-4 py-3">Arrival</th>
                            <th className="px-4 py-3">Processing</th>
                            <th className="px-4 py-3">Deadline</th>
                            <th className="px-4 py-3">Priority</th>
                            <th className="px-4 py-3">CPU</th>
                            <th className="px-4 py-3">RAM</th>
                            <th className="px-4 py-3 rounded-tr-lg">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tasks.length === 0 ? (
                            <tr>
                                <td colSpan={8} className="px-4 py-8 text-center text-gray-500">
                                    No tasks added yet. Add manually or import JSON.
                                </td>
                            </tr>
                        ) : (
                            tasks.map((task) => (
                                <tr key={task.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                                    <td className="px-4 py-3 font-medium text-white">{task.id}</td>
                                    <td className="px-4 py-3">{task.arrival_time}</td>
                                    <td className="px-4 py-3">{task.processing_time}</td>
                                    <td className="px-4 py-3">{task.deadline}</td>
                                    <td className="px-4 py-3">
                                        <span className={`px-2 py-0.5 rounded text-xs ${task.priority === 'HIGH'
                                                ? 'bg-red-500/20 text-red-300 border border-red-500/30'
                                                : 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                                            }`}>
                                            {task.priority}
                                        </span>
                                    </td>
                                    <td className="px-4 py-3">{task.cpu_required}</td>
                                    <td className="px-4 py-3">{task.ram_required}GB</td>
                                    <td className="px-4 py-3">
                                        <button
                                            onClick={() => handleRemoveTask(task.id)}
                                            className="text-red-400 hover:text-red-300 transition-colors"
                                        >
                                            <Trash2 className="w-4 h-4" />
                                        </button>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TaskBuilder;
