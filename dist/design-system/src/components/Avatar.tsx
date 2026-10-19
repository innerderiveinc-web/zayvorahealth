import React from 'react';

export interface AvatarProps {
  src?: string;
  name: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  status?: 'online' | 'offline' | 'busy';
  className?: string;
}

export const Avatar: React.FC<AvatarProps> = ({
  src,
  name,
  size = 'md',
  status,
  className = '',
}) => {
  const initials = name
    .split(' ')
    .slice(0, 2)
    .map((n) => n[0])
    .join('')
    .toUpperCase();

  const sizeClasses = {
    sm: 'w-8 h-8 text-xs',
    md: 'w-10 h-10 text-sm',
    lg: 'w-12 h-12 text-base',
    xl: 'w-16 h-16 text-lg',
  }[size];

  return (
    <div className={`relative inline-block ${className}`}>
      {src ? (
        <img
          src={src}
          alt={name}
          className={`${sizeClasses} rounded-full object-cover border border-brand-primary/20`}
        />
      ) : (
        <div
          className={`${sizeClasses} rounded-full bg-brand-primary text-white flex items-center justify-center font-bold tracking-wider`}
        >
          {initials}
        </div>
      )}
      {status && (
        <span
          className={`absolute bottom-0 right-0 block w-2.5 h-2.5 rounded-full ring-2 ring-white dark:ring-slate-900 ${
            status === 'online'
              ? 'bg-emerald-500'
              : status === 'busy'
              ? 'bg-amber-500'
              : 'bg-gray-400'
          }`}
        />
      )}
    </div>
  );
};
