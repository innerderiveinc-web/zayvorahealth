/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, act } from '@testing-library/react';

// Mock fetch globally
global.fetch = jest.fn().mockResolvedValue({
  ok: true,
  json: async () => ({ status: 'healthy' }),
} as Response);

jest.mock('next/navigation', () => ({
  usePathname: () => '/admin/health',
  useRouter: () => ({ push: jest.fn() }),
}));

describe('System Health Page', () => {
  it('renders all 6 service cards', async () => {
    jest.useFakeTimers();
    const SystemHealthPage = (await import('@/app/admin/health/page')).default;
    await act(async () => {
      render(<SystemHealthPage />);
    });
    expect(screen.getByText('System Health')).toBeInTheDocument();
    const serviceNames = ['Identity Service', 'Clinical Service', 'Knowledge Service',
      'Therapeutic Service', 'AI Service', 'API Gateway'];
    for (const name of serviceNames) {
      expect(screen.getByText(name)).toBeInTheDocument();
    }
    jest.useRealTimers();
  });

  it('shows Check Now button', async () => {
    const SystemHealthPage = (await import('@/app/admin/health/page')).default;
    await act(async () => {
      render(<SystemHealthPage />);
    });
    expect(screen.getByText(/Check Now/i)).toBeInTheDocument();
  });
});
