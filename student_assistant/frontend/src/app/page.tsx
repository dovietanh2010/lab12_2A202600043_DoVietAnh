"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";

export interface Source {
  title: string;
  doc_id: string;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
  toolUsed?: string;
}

interface ChatApiResponse {
  thread_id: string;
  response: string;
  sources?: Source[];
  tool_used?: string;
  requires_student_id?: boolean;
  student_id?: string | null;
}

function createThreadId() {
  return crypto.randomUUID();
}

function sanitizeAssistantContent(content: string) {
  return content
    .replace(/<think>[\s\S]*?<\/think>/gi, "")
    .replace(/<\/?think>/gi, "")
    .trim();
}

export default function Home() {
  const { user, isLoading: authLoading, logout } = useAuth();
  const router = useRouter();
  const [threadId, setThreadId] = useState<string>(createThreadId);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [awaitingStudentId, setAwaitingStudentId] = useState(false);

  if (authLoading || !user) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="h-6 w-6 animate-spin rounded-full border-2 border-gray-300 border-t-[#1a1a2e]" />
      </div>
    );
  }

  const sendMessage = async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      content: trimmed,
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${user.token}`,
        },
        body: JSON.stringify({
          thread_id: threadId,
          message: trimmed,
          student_id: user.student_id,
        }),
      });

      if (res.status === 401) {
        logout();
        return;
      }

      if (!res.ok) {
        throw new Error("Request failed");
      }

      const data = (await res.json()) as ChatApiResponse;
      setAwaitingStudentId(Boolean(data.requires_student_id));

      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: sanitizeAssistantContent(data.response || ""),
          sources: data.sources || [],
          toolUsed: data.tool_used || "",
        },
      ]);
    } catch {
      setAwaitingStudentId(false);
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: "Xin loi, da co loi xay ra. Vui long thu lai sau.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const startNewConversation = () => {
    setMessages([]);
    setThreadId(createThreadId());
    setAwaitingStudentId(false);
  };

  return (
    <div className="flex h-screen flex-col bg-white">
      <header className="flex items-center justify-between border-b border-gray-100 px-4 py-3 sm:px-6">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#1a1a2e] text-xs font-semibold text-white">
            SA
          </div>
          <span className="text-sm font-medium text-gray-900">Student Assistant</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-blue-50 px-2.5 py-1 text-xs font-medium text-blue-700">
            {user.display_name}
            {user.student_id && ` (${user.student_id})`}
          </span>
          {user.role === "admin" && (
            <button
              onClick={() => router.push("/admin")}
              className="rounded-lg border border-gray-200 px-3 py-1.5 text-xs font-medium text-gray-600 transition-colors hover:bg-gray-50"
            >
              Quan ly
            </button>
          )}
          <button
            onClick={startNewConversation}
            className="rounded-lg border border-gray-200 px-3 py-1.5 text-xs font-medium text-gray-600 transition-colors hover:bg-gray-50"
          >
            Cuoc tro chuyen moi
          </button>
          <button
            onClick={logout}
            className="rounded-lg border border-gray-200 px-3 py-1.5 text-xs font-medium text-red-500 transition-colors hover:bg-red-50"
          >
            Dang xuat
          </button>
        </div>
      </header>

      <ChatWindow messages={messages} isLoading={isLoading} />

      <ChatInput
        onSend={sendMessage}
        isLoading={isLoading}
        awaitingStudentId={awaitingStudentId}
      />
    </div>
  );
}
