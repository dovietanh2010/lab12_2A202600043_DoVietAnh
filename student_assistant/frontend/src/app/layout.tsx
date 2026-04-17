import type { Metadata } from "next";
import { AuthProvider } from "@/lib/auth-context";
import "./globals.css";

export const metadata: Metadata = {
  title: "Student Assistant - Tro ly Sinh vien",
  description: "He thong tro ly thong minh ho tro sinh vien tra cuu thong tin hoc vu",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi">
      <body className="text-[#17313b] antialiased">
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
