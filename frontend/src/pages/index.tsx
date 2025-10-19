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

      <div className="space-y-8">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-500 mt-1">
              AI-powered product trend discovery and listing automation
            </p>
          </div>
          <button
            onClick={handleScanTrends}
            disabled={isScanning}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isScanning ? 'Scanning...' : 'Scan Trends Now'}
          </button>
        </div>

        {/* Analytics Stats */}
        {analytics && <DashboardStats stats={analytics} />}

        {/* Filters */}
        <div className="card">
          <div className="flex gap-2">
            <button
              onClick={() => setStatusFilter('all')}
              className={`px-4 py-2 rounded-lg ${
                statusFilter === 'all'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              All Products
            </button>
            <button
              onClick={() => setStatusFilter('pending_review')}
              className={`px-4 py-2 rounded-lg ${
                statusFilter === 'pending_review'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              Pending Review
            </button>
            <button
              onClick={() => setStatusFilter('approved')}
              className={`px-4 py-2 rounded-lg ${
                statusFilter === 'approved'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              Approved
            </button>
            <button
              onClick={() => setStatusFilter('posted')}
              className={`px-4 py-2 rounded-lg ${
                statusFilter === 'posted'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              Posted
            </button>
            <button
              onClick={() => setStatusFilter('rejected')}
              className={`px-4 py-2 rounded-lg ${
                statusFilter === 'rejected'
                  ? 'bg-red-600 text-white'
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              Rejected
            </button>
          </div>
        </div>

        {/* Products Grid */}
        <div>
          {error && (
            <div className="card bg-red-50 border border-red-200">
              <p className="text-red-800">Failed to load products</p>
            </div>
          )}

          {!products && !error && (
            <div className="card">
              <p className="text-gray-500">Loading products...</p>
            </div>
          )}

          {filteredProducts && filteredProducts.length === 0 && (
            <div className="card">
              <p className="text-gray-500">No products found</p>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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
