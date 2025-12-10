/**
 * Section Component
 * 
 * Reusable section wrapper with consistent vertical spacing.
 * Mobile-first design following design system specifications.
 */

import React from 'react';
import { cn } from '@/lib/utils';
import { Container } from './Container';

interface SectionProps {
  children: React.ReactNode;
  className?: string;
  containerSize?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  noPadding?: boolean;
  fullWidth?: boolean;
}

export function Section({ 
  children, 
  className,
  containerSize = 'full',
  noPadding = false,
  fullWidth = false
}: SectionProps) {
  const content = fullWidth ? children : (
    <Container size={containerSize}>
      {children}
    </Container>
  );

  return (
    <section
      className={cn(
        !noPadding && 'py-8 md:py-16', // Mobile-specific spacing
        className
      )}
    >
      {content}
    </section>
  );
}
