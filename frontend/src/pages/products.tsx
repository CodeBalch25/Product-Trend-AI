import { useState } from 'react';
import Head from 'next/head';
import useSWR from 'swr';
import { productApi } from '@/services/api';
import ProductCard from '@/components/ProductCard';
import Layout from '@/components/Layout';

const fetcher = (url: string) => productApi.getAll().then(res => res.data);

export default function Products() {
  const [statusFilter, setStatusFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const { data: products, error, mutate } = useSWR('/api/products', fetcher);

  // Filter products by status and search term
  const filteredProducts = products?.filter((p: any) => {
    // Status filter
    const statusMatch = statusFilter === 'all' ? p.status !== 'rejected' : p.status === statusFilter;

    // Search filter
    const searchLower = searchTerm.toLowerCase();
    const searchMatch = !searchTerm ||
      p.title?.toLowerCase().includes(searchLower) ||
      p.description?.toLowerCase().includes(searchLower) ||
      p.category?.toLowerCase().includes(searchLower);

    return statusMatch && searchMatch;
  });

  return (
    <Layout>
      <Head>
        <title>Products - Product Trend Automation</title>
      </Head>

      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">All Products</h1>
          <p className="text-gray-500 mt-1">
            Browse and manage all discovered products
          </p>
        </div>

        {/* Search Bar */}
        <div className="card">
          <input
            type="text"
            placeholder="Search products by title, description, or category..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>

        {/* Status Filters */}
        <div className="card">
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setStatusFilter('all')}
              className={`px-4 py-2 rounded-lg ${
                statusFilter === 'all'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              All ({products?.filter((p: any) => p.status !== 'rejected').length || 0})
            </button>
            <button
              onClick={() => setStatusFilter('pending_review')}
              className={`px-4 py-2 rounded-lg ${
                statusFilter === 'pending_review'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              Pending Review ({products?.filter((p: any) => p.status === 'pending_review').length || 0})
            </button>
            <button
              onClick={() => setStatusFilter('approved')}
              className={`px-4 py-2 rounded-lg ${
                statusFilter === 'approved'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              Approved ({products?.filter((p: any) => p.status === 'approved').length || 0})
            </button>
            <button
              onClick={() => setStatusFilter('posted')}
              className={`px-4 py-2 rounded-lg ${
                statusFilter === 'posted'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              Posted ({products?.filter((p: any) => p.status === 'posted').length || 0})
            </button>
            <button
              onClick={() => setStatusFilter('rejected')}
              className={`px-4 py-2 rounded-lg ${
                statusFilter === 'rejected'
                  ? 'bg-red-600 text-white'
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              Rejected ({products?.filter((p: any) => p.status === 'rejected').length || 0})
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
              <p className="text-gray-500">
                {searchTerm ? 'No products match your search' : 'No products found'}
              </p>
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
