"use client";

/**
 * StatsCard component for displaying dashboard metrics.
 * Phase III: Todo AI Chatbot - NEW FILE (does not modify Phase II)
 */

interface StatsCardProps {
  title: string;
  value: number;
  icon: string;
  color: "purple" | "green" | "orange" | "blue" | "pink";
  subtitle?: string;
}

const colorClasses = {
  purple: {
    bg: "bg-gradient-to-br from-purple-500 to-purple-600",
    light: "bg-purple-100",
    text: "text-purple-600",
  },
  green: {
    bg: "bg-gradient-to-br from-green-500 to-green-600",
    light: "bg-green-100",
    text: "text-green-600",
  },
  orange: {
    bg: "bg-gradient-to-br from-orange-500 to-orange-600",
    light: "bg-orange-100",
    text: "text-orange-600",
  },
  blue: {
    bg: "bg-gradient-to-br from-blue-500 to-blue-600",
    light: "bg-blue-100",
    text: "text-blue-600",
  },
  pink: {
    bg: "bg-gradient-to-br from-pink-500 to-pink-600",
    light: "bg-pink-100",
    text: "text-pink-600",
  },
};

export default function StatsCard({
  title,
  value,
  icon,
  color,
  subtitle,
}: StatsCardProps) {
  const colors = colorClasses[color];

  return (
    <div className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden">
      <div className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-500 uppercase tracking-wider">
              {title}
            </p>
            <p className="mt-2 text-4xl font-bold text-gray-900">{value}</p>
            {subtitle && (
              <p className="mt-1 text-sm text-gray-500">{subtitle}</p>
            )}
          </div>
          <div
            className={`p-4 rounded-2xl ${colors.light} shadow-inner`}
          >
            <span className="text-3xl">{icon}</span>
          </div>
        </div>
      </div>
      <div className={`h-1.5 ${colors.bg}`} />
    </div>
  );
}
