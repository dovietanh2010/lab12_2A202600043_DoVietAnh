"use client";

import { useRef, useEffect } from "react";
import { Message } from "../page";
import MessageBubble from "./MessageBubble";

interface ChatWindowProps {
  messages: Message[];
  isLoading: boolean;
}

export default function ChatWindow({ messages, isLoading }: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const showTypingDots = isLoading;

  return (
    <div className="chat-scroll flex-1 overflow-y-auto">
      <div className="mx-auto max-w-3xl px-4 py-6 sm:px-6">
        {messages.length === 0 && (
          <div className="flex h-full min-h-[50vh] items-center justify-center">
            <div className="text-center">
              <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-[#1a1a2e] text-lg font-semibold text-white">
                SA
              </div>
              <h2 className="text-lg font-medium text-gray-900">
                Xin chao! Toi co the giup gi cho ban?
              </h2>
              <p className="mt-2 text-sm text-gray-500">
                Hoi bat ky dieu gi ve lich hoc, diem, hoc phi, hoac quy che hoc vu.
              </p>
            </div>
          </div>
        )}

        <div className="space-y-5">
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}

          {showTypingDots && (
            <div className="flex gap-3">
              <div className="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg bg-[#1a1a2e] text-[10px] font-semibold text-white">
                SA
              </div>
              <div className="flex items-center gap-1.5 pt-2">
                <span className="typing-dot h-2 w-2 rounded-full bg-gray-400" />
                <span className="typing-dot h-2 w-2 rounded-full bg-gray-400" />
                <span className="typing-dot h-2 w-2 rounded-full bg-gray-400" />
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      </div>
    </div>
  );
}
