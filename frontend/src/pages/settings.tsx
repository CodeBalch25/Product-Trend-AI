import Head from 'next/head';
import Layout from '@/components/Layout';

export default function Settings() {
  return (
    <Layout>
      <Head>
        <title>Settings - Product Trend Automation</title>
      </Head>

      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>

        <div className="card">
          <h2 className="text-xl font-semibold mb-4">API Configuration</h2>
          <p className="text-gray-600 mb-4">
            To configure API keys, edit the <code className="bg-gray-100 px-2 py-1 rounded">.env</code> file in your project directory:
          </p>
          <p className="text-sm font-mono bg-gray-900 text-green-400 p-4 rounded">
            C:\Users\timud\Documents\product-trend-automation\.env
          </p>

          <div className="mt-6 space-y-4">
            <div>
              <h3 className="font-semibold text-gray-900">✅ Groq API (Configured)</h3>
              <p className="text-sm text-gray-600">FREE & Fast - Using Llama 3.1 70B model</p>
            </div>

            <div>
              <h3 className="font-semibold text-gray-900">✅ Hugging Face API (Configured)</h3>
              <p className="text-sm text-gray-600">FREE - Alternative AI provider</p>
            </div>

            <div className="border-t pt-4">
              <h3 className="font-semibold text-gray-700">Platform Integrations (Optional)</h3>
              <ul className="text-sm text-gray-600 mt-2 space-y-1">
                <li>• Amazon SP-API - For posting to Amazon</li>
                <li>• eBay API - For posting to eBay</li>
                <li>• TikTok Shop API - For posting to TikTok Shop</li>
                <li>• Facebook/Instagram API - For posting to Meta platforms</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="card bg-blue-50 border border-blue-200">
          <h2 className="text-lg font-semibold text-blue-900 mb-2">
            🎉 Your AI is Ready!
          </h2>
          <p className="text-blue-800">
            Groq and Hugging Face are configured and will be used for product analysis.
            After editing .env, restart containers with: <code className="bg-blue-100 px-2 py-1 rounded">docker compose restart</code>
          </p>
        </div>
      </div>
    </Layout>
  );
}
