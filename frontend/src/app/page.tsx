import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center bg-gradient-to-b from-indigo-50 to-white text-gray-900 p-4 py-20">
      <div className="max-w-2xl text-center space-y-8">
        <h1 className="text-5xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
          Scheduling Simulator
        </h1>
        <p className="text-xl text-gray-600">
          A professional tool for visualizing and analyzing real-time scheduling algorithms.
          Compare SPT, EDF, Priority-First, and DPE algorithms with custom scenarios.
        </p>

        <div className="flex justify-center gap-4">
          <Link
            href="/dashboard"
            className="px-8 py-3 bg-blue-600 hover:bg-blue-500 rounded-full font-bold text-lg text-white transition-all shadow-lg hover:shadow-blue-500/25"
          >
            Launch Simulator
          </Link>
          <a
            href="https://github.com/AndrewCullacino/scheduling-simulator-dpe"
            target="_blank"
            rel="noopener noreferrer"
            className="px-8 py-3 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-full font-bold text-lg transition-all"
          >
            View Source
          </a>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12 text-left">
          <div className="p-6 bg-white rounded-xl shadow-md border border-gray-100">
            <h3 className="font-bold text-lg mb-2 text-blue-600">Real-Time</h3>
            <p className="text-sm text-gray-500">Discrete-event simulation engine with precise timing and event handling.</p>
          </div>
          <div className="p-6 bg-white rounded-xl shadow-md border border-gray-100">
            <h3 className="font-bold text-lg mb-2 text-purple-600">Visual</h3>
            <p className="text-sm text-gray-500">Interactive Gantt charts and detailed metrics for performance analysis.</p>
          </div>
          <div className="p-6 bg-white rounded-xl shadow-md border border-gray-100">
            <h3 className="font-bold text-lg mb-2 text-green-600">Extensible</h3>
            <p className="text-sm text-gray-500">Modular architecture supporting custom algorithms and scenarios.</p>
          </div>
        </div>

        {/* Documentation Section */}
        <div className="mt-24 text-left space-y-12 border-t border-gray-200 pt-16">
          <h2 className="text-3xl font-bold text-gray-800 text-center mb-12">How to Use</h2>

          <div className="space-y-8">
            <div className="flex gap-6 items-start">
              <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-xl shrink-0">1</div>
              <div>
                <h3 className="text-xl font-bold text-gray-800 mb-2">Configure Simulation</h3>
                <p className="text-gray-600">
                  Select an algorithm (e.g., SPT, EDF) and a scenario from the dropdowns.
                  You can adjust the number of machines available for processing.
                  For DPE algorithm, you can also tune the Alpha parameter.
                </p>
              </div>
            </div>

            <div className="flex gap-6 items-start">
              <div className="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center text-purple-600 font-bold text-xl shrink-0">2</div>
              <div>
                <h3 className="text-xl font-bold text-gray-800 mb-2">Create Custom Scenarios</h3>
                <p className="text-gray-600">
                  Choose <strong>"Custom Scenario"</strong> to build your own task set.
                  Use the built-in form to add tasks with specific Arrival Time, Processing Time, Deadline, and Priority.
                  You can also import/export task sets via JSON.
                </p>
              </div>
            </div>

            <div className="flex gap-6 items-start">
              <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center text-green-600 font-bold text-xl shrink-0">3</div>
              <div>
                <h3 className="text-xl font-bold text-gray-800 mb-2">Analyze & Compare</h3>
                <p className="text-gray-600">
                  Click <strong>"Run Simulation"</strong> to visualize the schedule on the Gantt chart.
                  Run multiple simulations to automatically generate a <strong>Comparison Table</strong>, allowing you to benchmark different algorithms side-by-side.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
