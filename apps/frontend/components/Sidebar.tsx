"use client";

import React, { useState } from "react";
import {
  ChevronDown,
  Settings,
  LogOut,
  Menu,
  X,
  Home,
  FolderOpen,
  Users,
  BarChart3,
} from "lucide-react";
import Link from "next/link";
import {
  Collapsible,
  CollapsibleTrigger,
  CollapsibleContent,
} from "@/components/ui/collapsible";
import { Separator } from "@/components/ui/separator";

export function Sidebar() {
  const [isOpen, setIsOpen] = useState(true);
  const [expandedSections, setExpandedSections] = useState<string[]>([
    "main",
  ]);

  const toggleSection = (section: string) => {
    setExpandedSections((prev) =>
      prev.includes(section)
        ? prev.filter((s) => s !== section)
        : [...prev, section]
    );
  };

  const menuItems = [
    {
      icon: Home,
      label: "Dashboard",
      href: "/",
      section: "main",
    },
    {
      icon: FolderOpen,
      label: "Projects",
      section: "main",
      items: [
        { label: "All Projects", href: "/projects" },
        { label: "My Projects", href: "/projects/my" },
        { label: "Archived", href: "/projects/archived" },
      ],
    },
    {
      icon: Users,
      label: "Team",
      section: "main",
      items: [
        { label: "Members", href: "/team/members" },
        { label: "Roles", href: "/team/roles" },
      ],
    },
    {
      icon: BarChart3,
      label: "Reports",
      href: "/reports",
      section: "main",
    },
  ];

  return (
    <>
      {/* Mobile menu button */}
      <div className="fixed top-4 left-4 z-50 lg:hidden">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="p-2 bg-white dark:bg-slate-900 rounded-lg shadow border border-slate-200 dark:border-slate-800"
        >
          {isOpen ? (
            <X className="w-5 h-5" />
          ) : (
            <Menu className="w-5 h-5" />
          )}
        </button>
      </div>

      {/* Sidebar */}
      <aside
        className={`${
          isOpen ? "translate-x-0" : "-translate-x-full"
        } fixed lg:relative lg:translate-x-0 top-0 left-0 z-40 transition-transform duration-300 w-64 h-screen bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col`}
      >
        {/* Header */}
        <div className="p-6">
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
            Capoo
          </h1>
          <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
            Project Management
          </p>
        </div>

        <Separator />

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto p-4 space-y-2">
          {menuItems.map((item) => {
            const isExpanded = expandedSections.includes(item.section);
            const Icon = item.icon;

            if (item.items) {
              return (
                <Collapsible
                  key={item.section}
                  open={isExpanded}
                  onOpenChange={() => toggleSection(item.section)}
                >
                  <CollapsibleTrigger className="w-full flex items-center justify-between px-4 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
                    <div className="flex items-center gap-3">
                      <Icon className="w-5 h-5 text-slate-600 dark:text-slate-400" />
                      <span className="text-sm font-medium text-slate-900 dark:text-white">
                        {item.label}
                      </span>
                    </div>
                    <ChevronDown
                      className={`w-4 h-4 text-slate-600 dark:text-slate-400 transition-transform ${
                        isExpanded ? "rotate-180" : ""
                      }`}
                    />
                  </CollapsibleTrigger>
                  <CollapsibleContent className="mt-1 space-y-1">
                    {item.items.map((subItem) => (
                      <Link
                        key={subItem.href}
                        href={subItem.href}
                        className="block px-4 py-2 ml-2 text-sm text-slate-600 dark:text-slate-400 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white transition-colors"
                      >
                        {subItem.label}
                      </Link>
                    ))}
                  </CollapsibleContent>
                </Collapsible>
              );
            }

            return (
              <Link
                key={item.href}
                href={item.href!}
                className="flex items-center gap-3 px-4 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors text-slate-900 dark:text-white"
              >
                <Icon className="w-5 h-5 text-slate-600 dark:text-slate-400" />
                <span className="text-sm font-medium">{item.label}</span>
              </Link>
            );
          })}
        </nav>

        <Separator />

        {/* Settings and Logout */}
        <div className="p-4 space-y-2">
          <Link
            href="/settings"
            className="flex items-center gap-3 px-4 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors text-slate-900 dark:text-white"
          >
            <Settings className="w-5 h-5 text-slate-600 dark:text-slate-400" />
            <span className="text-sm font-medium">Settings</span>
          </Link>
          <button className="w-full flex items-center gap-3 px-4 py-2 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors text-red-600 dark:text-red-400">
            <LogOut className="w-5 h-5" />
            <span className="text-sm font-medium">Logout</span>
          </button>
        </div>
      </aside>

      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  );
}
