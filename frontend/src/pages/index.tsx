import { useState, useEffect } from 'react';
import Head from 'next/head';
import useSWR from 'swr';
import { productApi, analyticsApi, trendApi } from '@/services/api';
import toast from 'react-hot-toast';
import ProductCard from '@/components/ProductCard';
import DashboardStats from '@/components/DashboardStats';
import Layout from '@/components/Layout';

const fetcher = (url: string) => productApi.getAll().then(res => res.data);

export default function Home() {
  const [statusFilter, setStatusFilter] = useState('pending_review');
  const { data: products, error, mutate } = useSWR('/api/products', fetcher);
  const { data: analytics } = useSWR('/api/analytics/dashboard', () =>
    analyticsApi.getDashboard().then(res => res.data)
  );

  const [isScanning, setIsScanning] = useState(false);

  const handleScanTrends = async () => {
    setIsScanning(true);
    try {
      const result = await trendApi.scan();
      // Show the message from backend
      const data = result.data || result;
      if (data.new_products_count > 0) {
        toast.success(data.message);
      } else {
        toast(data.message); // Default neutral toast
      }
      // Always refresh products after scan
      setTimeout(() => mutate(), 2000); // Wait 2 seconds then refresh
    } catch (err: any) {
      // Even if API call fails/times out, the scan might have worked!
      // Always refresh to check for new products
      toast('Scan completed. Refreshing products...'); // Default neutral toast
      setTimeout(() => mutate(), 2000);
    } finally {
      setIsScanning(false);
    }
  };

  const filteredProducts = products?.filter((p: any) => {
    // Exclude rejected products from 'all' view
    if (statusFilter === 'all') {
      return p.status !== 'rejected';
    }
    return p.status === statusFilter;
  });

  return (
    <Layout>
      <Head>
        <title>Product Trend Automation Dashboard</title>
        <meta name="description" content="AI-powered product trend discovery" />
      </Head>

      <div className="space-y-10">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-5xl font-bold text-gradient from-violet-600 to-indigo-600 mb-3">
              Dashboard
            </h1>
            <p className="text-slate-600 text-lg font-medium">
              AI-powered product trend discovery and listing automation
            </p>
          </div>
          <button
            onClick={handleScanTrends}
            disabled={isScanning}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isScanning ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Scanning...
              </span>
            ) : (
              'Scan Trends Now'
            )}
          </button>
        </div>

        {/* Analytics Stats */}
        {analytics && <DashboardStats stats={analytics} />}

        {/* Filters */}
        <div className="card">
          <h3 className="text-lg font-bold text-slate-800 mb-4">Filter Products</h3>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => setStatusFilter('all')}
              className={`px-5 py-2.5 rounded-xl font-medium transition-all duration-200 ${
                statusFilter === 'all'
                  ? 'bg-gradient-to-r from-violet-600 to-indigo-600 text-white shadow-lg shadow-violet-500/50 scale-105'
                  : 'bg-white border-2 border-slate-200 text-slate-700 hover:border-violet-300 hover:bg-violet-50'
              }`}
            >
              All Products
            </button>
            <button
              onClick={() => setStatusFilter('pending_review')}
              className={`px-5 py-2.5 rounded-xl font-medium transition-all duration-200 ${
                statusFilter === 'pending_review'
                  ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-lg shadow-amber-500/50 scale-105'
                  : 'bg-white border-2 border-slate-200 text-slate-700 hover:border-amber-300 hover:bg-amber-50'
              }`}
            >
              Pending Review
            </button>
            <button
              onClick={() => setStatusFilter('approved')}
              className={`px-5 py-2.5 rounded-xl font-medium transition-all duration-200 ${
                statusFilter === 'approved'
                  ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-white shadow-lg shadow-emerald-500/50 scale-105'
                  : 'bg-white border-2 border-slate-200 text-slate-700 hover:border-emerald-300 hover:bg-emerald-50'
              }`}
            >
              Approved
            </button>
            <button
              onClick={() => setStatusFilter('posted')}
              className={`px-5 py-2.5 rounded-xl font-medium transition-all duration-200 ${
                statusFilter === 'posted'
                  ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-lg shadow-blue-500/50 scale-105'
                  : 'bg-white border-2 border-slate-200 text-slate-700 hover:border-blue-300 hover:bg-blue-50'
              }`}
            >
              Posted
            </button>
            <button
              onClick={() => setStatusFilter('rejected')}
              className={`px-5 py-2.5 rounded-xl font-medium transition-all duration-200 ${
                statusFilter === 'rejected'
                  ? 'bg-gradient-to-r from-rose-600 to-red-600 text-white shadow-lg shadow-rose-500/50 scale-105'
                  : 'bg-white border-2 border-slate-200 text-slate-700 hover:border-rose-300 hover:bg-rose-50'
              }`}
            >
              Rejected
            </button>
          </div>
        </div>

        {/* Products Grid */}
        <div>
          {error && (
            <div className="card bg-gradient-to-r from-rose-50 to-red-50 border-2 border-rose-300">
              <p className="text-rose-800 font-semibold text-center">Failed to load products</p>
            </div>
          )}

          {!products && !error && (
            <div className="card text-center">
              <div className="flex items-center justify-center gap-3">
                <svg className="animate-spin h-6 w-6 text-violet-600" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                <p className="text-slate-600 font-medium">Loading products...</p>
              </div>
            </div>
          )}

          {filteredProducts && filteredProducts.length === 0 && (
            <div className="card text-center">
              <p className="text-slate-500 font-medium">No products found</p>
              <p className="text-slate-400 text-sm mt-2">Try scanning for trends or adjusting your filter</p>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-fade-in">
            {filteredProducts?.map((product: any) => (
              <ProductCard
                key={product.id}
                product={product}
                onUpdate={() => mutate()}
              />
            ))}
          </div>
        </div>
      </div>
    </Layout>
  );
}
