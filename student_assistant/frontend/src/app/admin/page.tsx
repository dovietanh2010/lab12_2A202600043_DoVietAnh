"use client";

import { useEffect, useState, useCallback } from "react";
import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";

interface DocumentMeta {
  doc_id: string;
  filename: string;
  title: string;
  category: string;
  upload_date: string;
  uploaded_by: string;
  page_count: number;
  chunk_count: number;
}

export default function AdminPage() {
  const { user, isLoading: authLoading, logout } = useAuth();
  const router = useRouter();
  const [documents, setDocuments] = useState<DocumentMeta[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState("");
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState("general");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const fetchDocuments = useCallback(async () => {
    try {
      const res = await fetch("/api/admin/documents", {
        headers: {
          Authorization: `Bearer ${user?.token ?? ""}`,
        },
      });
      if (res.status === 401) {
        logout();
        return;
      }
      if (res.ok) {
        const data = await res.json();
        setDocuments(data);
      }
    } catch {
      console.error("Failed to fetch documents");
    }
  }, [logout, user?.token]);

  useEffect(() => {
    if (!authLoading && user?.role === "admin") {
      fetchDocuments();
    }
  }, [authLoading, user, fetchDocuments]);

  // Redirect if not admin
  useEffect(() => {
    if (!authLoading && user && user.role !== "admin") {
      router.replace("/");
    }
  }, [authLoading, user, router]);

  if (authLoading || !user) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="h-6 w-6 animate-spin rounded-full border-2 border-gray-300 border-t-[#1a1a2e]" />
      </div>
    );
  }

  if (user.role !== "admin") {
    return null;
  }

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;

    setIsUploading(true);
    setUploadStatus("Dang xu ly PDF va embedding... Vui long doi.");

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
      if (title) formData.append("title", title);
      formData.append("category", category);

      const res = await fetch("/api/admin/documents/upload", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${user.token}`,
        },
        body: formData,
      });

      if (res.status === 401) {
        logout();
        return;
      }

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail || "Upload that bai");
      }

      const doc = await res.json();
      setUploadStatus(
        `Thanh cong! Da xu ly ${doc.chunk_count} phan tu ${doc.page_count} trang.`
      );
      setTitle("");
      setCategory("general");
      setSelectedFile(null);
      // Reset file input
      const fileInput = document.getElementById("pdf-file") as HTMLInputElement;
      if (fileInput) fileInput.value = "";
      fetchDocuments();
    } catch (err: any) {
      setUploadStatus(`Loi: ${err.message}`);
    } finally {
      setIsUploading(false);
    }
  };

  const handleDelete = async (docId: string) => {
    if (!confirm("Ban co chac muon xoa tai lieu nay?")) return;

    setDeletingId(docId);
    try {
      const res = await fetch(`/api/admin/documents/${docId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${user.token}`,
        },
      });
      if (res.status === 401) {
        logout();
        return;
      }
      if (res.ok) {
        fetchDocuments();
      }
    } catch {
      alert("Xoa that bai");
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="flex min-h-screen flex-col bg-white">
      {/* Header */}
      <header className="flex items-center justify-between border-b border-gray-100 px-4 py-3 sm:px-6">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#1a1a2e] text-xs font-semibold text-white">
            SA
          </div>
          <span className="text-sm font-medium text-gray-900">
            Student Assistant{" "}
            <span className="text-gray-400">/ Admin</span>
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-amber-50 px-2.5 py-1 text-xs font-medium text-amber-700">
            {user.display_name}
          </span>
          <button
            onClick={() => router.push("/")}
            className="rounded-lg border border-gray-200 px-3 py-1.5 text-xs font-medium text-gray-600 transition-colors hover:bg-gray-50"
          >
            Chat
          </button>
          <button
            onClick={logout}
            className="rounded-lg border border-gray-200 px-3 py-1.5 text-xs font-medium text-red-500 transition-colors hover:bg-red-50"
          >
            Dang xuat
          </button>
        </div>
      </header>

      <div className="mx-auto w-full max-w-4xl flex-1 px-4 py-6 sm:px-6">
        {/* Upload section */}
        <section className="mb-8">
          <h2 className="mb-4 text-lg font-semibold text-gray-900">
            Upload tai lieu PDF
          </h2>
          <form
            onSubmit={handleUpload}
            className="rounded-xl border border-gray-200 bg-gray-50 p-5"
          >
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="sm:col-span-2">
                <label htmlFor="pdf-file" className="mb-1.5 block text-sm font-medium text-gray-700">
                  File PDF
                </label>
                <input
                  id="pdf-file"
                  type="file"
                  accept=".pdf"
                  onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                  className="w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm text-gray-700 file:mr-3 file:rounded-md file:border-0 file:bg-[#1a1a2e] file:px-3 file:py-1 file:text-sm file:text-white"
                  required
                  disabled={isUploading}
                />
              </div>

              <div>
                <label htmlFor="title" className="mb-1.5 block text-sm font-medium text-gray-700">
                  Tieu de (tuy chon)
                </label>
                <input
                  id="title"
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="De trong se dung ten file"
                  className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-[#1a1a2e]"
                  disabled={isUploading}
                />
              </div>

              <div>
                <label htmlFor="category" className="mb-1.5 block text-sm font-medium text-gray-700">
                  Danh muc
                </label>
                <select
                  id="category"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-[#1a1a2e]"
                  disabled={isUploading}
                >
                  <option value="general">Chung</option>
                  <option value="quy_che">Quy che</option>
                  <option value="thong_bao">Thong bao</option>
                  <option value="huong_dan">Huong dan</option>
                </select>
              </div>
            </div>

            <div className="mt-4 flex items-center gap-4">
              <button
                type="submit"
                disabled={isUploading || !selectedFile}
                className="rounded-lg bg-[#1a1a2e] px-5 py-2.5 text-sm font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50"
              >
                {isUploading ? "Dang xu ly..." : "Upload va Embedding"}
              </button>
              {uploadStatus && (
                <p className={`text-sm ${uploadStatus.startsWith("Loi") ? "text-red-500" : uploadStatus.startsWith("Thanh cong") ? "text-emerald-600" : "text-amber-600"}`}>
                  {uploadStatus}
                </p>
              )}
            </div>
          </form>
        </section>

        {/* Document list */}
        <section>
          <h2 className="mb-4 text-lg font-semibold text-gray-900">
            Tai lieu da upload ({documents.length})
          </h2>

          {documents.length === 0 ? (
            <div className="rounded-xl border border-dashed border-gray-200 py-12 text-center">
              <p className="text-sm text-gray-400">Chua co tai lieu nao. Upload file PDF o tren.</p>
            </div>
          ) : (
            <div className="overflow-hidden rounded-xl border border-gray-200">
              <table className="w-full text-left text-sm">
                <thead className="border-b border-gray-100 bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 font-medium text-gray-600">Tieu de</th>
                    <th className="px-4 py-3 font-medium text-gray-600">File</th>
                    <th className="px-4 py-3 font-medium text-gray-600 text-center">Trang</th>
                    <th className="px-4 py-3 font-medium text-gray-600 text-center">Chunks</th>
                    <th className="px-4 py-3 font-medium text-gray-600">Ngay upload</th>
                    <th className="px-4 py-3 font-medium text-gray-600 text-center">Thao tac</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                  {documents.map((doc) => (
                    <tr key={doc.doc_id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 font-medium text-gray-900">
                        <a
                          href={`/uploads/${doc.doc_id}.pdf`}
                          target="_blank"
                          rel="noreferrer"
                          className="text-blue-600 hover:underline"
                        >
                          {doc.title}
                        </a>
                      </td>
                      <td className="px-4 py-3 text-gray-500">{doc.filename}</td>
                      <td className="px-4 py-3 text-center text-gray-500">{doc.page_count}</td>
                      <td className="px-4 py-3 text-center text-gray-500">{doc.chunk_count}</td>
                      <td className="px-4 py-3 text-gray-500">
                        {new Date(doc.upload_date).toLocaleDateString("vi-VN")}
                      </td>
                      <td className="px-4 py-3 text-center">
                        <button
                          onClick={() => handleDelete(doc.doc_id)}
                          disabled={deletingId === doc.doc_id}
                          className="rounded-md px-2 py-1 text-xs font-medium text-red-500 transition-colors hover:bg-red-50 disabled:opacity-50"
                        >
                          {deletingId === doc.doc_id ? "Dang xoa..." : "Xoa"}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
