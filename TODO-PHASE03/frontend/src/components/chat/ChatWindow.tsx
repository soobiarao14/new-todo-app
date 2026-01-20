"use client";

/**
 * ChatWindow component for displaying conversation messages.
 * Phase III: Todo AI Chatbot - NEW FILE (does not modify Phase II)
 */

import { useRef, useEffect } from "react";
import { ChatMessage } from "@/lib/chatApi";
import MessageBubble from "./MessageBubble";

interface ChatWindowProps {
  messages: ChatMessage[];
  loading?: boolean;
}

export default function ChatWindow({ messages, loading = false }: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 bg-gradient-to-b from-gray-50 to-white">
      {messages.length === 0 && !loading ? (
        <div className="flex flex-col items-center justify-center h-full text-center text-gray-500">
          <div className="text-6xl mb-4">💬</div>
          <h3 className="text-xl font-semibold text-gray-700 mb-2">
            Start a Conversation
          </h3>
          <p className="max-w-md text-gray-500">
            Ask me to help you manage your tasks! Try saying:
          </p>
          <div className="mt-4 space-y-2">
            <p className="text-purple-600 font-medium">"Add a task to buy groceries"</p>
            <p className="text-purple-600 font-medium">"Show me my tasks"</p>
            <p className="text-purple-600 font-medium">"Mark the groceries task as done"</p>
          </div>
        </div>
      ) : (
        <>
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}

          {/* Loading indicator */}
          {loading && (
            <div className="flex justify-start mb-4">
              <div className="bg-white rounded-2xl rounded-bl-sm px-4 py-3 shadow-md border border-gray-100">
                <div className="flex items-center gap-2">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                  </div>
                  <span className="text-gray-500 text-sm">Thinking...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </>
      )}
    </div>
  );
}
