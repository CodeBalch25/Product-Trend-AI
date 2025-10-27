import axios from 'axios';
import { productApi, trendApi, analyticsApi } from '@/services/api';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('API Services', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('productApi', () => {
    it('fetches all products', async () => {
      const mockProducts = [{ id: 1, title: 'Test Product' }];
      mockedAxios.get.mockResolvedValue({ data: mockProducts });

      const response = await productApi.getAll();

      expect(mockedAxios.get).toHaveBeenCalledWith('/api/products', {
        params: { status: undefined, limit: 50, offset: 0 },
      });
      expect(response.data).toEqual(mockProducts);
    });

    it('approves a product', async () => {
      mockedAxios.post.mockResolvedValue({ data: { success: true } });

      await productApi.approve(1);

      expect(mockedAxios.post).toHaveBeenCalledWith('/api/products/1/approve');
    });

    it('rejects a product with reason', async () => {
      mockedAxios.post.mockResolvedValue({ data: { success: true } });

      await productApi.reject(1, 'Not suitable');

      expect(mockedAxios.post).toHaveBeenCalledWith('/api/products/1/reject', {
        reason: 'Not suitable',
      });
    });
  });

  describe('trendApi', () => {
    it('triggers trend scan', async () => {
      mockedAxios.post.mockResolvedValue({ data: { products_found: 10 } });

      const response = await trendApi.scan();

      expect(mockedAxios.post).toHaveBeenCalledWith(
        '/api/trends/scan',
        {},
        { timeout: 60000 }
      );
      expect(response.data.products_found).toBe(10);
    });
  });

  describe('analyticsApi', () => {
    it('fetches dashboard analytics', async () => {
      const mockAnalytics = {
        total_products: 100,
        pending_review: 20,
        approved: 50,
      };
      mockedAxios.get.mockResolvedValue({ data: mockAnalytics });

      const response = await analyticsApi.getDashboard();

      expect(mockedAxios.get).toHaveBeenCalledWith('/api/analytics/dashboard');
      expect(response.data).toEqual(mockAnalytics);
    });
  });
});
