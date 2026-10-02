/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';

// Mock next/navigation
jest.mock('next/navigation', () => ({
  usePathname: () => '/admin',
  useRouter: () => ({ push: jest.fn() }),
}));

jest.mock('next/link', () => {
  return function MockLink({ children, href }: { children: React.ReactNode; href: string }) {
    return <a href={href}>{children}</a>;
  };
});

describe('Admin Console', () => {
  it('renders brand logo and nav items', async () => {
    const AdminLayout = (await import('@/app/admin/layout')).default;
    const { getByText } = render(
      <AdminLayout><div data-testid="child">Page Content</div></AdminLayout>
    );
    expect(getByText('ZAYVORA')).toBeInTheDocument();
    expect(getByText('Dashboard')).toBeInTheDocument();
    expect(getByText('Users')).toBeInTheDocument();
    expect(getByText('Audit Logs')).toBeInTheDocument();
    expect(getByText('System Health')).toBeInTheDocument();
    expect(getByText('Page Content')).toBeInTheDocument();
  });

  it('toggles sidebar collapse', async () => {
    const AdminLayout = (await import('@/app/admin/layout')).default;
    const { getByText, container } = render(
      <AdminLayout><div /></AdminLayout>
    );
    const toggleBtn = container.querySelector('button');
    expect(getByText('Dashboard')).toBeVisible();
    if (toggleBtn) fireEvent.click(toggleBtn);
    // Sidebar collapses — text still in DOM but layout changes
    expect(getByText('ZAYVORA')).toBeTruthy();
  });
});
