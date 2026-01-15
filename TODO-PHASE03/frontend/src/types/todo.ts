/**
 * Todo type definitions matching backend schemas.
 */

export interface Todo {
  id: string; // UUID as string
  user_id: string; // UUID as string
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string; // ISO 8601 timestamp
  updated_at: string; // ISO 8601 timestamp
}

export interface TodoCreateRequest {
  title: string; // Required, 1-200 chars
  description?: string; // Optional, max 2000 chars
}

export interface TodoUpdateRequest {
  title?: string; // Optional, 1-200 chars if provided
  description?: string; // Optional, max 2000 chars if provided
}

export interface TodoListResponse {
  todos: Todo[];
}
