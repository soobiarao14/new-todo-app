/**
 * Chat API client for AI chatbot functionality.
 * Phase III: Todo AI Chatbot - NEW FILE (does not modify Phase II)
 */

import { api } from "./api";

// Types for chat API
export interface ToolCall {
  tool: string;
  parameters: Record<string, unknown>;
  result: unknown;
  success: boolean;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  tool_calls?: ToolCall[] | null;
  created_at: string;
}

export interface ConversationSummary {
  id: string;
  title: string | null;
  created_at: string;
  updated_at: string;
  message_count: number;
  last_message_preview: string | null;
}

export interface ConversationDetail {
  id: string;
  title: string | null;
  messages: ChatMessage[];
  created_at: string;
  updated_at: string;
}

export interface ChatRequest {
  conversation_id?: string;
  message: string;
}

export interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls: ToolCall[];
}

export interface ConversationListResponse {
  conversations: ConversationSummary[];
  total: number;
}

export interface DashboardStats {
  total_tasks: number;
  completed_tasks: number;
  pending_tasks: number;
  total_conversations: number;
  messages_today: number;
}

/**
 * Send a chat message to the AI assistant.
 */
export async function sendMessage(
  message: string,
  conversationId?: string
): Promise<ChatResponse> {
  const request: ChatRequest = {
    message,
    ...(conversationId && { conversation_id: conversationId }),
  };

  return api.post<ChatResponse>("/api/chat", request);
}

/**
 * Get list of user's conversations.
 */
export async function getConversations(
  limit = 20,
  offset = 0
): Promise<ConversationListResponse> {
  return api.get<ConversationListResponse>(
    `/api/conversations?limit=${limit}&offset=${offset}`
  );
}

/**
 * Get a specific conversation with its messages.
 */
export async function getConversation(
  conversationId: string
): Promise<ConversationDetail> {
  return api.get<ConversationDetail>(`/api/conversations/${conversationId}`);
}

/**
 * Delete a conversation.
 */
export async function deleteConversation(conversationId: string): Promise<void> {
  await api.delete(`/api/conversations/${conversationId}`);
}

/**
 * Get dashboard statistics.
 */
export async function getDashboardStats(): Promise<DashboardStats> {
  return api.get<DashboardStats>("/api/dashboard/stats");
}
