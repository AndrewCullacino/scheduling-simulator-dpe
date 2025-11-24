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
        <div className="space-y-6 p-6 bg-white rounded-xl border border-gray-200 shadow-lg">
            <div className="flex justify-between items-center">
                <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                    <FileJson className="w-5 h-5 text-blue-600" />
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
                        className="flex items-center gap-2 px-3 py-1.5 text-sm bg-blue-50 text-blue-600 hover:bg-blue-100 rounded-lg transition-colors border border-blue-200 font-medium"
                    >
                        <Upload className="w-4 h-4" /> Import
                    </button>
                    <button
                        onClick={handleExport}
                        className="flex items-center gap-2 px-3 py-1.5 text-sm bg-purple-50 text-purple-600 hover:bg-purple-100 rounded-lg transition-colors border border-purple-200 font-medium"
                    >
                        <Download className="w-4 h-4" /> Export
                    </button>
                </div>
            </div>

            {/* Add Task Form */}
            <div className="grid grid-cols-2 md:grid-cols-6 gap-4 bg-gray-50 p-4 rounded-lg border border-gray-200">
                <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1">Arrival</label>
                    <input
                        type="number"
                        value={newTask.arrival_time}
                        onChange={(e) => setNewTask({ ...newTask, arrival_time: parseFloat(e.target.value) })}
                        className="w-full bg-white border border-gray-300 rounded-md px-2 py-1.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
                    />
                </div>
                <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1">Processing</label>
                    <input
                        type="number"
                        value={newTask.processing_time}
                        onChange={(e) => setNewTask({ ...newTask, processing_time: parseFloat(e.target.value) })}
                        className="w-full bg-white border border-gray-300 rounded-md px-2 py-1.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
                    />
                </div>
                <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1">Deadline</label>
                    <input
                        type="number"
                        value={newTask.deadline}
                        onChange={(e) => setNewTask({ ...newTask, deadline: parseFloat(e.target.value) })}
                        className="w-full bg-white border border-gray-300 rounded-md px-2 py-1.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
                    />
                </div>
                <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1">Priority</label>
                    <select
                        value={newTask.priority}
                        onChange={(e) => setNewTask({ ...newTask, priority: e.target.value as 'HIGH' | 'LOW' })}
                        className="w-full bg-white border border-gray-300 rounded-md px-2 py-1.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
                    >
                        <option value="HIGH">HIGH</option>
                        <option value="LOW">LOW</option>
                    </select>
                </div>
                <div className="col-span-2 grid grid-cols-2 gap-2">
                    <div>
                        <label className="block text-xs font-medium text-gray-500 mb-1">CPU</label>
                        <input
                            type="number"
                            value={newTask.cpu_required}
                            onChange={(e) => setNewTask({ ...newTask, cpu_required: parseInt(e.target.value) })}
                            className="w-full bg-white border border-gray-300 rounded-md px-2 py-1.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
                        />
                    </div>
                    <div>
                        <label className="block text-xs font-medium text-gray-500 mb-1">RAM (GB)</label>
                        <input
                            type="number"
                            value={newTask.ram_required}
                            onChange={(e) => setNewTask({ ...newTask, ram_required: parseInt(e.target.value) })}
                            className="w-full bg-white border border-gray-300 rounded-md px-2 py-1.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
                        />
                    </div>
                </div>
                <div className="col-span-2 md:col-span-6 flex justify-end">
                    <button
                        onClick={handleAddTask}
                        className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-bold transition-colors shadow-sm"
                    >
                        <Plus className="w-4 h-4" /> Add Task
                    </button>
                </div>
            </div>

            {/* Task List */}
            <div className="overflow-x-auto rounded-lg border border-gray-200">
                <table className="w-full text-sm text-left text-gray-600">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-100">
                        <tr>
                            <th className="px-4 py-3">ID</th>
                            <th className="px-4 py-3">Arrival</th>
                            <th className="px-4 py-3">Processing</th>
                            <th className="px-4 py-3">Deadline</th>
                            <th className="px-4 py-3">Priority</th>
                            <th className="px-4 py-3">CPU</th>
                            <th className="px-4 py-3">RAM</th>
                            <th className="px-4 py-3 text-right">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tasks.length === 0 ? (
                            <tr>
                                <td colSpan={8} className="px-4 py-8 text-center text-gray-400 bg-white">
                                    No tasks added yet. Add manually or import JSON.
                                </td>
                            </tr>
                        ) : (
                            tasks.map((task) => (
                                <tr key={task.id} className="bg-white border-b border-gray-100 hover:bg-gray-50 transition-colors">
                                    <td className="px-4 py-3 font-medium text-gray-900">{task.id}</td>
                                    <td className="px-4 py-3">{task.arrival_time}</td>
                                    <td className="px-4 py-3">{task.processing_time}</td>
                                    <td className="px-4 py-3">{task.deadline}</td>
                                    <td className="px-4 py-3">
                                        <span className={`px-2 py-0.5 rounded text-xs font-bold ${task.priority === 'HIGH'
                                            ? 'bg-red-100 text-red-700 border border-red-200'
                                            : 'bg-blue-100 text-blue-700 border border-blue-200'
                                            }`}>
                                            {task.priority}
                                        </span>
                                    </td>
                                    <td className="px-4 py-3">{task.cpu_required}</td>
                                    <td className="px-4 py-3">{task.ram_required}GB</td>
                                    <td className="px-4 py-3 text-right">
                                        <button
                                            onClick={() => handleRemoveTask(task.id)}
                                            className="text-gray-400 hover:text-red-600 transition-colors p-1 rounded-full hover:bg-red-50"
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
