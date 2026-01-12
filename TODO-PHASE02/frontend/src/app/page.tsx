/**
 * Home page - Landing page with links to signin/signup.
 */
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-red-500 flex items-center justify-center px-4 animate-gradient">
      <div className="max-w-2xl w-full text-center">
        <div className="animate-bounce-slow mb-6">
          <div className="text-8xl mb-4">✨</div>
        </div>
        <h1 className="text-6xl font-bold text-white mb-4 animate-fade-in drop-shadow-2xl">
          Todo App
        </h1>
        <p className="text-2xl text-white font-semibold mb-8 animate-slide-in-left drop-shadow-lg">
          Phase II Full-Stack Web Application
        </p>
        <p className="text-white text-lg mb-12 animate-slide-in-right drop-shadow-md">
          A modern todo management application with user authentication and secure data isolation.
        </p>

        <div className="flex gap-4 justify-center animate-fade-in-up">
          <Link
            href="/signup"
            className="px-10 py-4 bg-white text-purple-600 rounded-2xl hover:bg-purple-50 hover:scale-110 focus:outline-none focus:ring-4 focus:ring-white transition-all duration-300 font-bold text-lg shadow-2xl transform hover:shadow-purple-300"
          >
            🚀 Get Started
          </Link>
          <Link
            href="/signin"
            className="px-10 py-4 bg-gradient-to-r from-yellow-400 to-orange-500 text-white border-2 border-white rounded-2xl hover:from-yellow-300 hover:to-orange-400 hover:scale-110 focus:outline-none focus:ring-4 focus:ring-white transition-all duration-300 font-bold text-lg shadow-2xl transform"
          >
            🔥 Sign In
          </Link>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white bg-opacity-20 backdrop-blur-lg p-6 rounded-2xl shadow-2xl hover:bg-opacity-30 transition-all duration-300 transform hover:scale-105 hover:-rotate-1 animate-slide-up border border-white border-opacity-30">
            <div className="text-yellow-300 text-5xl mb-3 animate-pulse">🔒</div>
            <h3 className="font-bold text-white text-xl mb-2 drop-shadow-lg">Secure</h3>
            <p className="text-sm text-white drop-shadow-md">
              JWT authentication with strict user isolation
            </p>
          </div>

          <div className="bg-white bg-opacity-20 backdrop-blur-lg p-6 rounded-2xl shadow-2xl hover:bg-opacity-30 transition-all duration-300 transform hover:scale-105 animate-slide-up-delay border border-white border-opacity-30">
            <div className="text-yellow-300 text-5xl mb-3 animate-pulse-delay">⚡</div>
            <h3 className="font-bold text-white text-xl mb-2 drop-shadow-lg">Fast</h3>
            <p className="text-sm text-white drop-shadow-md">
              Built with Next.js and FastAPI for optimal performance
            </p>
          </div>

          <div className="bg-white bg-opacity-20 backdrop-blur-lg p-6 rounded-2xl shadow-2xl hover:bg-opacity-30 transition-all duration-300 transform hover:scale-105 hover:rotate-1 animate-slide-up-delay-2 border border-white border-opacity-30">
            <div className="text-yellow-300 text-5xl mb-3 animate-pulse-delay-2">📱</div>
            <h3 className="font-bold text-white text-xl mb-2 drop-shadow-lg">Responsive</h3>
            <p className="text-sm text-white drop-shadow-md">
              Works seamlessly on desktop and mobile devices
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
