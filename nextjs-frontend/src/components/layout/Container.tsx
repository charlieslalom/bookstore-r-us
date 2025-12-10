/**
 * Container Component
 * 
 * Mobile-first responsive container following design system specifications.
 * Provides consistent padding and max-width across breakpoints.
 */

import React from 'react';
import { cn } from '@/lib/utils';

interface ContainerProps {
  children: React.ReactNode;
  className?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
}

const containerSizes = {
  sm: 'sm:max-w-screen-sm',
  md: 'md:max-w-screen-md',
  lg: 'lg:max-w-screen-lg',
  xl: 'xl:max-w-screen-xl',
  full: '2xl:max-w-7xl',
};

export function Container({ 
  children, 
  className,
  size = 'full'
}: ContainerProps) {
  return (
    <div
      className={cn(
        'container mx-auto',
        'px-4 md:px-6 xl:px-8', // Responsive padding
        containerSizes[size],
        className
      )}
    >
      {children}
    </div>
  );
}
