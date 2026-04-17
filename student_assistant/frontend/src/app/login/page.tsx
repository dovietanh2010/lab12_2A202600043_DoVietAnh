"use client";

import { useState } from "react";
import { useAuth } from "@/lib/auth-context";

export default function LoginPage() {
  const { login, isLoading: authLoading } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      await login(username, password);
    } catch (err: any) {
      setError(err.message || "Đăng nhập thất bại");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (authLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="h-6 w-6 animate-spin rounded-full border-2 border-gray-300 border-t-[#1a1a2e]" />
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-white px-4">
      <div className="w-full max-w-sm">
        {/* Logo */}
        <div className="mb-8 text-center">
          <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-[#1a1a2e] text-lg font-bold text-white">
            SA
          </div>
          <h1 className="text-xl font-semibold text-gray-900">Student Assistant</h1>
          <p className="mt-1 text-sm text-gray-500">Dang nhap de tiep tuc</p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="username" className="mb-1.5 block text-sm font-medium text-gray-700">
              Ten dang nhap
            </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="admin, sinhvien1, sinhvien2, sinhvien3"
              className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm text-gray-900 outline-none transition-colors placeholder:text-gray-400 focus:border-[#1a1a2e] focus:ring-1 focus:ring-[#1a1a2e]"
              required
              autoFocus
            />
          </div>

          <div>
            <label htmlFor="password" className="mb-1.5 block text-sm font-medium text-gray-700">
              Mat khau
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Nhap mat khau"
              className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm text-gray-900 outline-none transition-colors placeholder:text-gray-400 focus:border-[#1a1a2e] focus:ring-1 focus:ring-[#1a1a2e]"
              required
            />
          </div>

          {error && (
            <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">{error}</p>
          )}

          <button
            type="submit"
            disabled={isSubmitting || !username || !password}
            className="w-full rounded-lg bg-[#1a1a2e] px-4 py-2.5 text-sm font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50"
          >
            {isSubmitting ? "Dang dang nhap..." : "Dang nhap"}
          </button>
        </form>

        {/* Demo accounts info */}
        <div className="mt-6 rounded-lg border border-gray-100 bg-gray-50 p-4">
          <p className="mb-2 text-xs font-medium text-gray-500">Tai khoan demo:</p>
          <div className="space-y-1 text-xs text-gray-600">
            <p><span className="font-medium">Admin:</span> admin / admin123</p>
            <p><span className="font-medium">SV001:</span> sinhvien1 / sv001</p>
            <p><span className="font-medium">SV002:</span> sinhvien2 / sv002</p>
            <p><span className="font-medium">SV003:</span> sinhvien3 / sv003</p>
          </div>
        </div>
      </div>
    </div>
  );
}
