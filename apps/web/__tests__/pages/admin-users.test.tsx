/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';

jest.mock('next/navigation', () => ({
  usePathname: () => '/admin/users',
  useRouter: () => ({ push: jest.fn() }),
}));

describe('Users Admin Page', () => {
  it('renders user table with mock data', async () => {
    const UsersPage = (await import('@/app/admin/users/page')).default;
    render(<UsersPage />);
    expect(screen.getByText('Users')).toBeInTheDocument();
    expect(screen.getByText('Dr. Ali Hassan')).toBeInTheDocument();
    expect(screen.getByText('Fatima Khan')).toBeInTheDocument();
  });

  it('filters users by search term', async () => {
    const UsersPage = (await import('@/app/admin/users/page')).default;
    render(<UsersPage />);
    const searchInput = screen.getByPlaceholderText(/search users/i);
    fireEvent.change(searchInput, { target: { value: 'ali' } });
    expect(screen.getByText('Dr. Ali Hassan')).toBeInTheDocument();
    expect(screen.queryByText('Fatima Khan')).not.toBeInTheDocument();
  });

  it('renders Invite User button', async () => {
    const UsersPage = (await import('@/app/admin/users/page')).default;
    render(<UsersPage />);
    expect(screen.getByText(/Invite User/i)).toBeInTheDocument();
  });
});
