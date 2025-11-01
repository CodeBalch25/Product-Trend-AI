interface DashboardStatsProps {
  stats: {
    total_products: number;
    pending_review: number;
    approved: number;
    posted: number;
    platform_stats: Record<string, { count: number; revenue: number }>;
  };
}

export default function DashboardStats({ stats }: DashboardStatsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {/* Total Products */}
      <div className="gradient-card from-blue-500 to-cyan-500 group">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-white/90">Total Products</p>
            <p className="text-4xl font-bold text-white mt-2">
              {stats.total_products}
            </p>
          </div>
          <div className="bg-white/20 backdrop-blur-sm p-4 rounded-2xl group-hover:scale-110 transition-transform duration-300">
            <svg
              className="w-8 h-8 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
              />
            </svg>
          </div>
        </div>
        <div className="absolute bottom-0 right-0 w-32 h-32 bg-white/10 rounded-full blur-3xl"></div>
      </div>

      {/* Pending Review */}
      <div className="gradient-card from-amber-500 to-orange-500 group">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-white/90">Pending Review</p>
            <p className="text-4xl font-bold text-white mt-2">
              {stats.pending_review}
            </p>
          </div>
          <div className="bg-white/20 backdrop-blur-sm p-4 rounded-2xl group-hover:scale-110 transition-transform duration-300">
            <svg
              className="w-8 h-8 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
        </div>
        <div className="absolute bottom-0 right-0 w-32 h-32 bg-white/10 rounded-full blur-3xl"></div>
      </div>

      {/* Approved */}
      <div className="gradient-card from-emerald-500 to-teal-500 group">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-white/90">Approved</p>
            <p className="text-4xl font-bold text-white mt-2">
              {stats.approved}
            </p>
          </div>
          <div className="bg-white/20 backdrop-blur-sm p-4 rounded-2xl group-hover:scale-110 transition-transform duration-300">
            <svg
              className="w-8 h-8 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
        </div>
        <div className="absolute bottom-0 right-0 w-32 h-32 bg-white/10 rounded-full blur-3xl"></div>
      </div>

      {/* Posted */}
      <div className="gradient-card from-violet-600 to-indigo-600 group">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-white/90">Posted</p>
            <p className="text-4xl font-bold text-white mt-2">
              {stats.posted}
            </p>
          </div>
          <div className="bg-white/20 backdrop-blur-sm p-4 rounded-2xl group-hover:scale-110 transition-transform duration-300">
            <svg
              className="w-8 h-8 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
          </div>
        </div>
        <div className="absolute bottom-0 right-0 w-32 h-32 bg-white/10 rounded-full blur-3xl"></div>
      </div>

      {/* Platform Stats */}
      {Object.keys(stats.platform_stats).length > 0 && (
        <div className="card col-span-full">
          <h3 className="text-xl font-bold text-slate-800 mb-6 text-gradient from-violet-600 to-indigo-600">
            Platform Performance
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
            {Object.entries(stats.platform_stats).map(([platform, data]) => (
              <div
                key={platform}
                className="relative overflow-hidden bg-gradient-to-br from-slate-50 to-slate-100 p-5 rounded-2xl border border-slate-200/60 hover:shadow-lg hover:scale-105 transition-all duration-300 group"
              >
                <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-violet-500/10 to-indigo-500/10 rounded-full blur-2xl group-hover:scale-150 transition-transform duration-500"></div>
                <p className="text-sm text-slate-600 capitalize font-medium relative">
                  {platform.replace('_', ' ')}
                </p>
                <p className="text-3xl font-bold text-slate-900 mt-2 relative">
                  {data.count}
                </p>
                <p className="text-sm font-semibold text-emerald-600 mt-2 relative">
                  ${data.revenue.toFixed(2)}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
