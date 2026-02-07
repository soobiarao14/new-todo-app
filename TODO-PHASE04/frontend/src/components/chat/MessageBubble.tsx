"use client";

/**
 * MessageBubble component for displaying chat messages.
 * Phase III: Todo AI Chatbot - NEW FILE (does not modify Phase II)
 */

import { ChatMessage, ToolCall } from "@/lib/chatApi";

interface MessageBubbleProps {
  message: ChatMessage;
}

function ToolCallDisplay({ toolCall }: { toolCall: ToolCall }) {
  const getToolIcon = (tool: string) => {
    switch (tool) {
      case "add_task":
        return "➕";
      case "list_tasks":
        return "📋";
      case "complete_task":
        return "✅";
      case "delete_task":
        return "🗑️";
      case "update_task":
        return "✏️";
      default:
        return "🔧";
    }
  };

  return (
    <div
      className={`mt-2 p-2 rounded-lg text-sm ${
        toolCall.success
          ? "bg-green-100 border border-green-200"
          : "bg-red-100 border border-red-200"
      }`}
    >
      <div className="flex items-center gap-2 font-medium">
        <span>{getToolIcon(toolCall.tool)}</span>
        <span className="capitalize">{toolCall.tool.replace("_", " ")}</span>
        <span
          className={`ml-auto text-xs px-2 py-0.5 rounded ${
            toolCall.success ? "bg-green-200 text-green-800" : "bg-red-200 text-red-800"
          }`}
        >
          {toolCall.success ? "Success" : "Failed"}
        </span>
      </div>
    </div>
  );
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 shadow-md ${
          isUser
            ? "bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-br-sm"
            : "bg-white text-gray-800 rounded-bl-sm border border-gray-100"
        }`}
      >
        {/* Message content */}
        <div className="whitespace-pre-wrap break-words">{message.content}</div>

        {/* Tool calls (for assistant messages) */}
        {!isUser && message.tool_calls && message.tool_calls.length > 0 && (
          <div className="mt-2 border-t border-gray-200 pt-2">
            {message.tool_calls.map((tc, index) => (
              <ToolCallDisplay key={index} toolCall={tc} />
            ))}
          </div>
        )}

        {/* Timestamp */}
        <div
          className={`text-xs mt-2 ${isUser ? "text-purple-100" : "text-gray-400"}`}
        >
          {new Date(message.created_at).toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </div>
      </div>
    </div>
  );
}
