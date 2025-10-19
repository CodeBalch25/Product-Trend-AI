import { useState } from 'react';
import { productApi } from '@/services/api';
import toast from 'react-hot-toast';

interface ProductCardProps {
  product: any;
  onUpdate: () => void;
}

export default function ProductCard({ product, onUpdate }: ProductCardProps) {
  const [showPostModal, setShowPostModal] = useState(false);
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([]);
  const [rejectionReason, setRejectionReason] = useState('');
  const [isPosting, setIsPosting] = useState(false);
  const [isRejecting, setIsRejecting] = useState(false);

  const handleApprove = async () => {
    try {
      await productApi.approve(product.id);
      toast.success('Product approved!');
      onUpdate();
    } catch (err) {
      toast.error('Failed to approve product');
    }
  };

  const handleReject = async () => {
    if (!rejectionReason) {
      toast.error('Please select a rejection reason');
      return;
    }

    setIsRejecting(true);
    try {
      await productApi.reject(product.id, rejectionReason);
      toast.success('Product rejected and moved to rejected section');
      setShowRejectModal(false);
      onUpdate();
    } catch (err) {
      toast.error('Failed to reject product');
    } finally {
      setIsRejecting(false);
    }
  };

  const handlePost = async () => {
    if (selectedPlatforms.length === 0) {
      toast.error('Please select at least one platform');
      return;
    }

    setIsPosting(true);
    try {
      await productApi.post(product.id, selectedPlatforms);
      toast.success('Product posted successfully!');
      setShowPostModal(false);
      onUpdate();
    } catch (err) {
      toast.error('Failed to post product');
    } finally {
      setIsPosting(false);
    }
  };

  const togglePlatform = (platform: string) => {
    setSelectedPlatforms(prev =>
      prev.includes(platform)
        ? prev.filter(p => p !== platform)
        : [...prev, platform]
    );
  };

  const statusColors: Record<string, string> = {
    discovered: 'badge-info',
    analyzing: 'badge-warning',
    pending_review: 'badge-warning',
    approved: 'badge-success',
    rejected: 'badge-danger',
    posted: 'badge-success',
  };

  return (
    <>
      <div className="card hover:shadow-lg transition-shadow">
        {/* Image */}
        {product.image_url && (
          <img
            src={product.image_url}
            alt={product.title}
            className="w-full h-48 object-cover rounded-lg mb-4"
          />
        )}

        {/* Title & Status */}
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-lg font-semibold text-gray-900 flex-1">
            {product.title}
          </h3>
          <div className="flex gap-1">
            {product.is_new && (
              <span className="badge bg-green-500 text-white text-xs px-2 py-1">
                NEW
              </span>
            )}
            <span className={`badge ${statusColors[product.status] || 'badge-info'}`}>
              {product.status.replace('_', ' ')}
            </span>
          </div>
        </div>

        {/* Description */}
        <p className="text-gray-600 text-sm mb-4 line-clamp-3">
          {product.description || 'No description available'}
        </p>

        {/* Metrics */}
        <div className="grid grid-cols-2 gap-2 mb-4">
          <div className="bg-gray-50 p-2 rounded">
            <p className="text-xs text-gray-500">Trend Score</p>
            <p className="text-lg font-semibold text-primary-600">
              {product.trend_score?.toFixed(0) || 'N/A'}
            </p>
          </div>
          <div className="bg-gray-50 p-2 rounded">
            <p className="text-xs text-gray-500">
              {product.suggested_price ? 'Suggested Price' : 'Est. Cost'}
            </p>
            <p className="text-lg font-semibold text-green-600">
              ${(product.suggested_price || product.estimated_cost)?.toFixed(2) || 'N/A'}
            </p>
          </div>
        </div>

        {/* Source */}
        <div className="mb-4">
          <p className="text-xs text-gray-500">Source: {product.trend_source || 'Unknown'}</p>
          {product.ai_keywords && product.ai_keywords.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-2">
              {product.ai_keywords.slice(0, 3).map((keyword: string, idx: number) => (
                <span key={idx} className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded">
                  {keyword}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Posted Platforms */}
        {product.posted_platforms && product.posted_platforms.length > 0 && (
          <div className="mb-4">
            <p className="text-xs text-gray-500 mb-1">Posted to:</p>
            <div className="flex flex-wrap gap-1">
              {product.posted_platforms.map((platform: string) => (
                <span key={platform} className="text-xs bg-green-50 text-green-700 px-2 py-1 rounded">
                  {platform}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Rejection Reason (for rejected products) */}
        {product.status === 'rejected' && product.rejection_reason && (
          <div className="mb-4 bg-red-50 border border-red-200 rounded p-3">
            <p className="text-xs text-red-600 font-semibold mb-1">Rejection Reason:</p>
            <p className="text-sm text-red-800">
              {product.rejection_reason.split('_').map((word: string) =>
                word.charAt(0).toUpperCase() + word.slice(1)
              ).join(' ')}
            </p>
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-2">
          {product.status === 'pending_review' && (
            <>
              <button onClick={handleApprove} className="btn-primary flex-1 text-sm">
                Approve
              </button>
              <button onClick={() => setShowRejectModal(true)} className="btn-secondary flex-1 text-sm">
                Reject
              </button>
            </>
          )}

          {product.status === 'approved' && (
            <button
              onClick={() => setShowPostModal(true)}
              className="btn-primary w-full text-sm"
            >
              Post to Platforms
            </button>
          )}

          {product.status === 'posted' && (
            <button className="btn-secondary w-full text-sm" disabled>
              Already Posted
            </button>
          )}
        </div>
      </div>

      {/* Post Modal */}
      {showPostModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-xl font-bold mb-4">Select Platforms</h3>

            <div className="space-y-2 mb-6">
              {['amazon', 'ebay', 'tiktok_shop', 'facebook_marketplace', 'instagram_shop'].map(
                platform => (
                  <label key={platform} className="flex items-center space-x-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={selectedPlatforms.includes(platform)}
                      onChange={() => togglePlatform(platform)}
                      className="w-5 h-5 text-primary-600"
                    />
                    <span className="text-gray-700 capitalize">
                      {platform.replace('_', ' ')}
                    </span>
                  </label>
                )
              )}
            </div>

            <p className="text-sm text-yellow-700 bg-yellow-50 p-3 rounded mb-4">
              Note: You must have configured API credentials for each platform in settings
            </p>

            <div className="flex gap-2">
              <button
                onClick={handlePost}
                disabled={isPosting || selectedPlatforms.length === 0}
                className="btn-primary flex-1 disabled:opacity-50"
              >
                {isPosting ? 'Posting...' : 'Post Now'}
              </button>
              <button
                onClick={() => setShowPostModal(false)}
                className="btn-secondary flex-1"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Reject Modal */}
      {showRejectModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-xl font-bold mb-4 text-red-600">Reject Product</h3>

            <p className="text-gray-700 mb-4">
              Why are you rejecting "<strong>{product.title}</strong>"?
            </p>

            <p className="text-sm text-blue-600 bg-blue-50 p-3 rounded mb-4">
              💡 Your feedback helps train the AI to find better products!
            </p>

            <div className="space-y-2 mb-6">
              {[
                { value: 'price_not_good', label: 'Price Not Good Enough', emoji: '💰' },
                { value: 'bad_product', label: 'Bad Product Quality', emoji: '👎' },
                { value: 'not_trending', label: 'Not a Hot/Trending Product', emoji: '📉' },
                { value: 'high_competition', label: 'Too Much Competition', emoji: '⚔️' },
                { value: 'low_profit_margin', label: 'Profit Margin Too Low', emoji: '📊' },
                { value: 'saturated_market', label: 'Market Already Saturated', emoji: '🏪' },
                { value: 'wrong_category', label: 'Wrong Product Category', emoji: '🏷️' },
                { value: 'other', label: 'Other Reason', emoji: '❓' },
              ].map(reason => (
                <label
                  key={reason.value}
                  className={`flex items-center space-x-3 p-3 rounded-lg border-2 cursor-pointer transition-all ${
                    rejectionReason === reason.value
                      ? 'border-red-500 bg-red-50'
                      : 'border-gray-200 hover:border-red-300'
                  }`}
                >
                  <input
                    type="radio"
                    name="rejection_reason"
                    value={reason.value}
                    checked={rejectionReason === reason.value}
                    onChange={(e) => setRejectionReason(e.target.value)}
                    className="w-5 h-5 text-red-600"
                  />
                  <span className="text-2xl">{reason.emoji}</span>
                  <span className="text-gray-700 font-medium">{reason.label}</span>
                </label>
              ))}
            </div>

            <div className="flex gap-2">
              <button
                onClick={handleReject}
                disabled={isRejecting || !rejectionReason}
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isRejecting ? 'Rejecting...' : 'Reject Product'}
              </button>
              <button
                onClick={() => {
                  setShowRejectModal(false);
                  setRejectionReason('');
                }}
                className="btn-secondary flex-1"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
