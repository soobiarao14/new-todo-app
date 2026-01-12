"use client";

/**
 * Todos list page - displays all user's todos with CRUD operations.
 */
import { useState, useEffect } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import TodoList from "@/components/TodoList";
import { Todo, TodoListResponse } from "@/types/todo";
import { api } from "@/lib/api";

export default function TodosPage() {
  const { user, isAuthenticated, loading: authLoading, signOut } = useAuth();
  const router = useRouter();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/signin");
    }
  }, [authLoading, isAuthenticated, router]);

  useEffect(() => {
    if (isAuthenticated) {
      fetchTodos();
    }
  }, [isAuthenticated]);

  const fetchTodos = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.get<TodoListResponse>("/api/tasks");
      setTodos(response.todos);
    } catch (err) {
      setError("Failed to load todos");
      console.error("Error fetching todos:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (id: string) => {
    try {
      const updatedTodo = await api.patch<Todo>(`/api/tasks/${id}/complete`);
      setTodos((prev) =>
        prev.map((todo) => (todo.id === id ? updatedTodo : todo))
      );
    } catch (err) {
      console.error("Error toggling todo:", err);
    }
  };

  const handleEdit = (id: string) => {
    router.push(`/todos/${id}/edit`);
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this todo?")) {
      return;
    }

    try {
      await api.delete(`/api/tasks/${id}`);
      setTodos((prev) => prev.filter((todo) => todo.id !== id));
    } catch (err) {
      console.error("Error deleting todo:", err);
    }
  };

  if (authLoading || loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-red-500 flex items-center justify-center">
        <div className="text-center">
          <div className="relative">
            <div className="animate-spin rounded-full h-20 w-20 border-t-4 border-b-4 border-white mx-auto"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-4xl animate-pulse">✨</span>
            </div>
          </div>
          <p className="mt-6 text-white text-xl font-bold drop-shadow-lg animate-pulse">Loading your todos...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-pink-100 to-blue-100">
      {/* Header */}
      <header className="bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 shadow-2xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div className="animate-slide-in-left">
              <h1 className="text-3xl font-extrabold text-white drop-shadow-lg">🎯 My Todos</h1>
              {user && (
                <p className="text-sm text-white font-semibold mt-1 drop-shadow-md">👤 {user.email}</p>
              )}
            </div>
            <div className="flex gap-3 animate-slide-in-right">
              <button
                onClick={() => router.push("/todos/add")}
                className="px-6 py-3 bg-white text-purple-600 rounded-2xl hover:bg-purple-50 hover:scale-110 focus:outline-none focus:ring-4 focus:ring-white transition-all duration-300 font-bold shadow-xl transform"
              >
                ➕ Add Todo
              </button>
              <button
                onClick={signOut}
                className="px-6 py-3 bg-gradient-to-r from-yellow-400 to-orange-500 text-white rounded-2xl hover:from-yellow-300 hover:to-orange-400 hover:scale-110 focus:outline-none focus:ring-4 focus:ring-white transition-all duration-300 font-bold shadow-xl transform"
              >
                🚪 Sign Out
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
        {error && (
          <div className="mb-6 bg-gradient-to-r from-red-100 to-pink-100 border-2 border-red-400 rounded-2xl p-6 shadow-lg animate-shake">
            <p className="text-red-800 font-bold">❌ {error}</p>
          </div>
        )}

        <TodoList
          todos={todos}
          onToggle={handleToggle}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      </main>
    </div>
  );
}
