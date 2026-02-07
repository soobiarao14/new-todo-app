"use client";

/**
 * Signin page for existing user authentication.
 */
import { useState, FormEvent } from "react";
import { useAuth } from "@/contexts/AuthContext";
import Link from "next/link";

export default function SigninPage() {
  const { signIn, loading, error } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    try {
      await signIn(email, password);
    } catch (err) {
      // Error handled by AuthContext
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-400 via-purple-500 to-pink-500 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white bg-opacity-95 backdrop-blur-lg p-10 rounded-3xl shadow-2xl animate-slide-up">
        <div className="animate-fade-in">
          <div className="text-center text-6xl mb-4 animate-bounce-slow">🔐</div>
          <h2 className="mt-6 text-center text-4xl font-extrabold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Welcome Back!
          </h2>
          <p className="mt-2 text-center text-sm text-gray-700">
            Don't have an account?{" "}
            <Link
              href="/signup"
              className="font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transition-all"
            >
              Create one here ✨
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6 animate-fade-in-up" onSubmit={handleSubmit}>
          <div className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-bold text-gray-700 mb-2">
                📧 Email address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="appearance-none relative block w-full px-4 py-3 border-2 border-blue-300 placeholder-gray-400 text-gray-900 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-300 focus:border-blue-500 transition-all duration-300 sm:text-sm"
                placeholder="Enter your email"
              />
            </div>
            <div>
              <label htmlFor="password" className="block text-sm font-bold text-gray-700 mb-2">
                🔒 Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="appearance-none relative block w-full px-4 py-3 border-2 border-blue-300 placeholder-gray-400 text-gray-900 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-300 focus:border-blue-500 transition-all duration-300 sm:text-sm"
                placeholder="Enter your password"
              />
            </div>
          </div>

          {error && (
            <div className="rounded-2xl bg-gradient-to-r from-red-100 to-pink-100 border-2 border-red-400 p-4 animate-shake">
              <p className="text-sm text-red-800 font-bold">❌ {error}</p>
            </div>
          )}

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-4 px-4 border border-transparent text-lg font-bold rounded-2xl text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-4 focus:ring-blue-300 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-300 shadow-xl"
            >
              {loading ? "✨ Signing in..." : "🚀 Sign in"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
