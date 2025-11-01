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
      <div className="card group hover:scale-[1.02] transition-all duration-300">
        {/* Image */}
        {product.image_url && (
          <div className="relative overflow-hidden rounded-xl mb-4 bg-gradient-to-br from-slate-100 to-slate-200">
            <img
              src={product.image_url}
              alt={product.title}
              className="w-full h-52 object-cover group-hover:scale-110 transition-transform duration-500"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </div>
        )}

        {/* Title & Status */}
        <div className="flex justify-between items-start mb-3">
          <h3 className="text-lg font-bold text-slate-800 flex-1 leading-tight">
            {product.title}
          </h3>
          <div className="flex gap-2 ml-2">
            {product.is_new && (
              <span className="badge bg-gradient-to-r from-emerald-500 to-teal-500 text-white text-xs px-3 py-1 shadow-md">
                NEW
              </span>
            )}
            <span className={`badge ${statusColors[product.status] || 'badge-info'}`}>
              {product.status.replace('_', ' ').toUpperCase()}
            </span>
          </div>
        </div>

        {/* Description */}
        <p className="text-slate-600 text-sm mb-4 line-clamp-3 leading-relaxed">
          {product.description || 'No description available'}
        </p>

        {/* Metrics */}
        <div className="grid grid-cols-2 gap-3 mb-4">
          <div className="relative overflow-hidden bg-gradient-to-br from-violet-50 to-indigo-50 p-3 rounded-xl border border-violet-100">
            <div className="absolute top-0 right-0 w-16 h-16 bg-violet-200/20 rounded-full blur-2xl"></div>
            <p className="text-xs text-slate-600 font-medium relative">Trend Score</p>
            <p className="text-2xl font-bold text-violet-600 mt-1 relative">
              {product.trend_score?.toFixed(0) || 'N/A'}
            </p>
          </div>
          <div className="relative overflow-hidden bg-gradient-to-br from-emerald-50 to-teal-50 p-3 rounded-xl border border-emerald-100">
            <div className="absolute top-0 right-0 w-16 h-16 bg-emerald-200/20 rounded-full blur-2xl"></div>
            <p className="text-xs text-slate-600 font-medium relative">
              {product.suggested_price ? 'Suggested Price' : 'Est. Cost'}
            </p>
            <p className="text-2xl font-bold text-emerald-600 mt-1 relative">
              ${(product.suggested_price || product.estimated_cost)?.toFixed(2) || 'N/A'}
            </p>
          </div>
        </div>

        {/* Source */}
        <div className="mb-4">
          <p className="text-xs text-slate-500 font-medium">
            Source: <span className="text-slate-700">{product.trend_source || 'Unknown'}</span>
          </p>
          {(() => {
            // Safe parsing of ai_keywords - handles string "null", actual arrays, and JSON strings
            let keywords: string[] = [];

            if (product.ai_keywords && typeof product.ai_keywords === 'string') {
              if (product.ai_keywords !== 'null' && product.ai_keywords !== 'undefined') {
                try {
                  // Try parsing as JSON array
                  const parsed = JSON.parse(product.ai_keywords);
                  keywords = Array.isArray(parsed) ? parsed : [];
                } catch {
                  // If not JSON, split by comma
                  keywords = product.ai_keywords.split(',').map(k => k.trim()).filter(k => k);
                }
              }
            } else if (Array.isArray(product.ai_keywords)) {
              keywords = product.ai_keywords;
            }

            return keywords.length > 0 ? (
              <div className="flex flex-wrap gap-2 mt-2">
                {keywords.slice(0, 3).map((keyword: string, idx: number) => (
                  <span key={idx} className="text-xs bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-700 px-3 py-1.5 rounded-lg border border-blue-100 font-medium">
                    {keyword}
                  </span>
                ))}
              </div>
            ) : null;
          })()}
        </div>

        {/* Posted Platforms */}
        {product.posted_platforms && product.posted_platforms.length > 0 && (
          <div className="mb-4">
            <p className="text-xs text-slate-500 font-medium mb-2">Posted to:</p>
            <div className="flex flex-wrap gap-2">
              {product.posted_platforms.map((platform: string) => (
                <span key={platform} className="text-xs bg-gradient-to-r from-emerald-50 to-teal-50 text-emerald-700 px-3 py-1.5 rounded-lg border border-emerald-100 font-medium">
                  {platform}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Rejection Reason (for rejected products) */}
        {product.status === 'rejected' && product.rejection_reason && (
          <div className="mb-4 bg-gradient-to-r from-rose-50 to-red-50 border border-rose-200 rounded-xl p-4">
            <p className="text-xs text-rose-700 font-bold mb-1">Rejection Reason:</p>
            <p className="text-sm text-rose-900 font-medium">
              {product.rejection_reason.split('_').map((word: string) =>
                word.charAt(0).toUpperCase() + word.slice(1)
              ).join(' ')}
            </p>
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-3">
          {product.status === 'pending_review' && (
            <>
              <button onClick={handleApprove} className="btn-primary flex-1">
                Approve
              </button>
              <button onClick={() => setShowRejectModal(true)} className="btn-secondary flex-1">
                Reject
              </button>
            </>
          )}

          {product.status === 'approved' && (
            <button
              onClick={() => setShowPostModal(true)}
              className="btn-primary w-full"
            >
              Post to Platforms
            </button>
          )}

          {product.status === 'posted' && (
            <button className="relative overflow-hidden bg-slate-100 text-slate-400 px-6 py-2.5 rounded-xl font-medium cursor-not-allowed w-full" disabled>
              Already Posted
            </button>
          )}
        </div>
      </div>

      {/* Post Modal */}
      {showPostModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 animate-fade-in">
          <div className="glass rounded-2xl p-8 max-w-md w-full mx-4 shadow-2xl animate-slide-up">
            <h3 className="text-2xl font-bold mb-6 text-gradient from-violet-600 to-indigo-600">Select Platforms</h3>

            <div className="space-y-3 mb-6">
              {['amazon', 'ebay', 'tiktok_shop', 'facebook_marketplace', 'instagram_shop'].map(
                platform => (
                  <label
                    key={platform}
                    className={`flex items-center space-x-3 p-4 rounded-xl border-2 cursor-pointer transition-all duration-200 ${
                      selectedPlatforms.includes(platform)
                        ? 'border-violet-500 bg-gradient-to-r from-violet-50 to-indigo-50'
                        : 'border-slate-200 hover:border-violet-300 hover:bg-slate-50'
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={selectedPlatforms.includes(platform)}
                      onChange={() => togglePlatform(platform)}
                      className="w-5 h-5 text-violet-600 rounded"
                    />
                    <span className="text-slate-700 capitalize font-medium">
                      {platform.replace('_', ' ')}
                    </span>
                  </label>
                )
              )}
            </div>

            <p className="text-sm text-amber-700 bg-gradient-to-r from-amber-50 to-yellow-50 p-4 rounded-xl border border-amber-200 mb-6">
              Note: You must have configured API credentials for each platform in settings
            </p>

            <div className="flex gap-3">
              <button
                onClick={handlePost}
                disabled={isPosting || selectedPlatforms.length === 0}
                className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
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
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 animate-fade-in">
          <div className="glass rounded-2xl p-8 max-w-md w-full mx-4 shadow-2xl animate-slide-up">
            <h3 className="text-2xl font-bold mb-4 text-gradient from-rose-600 to-red-600">Reject Product</h3>

            <p className="text-slate-700 mb-4 font-medium">
              Why are you rejecting "<strong className="text-slate-900">{product.title}</strong>"?
            </p>

            <p className="text-sm text-blue-700 bg-gradient-to-r from-blue-50 to-indigo-50 p-4 rounded-xl border border-blue-200 mb-6 font-medium">
              💡 Your feedback helps train the AI to find better products!
            </p>

            <div className="space-y-3 mb-6 max-h-96 overflow-y-auto">
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
                  className={`flex items-center space-x-3 p-4 rounded-xl border-2 cursor-pointer transition-all duration-200 ${
                    rejectionReason === reason.value
                      ? 'border-rose-500 bg-gradient-to-r from-rose-50 to-red-50 shadow-md'
                      : 'border-slate-200 hover:border-rose-300 hover:bg-slate-50'
                  }`}
                >
                  <input
                    type="radio"
                    name="rejection_reason"
                    value={reason.value}
                    checked={rejectionReason === reason.value}
                    onChange={(e) => setRejectionReason(e.target.value)}
                    className="w-5 h-5 text-rose-600"
                  />
                  <span className="text-2xl">{reason.emoji}</span>
                  <span className="text-slate-700 font-medium">{reason.label}</span>
                </label>
              ))}
            </div>

            <div className="flex gap-3">
              <button
                onClick={handleReject}
                disabled={isRejecting || !rejectionReason}
                className="bg-gradient-to-r from-rose-600 to-red-600 hover:from-rose-700 hover:to-red-700 text-white px-6 py-2.5 rounded-xl font-medium shadow-lg shadow-rose-500/50 hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
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
