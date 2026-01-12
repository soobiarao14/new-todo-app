"use client";

/**
 * TodoForm component for creating and editing todos.
 */
import { useState, FormEvent } from "react";
import { TodoCreateRequest, TodoUpdateRequest } from "@/types/todo";

interface TodoFormProps {
  mode?: "create" | "edit";
  initialValues?: { title: string; description: string };
  onSubmit: (data: TodoCreateRequest | TodoUpdateRequest) => Promise<void>;
  onCancel?: () => void;
}

export default function TodoForm({
  mode = "create",
  initialValues,
  onSubmit,
  onCancel,
}: TodoFormProps) {
  const [title, setTitle] = useState(initialValues?.title || "");
  const [description, setDescription] = useState(initialValues?.description || "");
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<{ title?: string; description?: string }>({});

  const validateForm = (): boolean => {
    const newErrors: { title?: string; description?: string } = {};

    if (!title.trim()) {
      newErrors.title = "Title is required";
    } else if (title.length > 200) {
      newErrors.title = "Title cannot exceed 200 characters";
    }

    if (description && description.length > 2000) {
      newErrors.description = "Description cannot exceed 2000 characters";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      await onSubmit({
        title: title.trim(),
        description: description.trim() || undefined,
      });
    } catch (err) {
      console.error("Form submission error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 animate-fade-in-up">
      <div className="transform transition-all duration-300 hover:scale-105">
        <label htmlFor="title" className="block text-sm font-bold text-gray-800 mb-2">
          🎯 Title <span className="text-red-500">*</span>
        </label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          maxLength={200}
          className="block w-full rounded-xl border-2 border-purple-300 shadow-lg focus:border-purple-500 focus:ring-4 focus:ring-purple-200 transition-all duration-300 text-gray-900 px-4 py-3 text-base"
          placeholder="What do you need to do? ✨"
        />
        {errors.title && (
          <p className="mt-2 text-sm text-red-600 font-bold animate-shake">❌ {errors.title}</p>
        )}
        <p className={`mt-2 text-xs font-semibold ${title.length > 180 ? 'text-orange-600' : 'text-purple-600'}`}>
          {title.length}/200 characters {title.length > 180 ? '⚠️' : '📝'}
        </p>
      </div>

      <div className="transform transition-all duration-300 hover:scale-105">
        <label htmlFor="description" className="block text-sm font-bold text-gray-800 mb-2">
          📋 Description (optional)
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          maxLength={2000}
          rows={4}
          className="block w-full rounded-xl border-2 border-pink-300 shadow-lg focus:border-pink-500 focus:ring-4 focus:ring-pink-200 transition-all duration-300 text-gray-900 px-4 py-3 text-base resize-none"
          placeholder="Add more details about your task... 💭"
        />
        {errors.description && (
          <p className="mt-2 text-sm text-red-600 font-bold animate-shake">❌ {errors.description}</p>
        )}
        <p className={`mt-2 text-xs font-semibold ${description.length > 1800 ? 'text-orange-600' : 'text-pink-600'}`}>
          {description.length}/2000 characters {description.length > 1800 ? '⚠️' : '✍️'}
        </p>
      </div>

      <div className="flex gap-4 pt-4">
        <button
          type="submit"
          disabled={loading}
          className="flex-1 bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 text-white px-6 py-4 rounded-2xl hover:from-purple-700 hover:via-pink-700 hover:to-red-700 focus:outline-none focus:ring-4 focus:ring-purple-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105 shadow-xl font-bold text-lg"
        >
          {loading
            ? mode === "create"
              ? "✨ Creating..."
              : "✨ Updating..."
            : mode === "create"
            ? "🎉 Create Todo"
            : "💫 Update Todo"}
        </button>

        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            disabled={loading}
            className="px-6 py-4 bg-gradient-to-r from-gray-400 to-gray-500 text-white rounded-2xl hover:from-gray-500 hover:to-gray-600 focus:outline-none focus:ring-4 focus:ring-gray-300 disabled:opacity-50 transition-all duration-300 transform hover:scale-105 shadow-xl font-bold text-lg"
          >
            🚫 Cancel
          </button>
        )}
      </div>
    </form>
  );
}
