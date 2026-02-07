"use client";

/**
 * Edit todo page for updating existing todos.
 */
import { useState, useEffect } from "react";
import { useRouter, useParams } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";
import TodoForm from "@/components/TodoForm";
import { TodoCreateRequest, TodoUpdateRequest, Todo } from "@/types/todo";
import { api } from "@/lib/api";

export default function EditTodoPage() {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const router = useRouter();
  const params = useParams();
  const todoId = params.id as string;

  const [todo, setTodo] = useState<Todo | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/signin");
    }
  }, [authLoading, isAuthenticated, router]);

  useEffect(() => {
    if (isAuthenticated && todoId) {
      fetchTodo();
    }
  }, [isAuthenticated, todoId]);

  const fetchTodo = async () => {
    setLoading(true);
    setError(null);

    try {
      const fetchedTodo = await api.get<Todo>(`/api/tasks/${todoId}`);
      setTodo(fetchedTodo);
    } catch (err: any) {
      if (err.statusCode === 404) {
        setError("Todo not found");
      } else {
        setError("Failed to load todo");
      }
      console.error("Error fetching todo:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (data: TodoCreateRequest | TodoUpdateRequest) => {
    try {
      await api.put<Todo>(`/api/tasks/${todoId}`, data);
      router.push("/todos");
    } catch (err) {
      console.error("Error updating todo:", err);
      throw err;
    }
  };

  const handleCancel = () => {
    router.push("/todos");
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
          <p className="mt-6 text-white text-xl font-bold drop-shadow-lg animate-pulse">Loading your todo...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  if (error || !todo) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-100 via-pink-100 to-blue-100 py-12 px-4 sm:px-6 lg:px-8 flex items-center justify-center">
        <div className="max-w-2xl w-full">
          <div className="bg-gradient-to-r from-red-100 to-pink-100 border-2 border-red-400 rounded-3xl p-8 shadow-2xl animate-shake">
            <div className="text-center">
              <div className="text-6xl mb-4">❌</div>
              <h2 className="text-2xl font-bold text-red-800 mb-3">Oops! Something went wrong</h2>
              <p className="text-red-700 text-lg mb-6">{error || "Todo not found"}</p>
              <button
                onClick={() => router.push("/todos")}
                className="px-8 py-3 bg-gradient-to-r from-red-600 to-pink-600 text-white rounded-2xl hover:from-red-700 hover:to-pink-700 transition-all duration-300 transform hover:scale-110 shadow-xl font-bold"
              >
                🏠 Back to Todos
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-pink-100 to-blue-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto animate-slide-up">
        <div className="bg-white bg-opacity-95 backdrop-blur-lg shadow-2xl rounded-3xl p-8 border-2 border-blue-300">
          <div className="text-center mb-6">
            <div className="text-6xl mb-4 animate-bounce-slow">✏️</div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent animate-fade-in">
              Edit Todo
            </h1>
            <p className="text-gray-600 mt-2">Update your task details ✨</p>
          </div>
          <TodoForm
            mode="edit"
            initialValues={{
              title: todo.title,
              description: todo.description || "",
            }}
            onSubmit={handleSubmit}
            onCancel={handleCancel}
          />
        </div>
      </div>
    </div>
  );
}
