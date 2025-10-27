import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ProductCard from '@/components/ProductCard';

// Mock the API
jest.mock('@/services/api', () => ({
  productApi: {
    approve: jest.fn(),
    reject: jest.fn(),
  },
}));

describe('ProductCard', () => {
  const mockProduct = {
    id: 1,
    title: 'Test Product',
    description: 'Test Description',
    category: 'Electronics',
    trend_score: 85,
    status: 'pending_review',
    suggested_price: 29.99,
    image_url: 'https://example.com/image.jpg',
  };

  const mockOnUpdate = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders product information correctly', () => {
    render(<ProductCard product={mockProduct} onUpdate={mockOnUpdate} />);

    expect(screen.getByText('Test Product')).toBeInTheDocument();
    expect(screen.getByText(/Test Description/)).toBeInTheDocument();
    expect(screen.getByText('Electronics')).toBeInTheDocument();
  });

  it('displays trend score', () => {
    render(<ProductCard product={mockProduct} onUpdate={mockOnUpdate} />);

    expect(screen.getByText(/85/)).toBeInTheDocument();
  });

  it('shows approve and reject buttons for pending products', () => {
    render(<ProductCard product={mockProduct} onUpdate={mockOnUpdate} />);

    expect(screen.getByRole('button', { name: /approve/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /reject/i })).toBeInTheDocument();
  });

  it('does not show action buttons for approved products', () => {
    const approvedProduct = { ...mockProduct, status: 'approved' };
    render(<ProductCard product={approvedProduct} onUpdate={mockOnUpdate} />);

    expect(screen.queryByRole('button', { name: /approve/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /reject/i })).not.toBeInTheDocument();
  });
});
