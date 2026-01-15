"use client";

/**
 * Add todo page for creating new todos.
 */
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";
import TodoForm from "@/components/TodoForm";
import { TodoCreateRequest, TodoUpdateRequest, Todo } from "@/types/todo";
import { api } from "@/lib/api";
import { useEffect } from "react";

export default function AddTodoPage() {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push("/signin");
    }
  }, [loading, isAuthenticated, router]);

  const handleSubmit = async (data: TodoCreateRequest | TodoUpdateRequest) => {
    try {
      await api.post<Todo>("/api/tasks", data);
      router.push("/todos");
    } catch (err) {
      console.error("Error creating todo:", err);
      throw err;
    }
  };

  const handleCancel = () => {
    router.push("/todos");
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-red-500 flex items-center justify-center">
        <div className="text-center">
          <div className="relative">
            <div className="animate-spin rounded-full h-20 w-20 border-t-4 border-b-4 border-white mx-auto"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-4xl animate-pulse">✨</span>
            </div>
          </div>
          <p className="mt-6 text-white text-xl font-bold drop-shadow-lg animate-pulse">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-pink-100 to-blue-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto animate-slide-up">
        <div className="bg-white bg-opacity-95 backdrop-blur-lg shadow-2xl rounded-3xl p-8 border-2 border-purple-300">
          <div className="text-center mb-6">
            <div className="text-6xl mb-4 animate-bounce-slow">📝</div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 bg-clip-text text-transparent animate-fade-in">
              Create New Todo
            </h1>
            <p className="text-gray-600 mt-2">Add a new task to your list ✨</p>
          </div>
          <TodoForm
            mode="create"
            onSubmit={handleSubmit}
            onCancel={handleCancel}
          />
        </div>
      </div>
    </div>
  );
}
