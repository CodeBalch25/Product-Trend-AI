import { useState } from 'react';
import Head from 'next/head';
import useSWR from 'swr';
import { toast } from 'react-hot-toast';
import { analyticsApi, mlApi } from '@/services/api';
import Layout from '@/components/Layout';

export default function Analytics() {
  const [isTraining, setIsTraining] = useState(false);

  const { data: rejectionData, error } = useSWR('/api/analytics/rejections', () =>
    analyticsApi.getRejections().then(res => res.data)
  );

  const { data: mlStatus, mutate: mutateMLStatus } = useSWR('/api/ml/status', () =>
    mlApi.getStatus().then(res => res.data)
  );

  const handleTrainModel = async () => {
    try {
      setIsTraining(true);
      const response = await mlApi.trainModel();
      toast.success(response.data.message);
      mutateMLStatus(); // Refresh ML status
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Failed to train model');
    } finally {
      setIsTraining(false);
    }
  };

  if (error) {
    return (
      <Layout>
        <div className="card bg-red-50">
          <p className="text-red-800">Failed to load analytics data</p>
        </div>
      </Layout>
    );
  }

  if (!rejectionData) {
    return (
      <Layout>
        <div className="card">
          <p className="text-gray-500">Loading analytics...</p>
        </div>
      </Layout>
    );
  }

  const { overall, rejection_by_reason, rejection_by_score_range, rejection_by_source, insights } = rejectionData;

  return (
    <Layout>
      <Head>
        <title>AI Learning Analytics - Product Trend Automation</title>
      </Head>

      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">AI Learning Analytics</h1>
          <p className="text-gray-500 mt-1">
            Track rejection patterns to improve AI performance
          </p>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="card">
            <p className="text-sm text-gray-500">Total Products</p>
            <p className="text-3xl font-bold text-gray-900">{overall.total_products}</p>
          </div>
          <div className="card">
            <p className="text-sm text-gray-500">Rejection Rate</p>
            <p className="text-3xl font-bold text-red-600">{overall.rejection_rate}%</p>
          </div>
          <div className="card">
            <p className="text-sm text-gray-500">Approval Rate</p>
            <p className="text-3xl font-bold text-green-600">{overall.approval_rate}%</p>
          </div>
          <div className="card">
            <p className="text-sm text-gray-500">Total Rejected</p>
            <p className="text-3xl font-bold text-orange-600">{overall.total_rejected}</p>
          </div>
        </div>

        {/* AI Insights */}
        {insights && insights.length > 0 && (
          <div className="card">
            <h2 className="text-xl font-bold mb-4">🧠 AI Insights & Recommendations</h2>
            <div className="space-y-3">
              {insights.map((insight: any, idx: number) => (
                <div
                  key={idx}
                  className={`p-4 rounded-lg border-2 ${
                    insight.type === 'warning'
                      ? 'bg-yellow-50 border-yellow-300'
                      : insight.type === 'success'
                      ? 'bg-green-50 border-green-300'
                      : 'bg-blue-50 border-blue-300'
                  }`}
                >
                  <p className="font-bold text-gray-900">{insight.title}</p>
                  <p className="text-gray-700 mt-1">{insight.message}</p>
                  <p className="text-sm text-gray-600 mt-2">
                    <strong>Recommended Action:</strong> {insight.action}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Rejection by Reason */}
        <div className="card">
          <h2 className="text-xl font-bold mb-4">📊 Rejection Reasons Distribution</h2>
          {Object.keys(rejection_by_reason).length > 0 ? (
            <div className="space-y-3">
              {Object.entries(rejection_by_reason)
                .sort((a: any, b: any) => b[1] - a[1])
                .map(([reason, count]: any) => {
                  const percentage = ((count / overall.total_rejected) * 100).toFixed(1);
                  const reasonName = reason.split('_').map((w: string) =>
                    w.charAt(0).toUpperCase() + w.slice(1)
                  ).join(' ');

                  return (
                    <div key={reason}>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-medium text-gray-700">{reasonName}</span>
                        <span className="text-sm font-bold text-gray-900">
                          {count} ({percentage}%)
                        </span>
                      </div>
                      <div className="h-6 bg-gray-200 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-red-500 to-red-600 transition-all duration-300"
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              <div className="mt-4 pt-3 border-t border-gray-200">
                <p className="text-xs text-gray-500">
                  💡 All percentages sum to 100% of total rejections ({overall.total_rejected})
                </p>
              </div>
            </div>
          ) : (
            <p className="text-gray-500">No rejections yet - keep reviewing products!</p>
          )}
        </div>

        {/* Rejection by Trend Score Range */}
        <div className="card">
          <h2 className="text-xl font-bold mb-4">📈 Rejection Rate by Trend Score</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {Object.entries(rejection_by_score_range).map(([range, data]: any) => (
              <div key={range} className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm font-bold text-gray-600">Score {range}</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">{data.total} products</p>
                <p className="text-sm text-gray-600 mt-1">
                  {data.rejected} rejected
                </p>
                <div className="mt-2">
                  <div className="h-2 bg-gray-300 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${
                        data.rejection_rate > 70
                          ? 'bg-red-500'
                          : data.rejection_rate > 40
                          ? 'bg-yellow-500'
                          : 'bg-green-500'
                      }`}
                      style={{ width: `${data.rejection_rate}%` }}
                    />
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    {data.rejection_rate.toFixed(1)}% rejection rate
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Rejection by Source */}
        <div className="card">
          <h2 className="text-xl font-bold mb-4">🔍 Source Performance</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b-2 border-gray-200">
                  <th className="text-left py-2 px-4">Source</th>
                  <th className="text-right py-2 px-4">Total</th>
                  <th className="text-right py-2 px-4">Rejected</th>
                  <th className="text-right py-2 px-4">Approved</th>
                  <th className="text-right py-2 px-4">Rejection Rate</th>
                  <th className="text-right py-2 px-4">Approval Rate</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(rejection_by_source)
                  .sort((a: any, b: any) => b[1].rejection_rate - a[1].rejection_rate)
                  .map(([source, data]: any) => (
                    <tr key={source} className="border-b border-gray-100">
                      <td className="py-3 px-4 font-medium">{source}</td>
                      <td className="py-3 px-4 text-right">{data.total}</td>
                      <td className="py-3 px-4 text-right text-red-600">{data.rejected}</td>
                      <td className="py-3 px-4 text-right text-green-600">{data.approved}</td>
                      <td className="py-3 px-4 text-right">
                        <span
                          className={`px-2 py-1 rounded text-sm font-bold ${
                            data.rejection_rate > 60
                              ? 'bg-red-100 text-red-800'
                              : data.rejection_rate > 40
                              ? 'bg-yellow-100 text-yellow-800'
                              : 'bg-green-100 text-green-800'
                          }`}
                        >
                          {data.rejection_rate.toFixed(1)}%
                        </span>
                      </td>
                      <td className="py-3 px-4 text-right">
                        <span className="text-green-600 font-bold">
                          {data.approval_rate.toFixed(1)}%
                        </span>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Learning Progress */}
        <div className="card bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-200">
          <h2 className="text-xl font-bold mb-4">🎓 AI Learning Progress</h2>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium text-gray-700">Data Collection</span>
                <span className="text-sm font-bold text-blue-600">
                  {overall.total_products > 50 ? '100%' : `${(overall.total_products / 50 * 100).toFixed(0)}%`}
                </span>
              </div>
              <div className="h-3 bg-gray-200 rounded-full">
                <div
                  className="h-full bg-blue-600 rounded-full"
                  style={{ width: `${Math.min((overall.total_products / 50) * 100, 100)}%` }}
                />
              </div>
              <p className="text-xs text-gray-600 mt-1">
                {overall.total_products}/50 products reviewed (need 50 for ML training)
              </p>
            </div>

            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium text-gray-700">Rejection Feedback</span>
                <span className="text-sm font-bold text-purple-600">
                  {overall.total_rejected > 20 ? '100%' : `${(overall.total_rejected / 20 * 100).toFixed(0)}%`}
                </span>
              </div>
              <div className="h-3 bg-gray-200 rounded-full">
                <div
                  className="h-full bg-purple-600 rounded-full"
                  style={{ width: `${Math.min((overall.total_rejected / 20) * 100, 100)}%` }}
                />
              </div>
              <p className="text-xs text-gray-600 mt-1">
                {overall.total_rejected}/20 rejections (need 20 for pattern analysis)
              </p>
            </div>

            {overall.total_products >= 50 && overall.total_rejected >= 20 && (
              <div className="mt-4 p-4 bg-green-100 border-2 border-green-400 rounded-lg">
                <p className="font-bold text-green-800">✅ Ready for ML Training!</p>
                <p className="text-sm text-green-700 mt-1">
                  You have enough data to train the AI predictor model (Phase 4)
                </p>
              </div>
            )}
          </div>
        </div>

        {/* ML Model Training */}
        <div className="card bg-gradient-to-r from-purple-50 to-pink-50 border-2 border-purple-200">
          <h2 className="text-xl font-bold mb-4">🤖 ML Model Training</h2>

          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-bold text-gray-900">
                  Model Status: {mlStatus?.trained ? (
                    <span className="text-green-600">✅ Trained</span>
                  ) : (
                    <span className="text-orange-600">⏳ Not Trained</span>
                  )}
                </p>
                <p className="text-sm text-gray-600 mt-1">
                  {mlStatus?.trained
                    ? 'ML model is ready to predict product approvals'
                    : 'Train the model to enable smart predictions'}
                </p>
              </div>

              <button
                onClick={handleTrainModel}
                disabled={isTraining || overall.total_products < 20}
                className={`px-6 py-3 rounded-lg font-bold text-white transition-colors ${
                  isTraining || overall.total_products < 20
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700'
                }`}
              >
                {isTraining ? '🔄 Training...' : '🎓 Train ML Model'}
              </button>
            </div>

            {overall.total_products < 20 && (
              <div className="p-3 bg-yellow-100 border border-yellow-300 rounded-lg">
                <p className="text-sm text-yellow-800">
                  ⚠️ Need at least 20 products with approval/rejection data to train the model.
                  Current: {overall.total_products} products.
                </p>
              </div>
            )}

            {mlStatus?.trained && (
              <div className="p-4 bg-green-50 border-2 border-green-300 rounded-lg">
                <p className="font-bold text-green-800">🚀 Phase 4 Complete!</p>
                <p className="text-sm text-green-700 mt-1">
                  ML model will now predict approval probability for new products.
                  Next: Implement Phase 5 for auto-approval of high-confidence predictions.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}
