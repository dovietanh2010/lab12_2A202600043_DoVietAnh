"use client";

import ReactMarkdown from "react-markdown";
import { Message } from "../page";

interface MessageBubbleProps {
  message: Message;
}

type SourceItem = string | { title: string; doc_id: string };

const TOOL_INFO: Record<string, { label: string; icon: string; desc: string }> = {
  rag: { label: "Tai lieu noi bo", icon: "search", desc: "Tim kiem va tong hop tu tai lieu noi bo" },
  general_chat: { label: "Tro chuyen", icon: "chat", desc: "Tra loi tu nhien, khong can tra cuu" },
  fallback: { label: "Ngoai pham vi", icon: "alert", desc: "Cau hoi nam ngoai pham vi ho tro" },
  error: { label: "Loi", icon: "alert", desc: "Da xay ra loi trong qua trinh xu ly" },
  needs_student_id: { label: "Can MSSV", icon: "user", desc: "Yeu cau nhap ma so sinh vien de tiep tuc" },
  get_schedule: { label: "Lich hoc", icon: "calendar", desc: "Tra cuu lich hoc ca nhan" },
  "lich hoc": { label: "Lich hoc", icon: "calendar", desc: "Tra cuu lich hoc ca nhan" },
  get_grades: { label: "Bang diem", icon: "chart", desc: "Tra cuu bang diem hoc tap" },
  "bang diem": { label: "Bang diem", icon: "chart", desc: "Tra cuu bang diem hoc tap" },
  get_exam: { label: "Lich thi", icon: "calendar", desc: "Tra cuu lich thi cuoi ky" },
  "lich thi": { label: "Lich thi", icon: "calendar", desc: "Tra cuu lich thi cuoi ky" },
  get_tuition: { label: "Hoc phi", icon: "wallet", desc: "Tra cuu thong tin hoc phi" },
  "hoc phi": { label: "Hoc phi", icon: "wallet", desc: "Tra cuu thong tin hoc phi" },
  "thong tin ca nhan": { label: "Thong tin ca nhan", icon: "user", desc: "Tra cuu thong tin ca nhan sinh vien" },
};

function ToolIcon({ type }: { type: string }) {
  const cls = "h-3.5 w-3.5";
  switch (type) {
    case "search":
      return (
        <svg className={cls} fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
        </svg>
      );
    case "chat":
      return (
        <svg className={cls} fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0m-12 3.75h.008v.008H5.25v-.008zm0 0c-1.293 0-2.395-.472-3.192-1.192A4.131 4.131 0 011.5 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25-4.03 8.25-9 8.25" />
        </svg>
      );
    case "calendar":
      return (
        <svg className={cls} fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
        </svg>
      );
    case "chart":
      return (
        <svg className={cls} fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
        </svg>
      );
    case "wallet":
      return (
        <svg className={cls} fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" />
        </svg>
      );
    case "user":
      return (
        <svg className={cls} fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
        </svg>
      );
    default:
      return (
        <svg className={cls} fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M11.42 15.17l-5.384 3.183A1.2 1.2 0 014.5 17.244V6.756a1.2 1.2 0 011.536-1.109l5.384 3.183m0 0l5.384-3.183A1.2 1.2 0 0118.3 6.756v10.488a1.2 1.2 0 01-1.536 1.109l-5.384-3.183" />
        </svg>
      );
  }
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";
  const tools = !isUser && message.toolUsed
    ? message.toolUsed.split(",").map((t) => t.trim()).filter(Boolean)
    : [];
  const hasSources = !isUser && message.sources && message.sources.length > 0;
  const hasToolInfo = tools.length > 0 || hasSources;

  return (
    <div className={`flex gap-3 ${isUser ? "flex-row-reverse" : ""}`}>
      {/* Avatar */}
      {!isUser && (
        <div className="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg bg-[#1a1a2e] text-[10px] font-semibold text-white">
          SA
        </div>
      )}

      <div className={`max-w-[80%] ${isUser ? "ml-auto" : ""}`}>
        {/* Collapsible tool info */}
        {!isUser && hasToolInfo && (
          <details className="group mb-2">
            <summary className="flex cursor-pointer list-none items-center gap-1.5 text-xs text-gray-400 transition-colors hover:text-gray-600 [&::-webkit-details-marker]:hidden">
              <svg className="h-3 w-3 transition-transform group-open:rotate-90" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
              </svg>
              <span>
                {tools.map((t) => TOOL_INFO[t]?.label || t).join(", ") || "Chi tiet"}
              </span>
            </summary>
            <div className="mt-1.5 rounded-xl border border-gray-100 bg-gray-50 p-3">
              {/* Tools */}
              {tools.length > 0 && (
                <div className="space-y-2">
                  {tools.map((tool) => {
                    const info = TOOL_INFO[tool] || { label: tool, icon: "default", desc: "" };
                    return (
                      <div key={tool} className="flex items-start gap-2">
                        <span className="mt-0.5 flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-md bg-gray-200 text-gray-500">
                          <ToolIcon type={info.icon} />
                        </span>
                        <div>
                          <span className="text-xs font-medium text-gray-700">{info.label}</span>
                          {info.desc && (
                            <p className="text-[11px] leading-4 text-gray-400">{info.desc}</p>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}

              {/* Sources */}
              {hasSources && (
                <div className={tools.length > 0 ? "mt-2.5 border-t border-gray-100 pt-2.5" : ""}>
                  <p className="mb-1.5 text-[11px] font-medium uppercase tracking-wider text-gray-400">
                    Nguon tham khao
                  </p>
                  <div className="flex flex-wrap gap-1">
                    {message.sources!.map((src: SourceItem, i: number) => {
                      if (typeof src === "object" && src.doc_id) {
                        return (
                          <a
                            key={i}
                            href={`/uploads/${src.doc_id}.pdf`}
                            target="_blank"
                            rel="noreferrer"
                            className="inline-flex items-center gap-1 rounded-md border border-blue-100 bg-blue-50 px-2 py-0.5 text-[11px] text-blue-600 transition-colors hover:bg-blue-100"
                          >
                            <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m.75 12l3 3m0 0l3-3m-3 3v-6m-1.5-9H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                            </svg>
                            {src.title}
                          </a>
                        );
                      }
                      return (
                        <span
                          key={i}
                          className="rounded-md border border-gray-200 bg-white px-2 py-0.5 text-[11px] text-gray-500"
                        >
                          {typeof src === "string" ? src : src.title}
                        </span>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          </details>
        )}

        {/* Message content */}
        <div
          className={`rounded-2xl px-4 py-3 text-sm leading-7 ${
            isUser
              ? "bg-[#1a1a2e] text-white"
              : "bg-gray-50 text-gray-900"
          }`}
        >
          <div className="chat-prose max-w-none">
            <ReactMarkdown
              components={{
                p: ({ children }) => <p>{children}</p>,
                ul: ({ children }) => <ul className="list-disc">{children}</ul>,
                ol: ({ children }) => <ol className="list-decimal">{children}</ol>,
                a: ({ href, children }) => (
                  <a
                    href={href}
                    className={`underline underline-offset-2 ${isUser ? "text-blue-200" : "text-blue-600"}`}
                    target="_blank"
                    rel="noreferrer"
                  >
                    {children}
                  </a>
                ),
                pre: ({ children }) => <pre>{children}</pre>,
                code: ({ children }) => <code>{children}</code>,
                table: ({ children }) => (
                  <div className="overflow-x-auto">
                    <table>{children}</table>
                  </div>
                ),
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  );
}
