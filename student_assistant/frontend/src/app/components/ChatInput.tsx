"use client";

import { useEffect, useRef, useState, KeyboardEvent } from "react";

interface ChatInputProps {
  onSend: (text: string) => void;
  isLoading: boolean;
  awaitingStudentId: boolean;
}

export default function ChatInput({ onSend, isLoading, awaitingStudentId }: ChatInputProps) {
  const [input, setInput] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    textarea.style.height = "0px";
    textarea.style.height = `${Math.min(textarea.scrollHeight, 160)}px`;
  }, [input]);

  const handleSend = () => {
    if (input.trim() && !isLoading) {
      onSend(input.trim());
      setInput("");
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-gray-100 bg-white px-4 py-3 sm:px-6 sm:py-4">
      <div className="mx-auto max-w-3xl">
        <div className="flex items-end gap-2 rounded-2xl border border-gray-200 bg-gray-50 p-2 transition-colors focus-within:border-gray-300 focus-within:bg-white">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              awaitingStudentId
                ? "Nhap MSSV cua ban, vi du SV001..."
                : "Nhap tin nhan..."
            }
            rows={1}
            className="max-h-[160px] flex-1 resize-none bg-transparent px-2 py-2 text-sm leading-6 text-gray-900 placeholder:text-gray-400 focus:outline-none"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-xl bg-[#1a1a2e] text-white transition-opacity hover:opacity-90 disabled:opacity-30"
          >
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 10.5L12 3m0 0l7.5 7.5M12 3v18" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
