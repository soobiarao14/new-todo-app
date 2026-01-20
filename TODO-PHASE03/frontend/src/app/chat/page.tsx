"use client";

/**
 * Chat page - AI chatbot interface for task management.
 * Phase III: Todo AI Chatbot - NEW FILE (does not modify Phase II)
 */

import { useState, useEffect, useCallback } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import ChatWindow from "@/components/chat/ChatWindow";
import MessageInput from "@/components/chat/MessageInput";
import ConversationList from "@/components/chat/ConversationList";
import {
  ChatMessage,
  ConversationSummary,
  sendMessage,
  getConversations,
  getConversation,
  deleteConversation,
} from "@/lib/chatApi";

export default function ChatPage() {
  const { user, isAuthenticated, loading: authLoading, signOut } = useAuth();
  const router = useRouter();

  // Conversation state
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [selectedConversationId, setSelectedConversationId] = useState<string | undefined>();
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  // Loading states
  const [loadingConversations, setLoadingConversations] = useState(true);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [sendingMessage, setSendingMessage] = useState(false);

  // Error state
  const [error, setError] = useState<string | null>(null);

  // Redirect if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/signin");
    }
  }, [authLoading, isAuthenticated, router]);

  // Fetch conversations on mount
  const fetchConversations = useCallback(async () => {
    try {
      setLoadingConversations(true);
      const response = await getConversations();
      setConversations(response.conversations);
    } catch (err) {
      console.error("Error fetching conversations:", err);
      setError("Failed to load conversations");
    } finally {
      setLoadingConversations(false);
    }
  }, []);

  useEffect(() => {
    if (isAuthenticated) {
      fetchConversations();
    }
  }, [isAuthenticated, fetchConversations]);

  // Load conversation messages when selected
  const loadConversation = useCallback(async (conversationId: string) => {
    try {
      setLoadingMessages(true);
      setError(null);
      const conversation = await getConversation(conversationId);
      setMessages(conversation.messages);
      setSelectedConversationId(conversationId);
    } catch (err) {
      console.error("Error loading conversation:", err);
      setError("Failed to load conversation");
    } finally {
      setLoadingMessages(false);
    }
  }, []);

  // Handle starting a new chat
  const handleNewChat = () => {
    setSelectedConversationId(undefined);
    setMessages([]);
    setError(null);
  };

  // Handle selecting a conversation
  const handleSelectConversation = (conversationId: string) => {
    loadConversation(conversationId);
  };

  // Handle deleting a conversation
  const handleDeleteConversation = async (conversationId: string) => {
    if (!confirm("Are you sure you want to delete this conversation?")) {
      return;
    }

    try {
      await deleteConversation(conversationId);
      setConversations((prev) => prev.filter((c) => c.id !== conversationId));

      // If deleted conversation was selected, clear the chat
      if (selectedConversationId === conversationId) {
        handleNewChat();
      }
    } catch (err) {
      console.error("Error deleting conversation:", err);
      setError("Failed to delete conversation");
    }
  };

  // Handle sending a message
  const handleSendMessage = async (content: string) => {
    try {
      setSendingMessage(true);
      setError(null);

      // Optimistically add user message to UI
      const tempUserMessage: ChatMessage = {
        id: `temp-${Date.now()}`,
        role: "user",
        content,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, tempUserMessage]);

      // Send message to API
      const response = await sendMessage(content, selectedConversationId);

      // Update conversation ID if this was a new conversation
      if (!selectedConversationId) {
        setSelectedConversationId(response.conversation_id);
      }

      // Add assistant response to messages
      const assistantMessage: ChatMessage = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content: response.response,
        tool_calls: response.tool_calls,
        created_at: new Date().toISOString(),
      };

      // Update messages (remove temp user message, add real ones)
      setMessages((prev) => {
        const filtered = prev.filter((m) => m.id !== tempUserMessage.id);
        return [
          ...filtered,
          { ...tempUserMessage, id: `user-${Date.now()}` },
          assistantMessage,
        ];
      });

      // Refresh conversations list to update sidebar
      fetchConversations();
    } catch (err) {
      console.error("Error sending message:", err);
      setError("Failed to send message. Please try again.");

      // Remove optimistic message on error
      setMessages((prev) => prev.filter((m) => !m.id.startsWith("temp-")));
    } finally {
      setSendingMessage(false);
    }
  };

  // Loading screen
  if (authLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-red-500 flex items-center justify-center">
        <div className="text-center">
          <div className="relative">
            <div className="animate-spin rounded-full h-20 w-20 border-t-4 border-b-4 border-white mx-auto"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-4xl animate-pulse">💬</span>
            </div>
          </div>
          <p className="mt-6 text-white text-xl font-bold drop-shadow-lg animate-pulse">
            Loading chat...
          </p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 shadow-2xl">
        <div className="px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-extrabold text-white drop-shadow-lg">
                💬 AI Task Assistant
              </h1>
              {user && (
                <p className="text-sm text-white/80 font-medium mt-0.5">
                  👤 {user.email}
                </p>
              )}
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => router.push("/todos")}
                className="px-4 py-2 bg-white/20 text-white rounded-xl hover:bg-white/30 focus:outline-none focus:ring-2 focus:ring-white transition-all duration-200 font-semibold backdrop-blur-sm"
              >
                📋 Tasks
              </button>
              <button
                onClick={() => router.push("/dashboard")}
                className="px-4 py-2 bg-white/20 text-white rounded-xl hover:bg-white/30 focus:outline-none focus:ring-2 focus:ring-white transition-all duration-200 font-semibold backdrop-blur-sm"
              >
                📊 Dashboard
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

      {/* Error banner */}
      {error && (
        <div className="bg-red-100 border-b border-red-200 px-4 py-2 text-red-800 text-sm flex items-center justify-between">
          <span>❌ {error}</span>
          <button
            onClick={() => setError(null)}
            className="text-red-600 hover:text-red-800"
          >
            ✕
          </button>
        </div>
      )}

      {/* Main content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar - Conversation list */}
        <ConversationList
          conversations={conversations}
          selectedId={selectedConversationId}
          onSelect={handleSelectConversation}
          onNewChat={handleNewChat}
          onDelete={handleDeleteConversation}
          loading={loadingConversations}
        />

        {/* Chat area */}
        <div className="flex-1 flex flex-col">
          <ChatWindow
            messages={messages}
            loading={sendingMessage || loadingMessages}
          />
          <MessageInput
            onSend={handleSendMessage}
            disabled={sendingMessage}
            placeholder="Ask me to manage your tasks..."
          />
        </div>
      </div>
    </div>
  );
}
