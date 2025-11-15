"use client";

import { Settings } from "lucide-react";

export default function SettingsPage() {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-slate-900 dark:text-white flex items-center gap-3">
          <Settings className="w-10 h-10" />
          Settings
        </h1>
        <p className="text-slate-600 dark:text-slate-400 mt-2">
          Manage your account and preferences
        </p>
      </div>

      <div className="max-w-2xl space-y-8">
        {/* Profile Settings */}
        <div className="bg-white dark:bg-slate-900 rounded-lg shadow border border-slate-200 dark:border-slate-800 p-6">
          <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-4">
            Profile Settings
          </h2>
          <p className="text-slate-600 dark:text-slate-400">
            Update your profile information here
          </p>
        </div>

        {/* Notification Settings */}
        <div className="bg-white dark:bg-slate-900 rounded-lg shadow border border-slate-200 dark:border-slate-800 p-6">
          <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-4">
            Notifications
          </h2>
          <p className="text-slate-600 dark:text-slate-400">
            Manage notification preferences
          </p>
        </div>

        {/* Security */}
        <div className="bg-white dark:bg-slate-900 rounded-lg shadow border border-slate-200 dark:border-slate-800 p-6">
          <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-4">
            Security
          </h2>
          <p className="text-slate-600 dark:text-slate-400">
            Manage password and security settings
          </p>
        </div>
      </div>
    </div>
  );
}
