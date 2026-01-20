"use client";

/**
 * ConversationList component for displaying and selecting conversations.
 * Phase III: Todo AI Chatbot - NEW FILE (does not modify Phase II)
 */

import { ConversationSummary } from "@/lib/chatApi";

interface ConversationListProps {
  conversations: ConversationSummary[];
  selectedId?: string;
  onSelect: (conversationId: string) => void;
  onNewChat: () => void;
  onDelete?: (conversationId: string) => void;
  loading?: boolean;
}

export default function ConversationList({
  conversations,
  selectedId,
  onSelect,
  onNewChat,
  onDelete,
  loading = false,
}: ConversationListProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
      return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    } else if (diffDays === 1) {
      return "Yesterday";
    } else if (diffDays < 7) {
      return date.toLocaleDateString([], { weekday: "short" });
    } else {
      return date.toLocaleDateString([], { month: "short", day: "numeric" });
    }
  };

  return (
    <div className="w-72 bg-gray-50 border-r border-gray-200 flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <button
          onClick={onNewChat}
          className="w-full px-4 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:from-purple-600 hover:to-pink-600 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 transition-all duration-200 font-semibold shadow-md hover:shadow-lg transform hover:scale-[1.02]"
        >
          ✨ New Chat
        </button>
      </div>

      {/* Conversation list */}
      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <div className="p-4 text-center text-gray-500">
            <div className="animate-spin w-6 h-6 border-2 border-purple-500 border-t-transparent rounded-full mx-auto mb-2" />
            Loading...
          </div>
        ) : conversations.length === 0 ? (
          <div className="p-4 text-center text-gray-500">
            <p className="text-sm">No conversations yet</p>
            <p className="text-xs mt-1">Start a new chat to begin!</p>
          </div>
        ) : (
          <div className="p-2 space-y-1">
            {conversations.map((conv) => (
              <div
                key={conv.id}
                onClick={() => onSelect(conv.id)}
                className={`group relative p-3 rounded-lg cursor-pointer transition-all duration-200 ${
                  selectedId === conv.id
                    ? "bg-purple-100 border border-purple-200"
                    : "hover:bg-gray-100 border border-transparent"
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <h4 className="font-medium text-gray-800 truncate text-sm">
                      {conv.title || "New Conversation"}
                    </h4>
                    {conv.last_message_preview && (
                      <p className="text-xs text-gray-500 truncate mt-1">
                        {conv.last_message_preview}
                      </p>
                    )}
                  </div>
                  <span className="text-xs text-gray-400 whitespace-nowrap ml-2">
                    {formatDate(conv.updated_at)}
                  </span>
                </div>

                <div className="flex items-center justify-between mt-2">
                  <span className="text-xs text-gray-400">
                    {conv.message_count} messages
                  </span>
                  {onDelete && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onDelete(conv.id);
                      }}
                      className="opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-red-500 transition-all duration-200"
                      title="Delete conversation"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
