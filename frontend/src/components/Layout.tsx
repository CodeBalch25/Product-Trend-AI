import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const router = useRouter();

  const isActive = (path: string) => router.pathname === path;

  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="glass sticky top-0 z-50 border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-20">
            <div className="flex items-center">
              <Link href="/" className="flex items-center group">
                <div className="relative">
                  <div className="absolute -inset-2 bg-gradient-to-r from-violet-600 to-indigo-600 rounded-lg opacity-20 blur group-hover:opacity-30 transition-opacity"></div>
                  <span className="relative text-3xl font-bold text-gradient from-violet-600 to-indigo-600">
                    UltraThink
                  </span>
                </div>
                <span className="ml-3 text-sm text-slate-500 font-medium hidden lg:block">
                  AI Trend Discovery
                </span>
              </Link>
              <div className="ml-12 flex items-center space-x-2">
                <Link
                  href="/"
                  className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                    isActive('/')
                      ? 'bg-gradient-to-r from-violet-600 to-indigo-600 text-white shadow-lg shadow-violet-500/50'
                      : 'text-slate-700 hover:bg-white/60 hover:text-violet-600'
                  }`}
                >
                  Dashboard
                </Link>
                <Link
                  href="/products"
                  className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                    isActive('/products')
                      ? 'bg-gradient-to-r from-violet-600 to-indigo-600 text-white shadow-lg shadow-violet-500/50'
                      : 'text-slate-700 hover:bg-white/60 hover:text-violet-600'
                  }`}
                >
                  Products
                </Link>
                <Link
                  href="/analytics"
                  className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                    isActive('/analytics')
                      ? 'bg-gradient-to-r from-violet-600 to-indigo-600 text-white shadow-lg shadow-violet-500/50'
                      : 'text-slate-700 hover:bg-white/60 hover:text-violet-600'
                  }`}
                >
                  Analytics
                </Link>
                <Link
                  href="/settings"
                  className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                    isActive('/settings')
                      ? 'bg-gradient-to-r from-violet-600 to-indigo-600 text-white shadow-lg shadow-violet-500/50'
                      : 'text-slate-700 hover:bg-white/60 hover:text-violet-600'
                  }`}
                >
                  Settings
                </Link>
              </div>
            </div>
            <div className="flex items-center">
              <div className="relative">
                <div className="absolute -inset-1 bg-gradient-to-r from-violet-600 to-indigo-600 rounded-full opacity-20 blur"></div>
                <div className="relative w-10 h-10 bg-gradient-to-r from-violet-600 to-indigo-600 rounded-full flex items-center justify-center text-white font-bold shadow-lg">
                  AI
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 animate-fade-in">
        {children}
      </main>

      {/* Footer */}
      <footer className="glass border-t border-white/20 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <p className="text-center text-slate-600 text-sm font-medium">
            UltraThink AI - Next-Generation Product Discovery
          </p>
          <p className="text-center text-slate-400 text-xs mt-2">
            Powered by advanced AI to discover trending products automatically
          </p>
        </div>
      </footer>
    </div>
  );
}
