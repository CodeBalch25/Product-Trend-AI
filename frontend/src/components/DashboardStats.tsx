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
      <div className="card">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-500">Total Products</p>
            <p className="text-3xl font-bold text-gray-900 mt-1">
              {stats.total_products}
            </p>
          </div>
          <div className="bg-blue-100 p-3 rounded-full">
            <svg
              className="w-6 h-6 text-blue-600"
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
      </div>

      {/* Pending Review */}
      <div className="card">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-500">Pending Review</p>
            <p className="text-3xl font-bold text-yellow-600 mt-1">
              {stats.pending_review}
            </p>
          </div>
          <div className="bg-yellow-100 p-3 rounded-full">
            <svg
              className="w-6 h-6 text-yellow-600"
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
      </div>

      {/* Approved */}
      <div className="card">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-500">Approved</p>
            <p className="text-3xl font-bold text-green-600 mt-1">
              {stats.approved}
            </p>
          </div>
          <div className="bg-green-100 p-3 rounded-full">
            <svg
              className="w-6 h-6 text-green-600"
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
      </div>

      {/* Posted */}
      <div className="card">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-500">Posted</p>
            <p className="text-3xl font-bold text-primary-600 mt-1">
              {stats.posted}
            </p>
          </div>
          <div className="bg-primary-100 p-3 rounded-full">
            <svg
              className="w-6 h-6 text-primary-600"
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
      </div>

      {/* Platform Stats */}
      {Object.keys(stats.platform_stats).length > 0 && (
        <div className="card col-span-full">
          <h3 className="text-lg font-semibold mb-4">Platform Performance</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
            {Object.entries(stats.platform_stats).map(([platform, data]) => (
              <div key={platform} className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-500 capitalize">
                  {platform.replace('_', ' ')}
                </p>
                <p className="text-2xl font-bold text-gray-900 mt-1">
                  {data.count}
                </p>
                <p className="text-sm text-green-600 mt-1">
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
