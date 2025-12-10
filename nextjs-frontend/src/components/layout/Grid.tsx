/**
 * Grid Component
 * 
 * Responsive grid layout for products, categories, etc.
 * Mobile-first with configurable column counts per breakpoint.
 */

import React from 'react';
import { cn } from '@/lib/utils';

interface GridProps {
  children: React.ReactNode;
  className?: string;
  cols?: {
    mobile?: 1 | 2;
    tablet?: 2 | 3 | 4;
    desktop?: 3 | 4 | 5 | 6;
  };
  gap?: 'sm' | 'md' | 'lg';
}

const gapSizes = {
  sm: 'gap-3 md:gap-4',
  md: 'gap-4 md:gap-6',
  lg: 'gap-6 md:gap-8',
};

export function Grid({ 
  children, 
  className,
  cols = { mobile: 1, tablet: 2, desktop: 4 },
  gap = 'md'
}: GridProps) {
  const gridCols = cn(
    cols.mobile === 1 ? 'grid-cols-1' : 'grid-cols-2',
    cols.tablet === 2 && 'sm:grid-cols-2',
    cols.tablet === 3 && 'sm:grid-cols-3',
    cols.tablet === 4 && 'sm:grid-cols-4',
    cols.desktop === 3 && 'lg:grid-cols-3',
    cols.desktop === 4 && 'lg:grid-cols-4',
    cols.desktop === 5 && 'lg:grid-cols-5',
    cols.desktop === 6 && 'lg:grid-cols-6',
  );

  return (
    <div
      className={cn(
        'grid',
        gridCols,
        gapSizes[gap],
        className
      )}
    >
      {children}
    </div>
  );
}
