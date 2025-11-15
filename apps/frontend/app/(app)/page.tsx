"use client";

export default function DashboardPage() {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-slate-900 dark:text-white">
          Dashboard
        </h1>
        <p className="text-slate-600 dark:text-slate-400 mt-2">
          Welcome to your dashboard
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white dark:bg-slate-900 rounded-lg shadow p-6 border border-slate-200 dark:border-slate-800">
          <h3 className="text-slate-600 dark:text-slate-400 text-sm font-medium mb-2">
            Total Projects
          </h3>
          <p className="text-3xl font-bold text-slate-900 dark:text-white">
            12
          </p>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-lg shadow p-6 border border-slate-200 dark:border-slate-800">
          <h3 className="text-slate-600 dark:text-slate-400 text-sm font-medium mb-2">
            Active Tasks
          </h3>
          <p className="text-3xl font-bold text-slate-900 dark:text-white">
            24
          </p>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-lg shadow p-6 border border-slate-200 dark:border-slate-800">
          <h3 className="text-slate-600 dark:text-slate-400 text-sm font-medium mb-2">
            Team Members
          </h3>
          <p className="text-3xl font-bold text-slate-900 dark:text-white">
            8
          </p>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-lg shadow p-6 border border-slate-200 dark:border-slate-800">
          <h3 className="text-slate-600 dark:text-slate-400 text-sm font-medium mb-2">
            Completion Rate
          </h3>
          <p className="text-3xl font-bold text-slate-900 dark:text-white">
            78%
          </p>
        </div>
      </div>

      <div className="mt-12 bg-white dark:bg-slate-900 rounded-lg shadow border border-slate-200 dark:border-slate-800">
        <div className="p-6">
          <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-4">
            Recent Activity
          </h2>
          <div className="space-y-4">
            {[1, 2, 3].map((item) => (
              <div
                key={item}
                className="flex items-center justify-between py-3 border-b border-slate-200 dark:border-slate-800 last:border-b-0"
              >
                <div>
                  <p className="text-slate-900 dark:text-white font-medium">
                    Task activity {item}
                  </p>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    2 hours ago
                  </p>
                </div>
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300">
                  Active
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
