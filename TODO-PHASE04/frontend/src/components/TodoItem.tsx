/**
 * TodoItem component displays a single todo with title, description, completion status, and timestamps.
 */
import { Todo } from "@/types/todo";

interface TodoItemProps {
  todo: Todo;
  onToggle?: (id: string) => void;
  onEdit?: (id: string) => void;
  onDelete?: (id: string) => void;
}

export default function TodoItem({ todo, onToggle, onEdit, onDelete }: TodoItemProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  return (
    <div className={`border-2 rounded-2xl p-5 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl animate-slide-up ${
      todo.completed
        ? "bg-gradient-to-r from-green-50 to-emerald-50 border-green-300 hover:border-green-400"
        : "bg-gradient-to-r from-purple-50 via-pink-50 to-blue-50 border-purple-300 hover:border-purple-400"
    }`}>
      <div className="flex items-start gap-4">
        {/* Checkbox for completion status */}
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={() => onToggle?.(todo.id)}
          className="mt-1 h-6 w-6 text-purple-600 rounded-lg focus:ring-4 focus:ring-purple-300 cursor-pointer transition-transform hover:scale-125"
        />

        <div className="flex-1 min-w-0">
          {/* Title */}
          <h3
            className={`text-xl font-bold transition-all duration-300 ${
              todo.completed
                ? "line-through text-gray-500"
                : "bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent"
            }`}
          >
            {todo.completed ? "✅ " : "🎯 "}
            {todo.title}
          </h3>

          {/* Description */}
          {todo.description && (
            <p
              className={`mt-2 text-sm transition-colors duration-300 ${
                todo.completed ? "text-gray-400" : "text-gray-700"
              }`}
            >
              {todo.description}
            </p>
          )}

          {/* Timestamps */}
          <div className="mt-3 flex gap-4 text-xs font-semibold">
            <span className="text-purple-600">📅 {formatDate(todo.created_at)}</span>
            {todo.updated_at !== todo.created_at && (
              <span className="text-pink-600">🔄 {formatDate(todo.updated_at)}</span>
            )}
          </div>
        </div>

        {/* Action buttons */}
        <div className="flex gap-2">
          {onEdit && (
            <button
              onClick={() => onEdit(todo.id)}
              className="px-4 py-2 text-sm font-bold text-white bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 rounded-xl transition-all duration-300 transform hover:scale-110 shadow-lg hover:shadow-xl"
            >
              ✏️ Edit
            </button>
          )}
          {onDelete && (
            <button
              onClick={() => onDelete(todo.id)}
              className="px-4 py-2 text-sm font-bold text-white bg-gradient-to-r from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600 rounded-xl transition-all duration-300 transform hover:scale-110 shadow-lg hover:shadow-xl"
            >
              🗑️ Delete
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
