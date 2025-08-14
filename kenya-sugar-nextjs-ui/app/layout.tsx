import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Kenya Sugar Board Analysis System',
  description: 'AI-Powered Data Analysis with Conversation Memory for Kenya Sugar Industry',
  keywords: 'Kenya, Sugar, Analysis, AI, Data Science, Sugar Industry',
  authors: [{ name: 'Kenya Sugar Board Analysis Team' }],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} antialiased`}>
        <div className="min-h-screen bg-sugar-gradient">
          {children}
        </div>
      </body>
    </html>
  );
}