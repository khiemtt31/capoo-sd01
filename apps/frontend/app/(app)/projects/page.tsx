"use client";

import { FolderOpen } from "lucide-react";

export default function ProjectsPage() {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-slate-900 dark:text-white flex items-center gap-3">
          <FolderOpen className="w-10 h-10" />
          Projects
        </h1>
        <p className="text-slate-600 dark:text-slate-400 mt-2">
          Manage and view all your projects
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[1, 2, 3, 4, 5, 6].map((project) => (
          <div
            key={project}
            className="bg-white dark:bg-slate-900 rounded-lg shadow border border-slate-200 dark:border-slate-800 p-6 hover:shadow-lg transition-shadow cursor-pointer"
          >
            <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2">
              Project {project}
            </h3>
            <p className="text-sm text-slate-600 dark:text-slate-400 mb-4">
              Description for project {project}
            </p>
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium px-2 py-1 rounded-full bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300">
                Active
              </span>
              <span className="text-xs text-slate-600 dark:text-slate-400">
                3 members
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
