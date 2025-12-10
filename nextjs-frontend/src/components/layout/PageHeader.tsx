/**
 * Page Header Component
 * 
 * Mobile-first page header with title and optional actions.
 * Used for consistent page headers across the application.
 */

import React from 'react';
import { cn } from '@/lib/utils';
import { Container } from './Container';

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
  className?: string;
}

export function PageHeader({ 
  title, 
  subtitle, 
  action,
  className 
}: PageHeaderProps) {
  return (
    <header
      className={cn(
        'border-b border-stone-200 bg-white',
        'py-6 md:py-8',
        className
      )}
    >
      <Container>
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold text-stone-900 tracking-tight">
              {title}
            </h1>
            {subtitle && (
              <p className="mt-2 text-base md:text-lg text-stone-600">
                {subtitle}
              </p>
            )}
          </div>
          {action && (
            <div className="flex-shrink-0">
              {action}
            </div>
          )}
        </div>
      </Container>
    </header>
  );
}
