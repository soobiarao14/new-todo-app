"use client";

/**
 * Dashboard page - Analytics and statistics view.
 * Phase III: Todo AI Chatbot - NEW FILE (does not modify Phase II)
 */

import { useState, useEffect } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import StatsCard from "@/components/dashboard/StatsCard";
import { getDashboardStats, DashboardStats } from "@/lib/chatApi";

export default function DashboardPage() {
  const { user, isAuthenticated, loading: authLoading, signOut } = useAuth();
  const router = useRouter();

  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Redirect if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/signin");
    }
  }, [authLoading, isAuthenticated, router]);

  // Fetch stats on mount
  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        const data = await getDashboardStats();
        setStats(data);
      } catch (err) {
        console.error("Error fetching stats:", err);
        setError("Failed to load dashboard statistics");
      } finally {
        setLoading(false);
      }
    };

    if (isAuthenticated) {
      fetchStats();
    }
  }, [isAuthenticated]);

  // Loading screen
  if (authLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-red-500 flex items-center justify-center">
        <div className="text-center">
          <div className="relative">
            <div className="animate-spin rounded-full h-20 w-20 border-t-4 border-b-4 border-white mx-auto"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-4xl animate-pulse">📊</span>
            </div>
          </div>
          <p className="mt-6 text-white text-xl font-bold drop-shadow-lg animate-pulse">
            Loading dashboard...
          </p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  // Calculate completion percentage
  const completionPercentage =
    stats && stats.total_tasks > 0
      ? Math.round((stats.completed_tasks / stats.total_tasks) * 100)
      : 0;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 shadow-2xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-extrabold text-white drop-shadow-lg">
                📊 Dashboard
              </h1>
              {user && (
                <p className="text-sm text-white/80 font-medium mt-1">
                  👤 {user.email}
                </p>
              )}
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => router.push("/chat")}
                className="px-4 py-2 bg-white/20 text-white rounded-xl hover:bg-white/30 focus:outline-none focus:ring-2 focus:ring-white transition-all duration-200 font-semibold backdrop-blur-sm"
              >
                💬 Chat
              </button>
              <button
                onClick={() => router.push("/todos")}
                className="px-4 py-2 bg-white/20 text-white rounded-xl hover:bg-white/30 focus:outline-none focus:ring-2 focus:ring-white transition-all duration-200 font-semibold backdrop-blur-sm"
              >
                📋 Tasks
              </button>
              <button
                onClick={signOut}
                className="px-4 py-2 bg-gradient-to-r from-yellow-400 to-orange-500 text-white rounded-xl hover:from-yellow-300 hover:to-orange-400 focus:outline-none focus:ring-2 focus:ring-white transition-all duration-200 font-semibold shadow-md"
              >
                🚪 Sign Out
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error display */}
        {error && (
          <div className="mb-6 bg-red-100 border border-red-200 rounded-xl px-4 py-3 text-red-800 flex items-center justify-between">
            <span>❌ {error}</span>
            <button
              onClick={() => setError(null)}
              className="text-red-600 hover:text-red-800"
            >
              ✕
            </button>
          </div>
        )}

        {/* Loading state */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5].map((i) => (
              <div
                key={i}
                className="bg-white rounded-2xl shadow-lg p-6 animate-pulse"
              >
                <div className="flex items-center justify-between">
                  <div className="space-y-3">
                    <div className="h-4 w-24 bg-gray-200 rounded" />
                    <div className="h-10 w-16 bg-gray-200 rounded" />
                  </div>
                  <div className="h-16 w-16 bg-gray-200 rounded-2xl" />
                </div>
                <div className="h-1.5 bg-gray-200 mt-6 rounded" />
              </div>
            ))}
          </div>
        ) : stats ? (
          <>
            {/* Stats grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              <StatsCard
                title="Total Tasks"
                value={stats.total_tasks}
                icon="📝"
                color="purple"
                subtitle="All time"
              />
              <StatsCard
                title="Completed Tasks"
                value={stats.completed_tasks}
                icon="✅"
                color="green"
                subtitle={`${completionPercentage}% completion rate`}
              />
              <StatsCard
                title="Pending Tasks"
                value={stats.pending_tasks}
                icon="⏳"
                color="orange"
                subtitle="Still to do"
              />
              <StatsCard
                title="Conversations"
                value={stats.total_conversations}
                icon="💬"
                color="blue"
                subtitle="Chat sessions"
              />
              <StatsCard
                title="Messages Today"
                value={stats.messages_today}
                icon="📨"
                color="pink"
                subtitle="Activity today"
              />
            </div>

            {/* Progress overview */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4">
                📈 Progress Overview
              </h2>

              {stats.total_tasks > 0 ? (
                <div className="space-y-4">
                  {/* Progress bar */}
                  <div>
                    <div className="flex justify-between text-sm text-gray-600 mb-2">
                      <span>Task Completion</span>
                      <span className="font-semibold">
                        {stats.completed_tasks} / {stats.total_tasks}
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-green-400 to-green-600 rounded-full transition-all duration-500"
                        style={{ width: `${completionPercentage}%` }}
                      />
                    </div>
                    <p className="text-sm text-gray-500 mt-2">
                      {completionPercentage}% of tasks completed
                    </p>
                  </div>

                  {/* Quick stats */}
                  <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-100">
                    <div className="text-center p-4 bg-gray-50 rounded-xl">
                      <p className="text-2xl font-bold text-purple-600">
                        {stats.total_conversations}
                      </p>
                      <p className="text-sm text-gray-500">Chat Sessions</p>
                    </div>
                    <div className="text-center p-4 bg-gray-50 rounded-xl">
                      <p className="text-2xl font-bold text-pink-600">
                        {stats.messages_today}
                      </p>
                      <p className="text-sm text-gray-500">Messages Today</p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center py-8">
                  <span className="text-6xl">🎯</span>
                  <h3 className="text-xl font-semibold text-gray-700 mt-4">
                    No tasks yet!
                  </h3>
                  <p className="text-gray-500 mt-2">
                    Start chatting with the AI assistant to create your first task.
                  </p>
                  <button
                    onClick={() => router.push("/chat")}
                    className="mt-4 px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:from-purple-600 hover:to-pink-600 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all duration-200 font-semibold shadow-lg hover:shadow-xl"
                  >
                    💬 Start Chatting
                  </button>
                </div>
              )}
            </div>
          </>
        ) : null}
      </main>
    </div>
  );
}
