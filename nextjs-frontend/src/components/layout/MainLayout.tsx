/**
 * Main Layout Component
 * 
 * Primary layout wrapper with mobile-first design.
 * Includes navigation and bottom navigation for mobile.
 * 
 * Features:
 * - Mobile-first responsive design
 * - Bottom navigation on mobile (<768px)
 * - Top navigation on desktop
 * - Proper spacing for content area
 * - Safe area insets for notched devices
 */

import React from 'react';
import { cn } from '@/lib/utils';
import { BottomNav } from '@/components/navigation/BottomNav';

interface MainLayoutProps {
  children: React.ReactNode;
  className?: string;
  showBottomNav?: boolean;
}

export function MainLayout({ 
  children, 
  className,
  showBottomNav = true 
}: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-stone-50">
      {/* Main content area */}
      <main
        className={cn(
          'min-h-screen',
          // Add bottom padding on mobile to account for bottom navigation
          showBottomNav && 'pb-20 md:pb-0',
          className
        )}
      >
        {children}
      </main>

      {/* Bottom navigation (mobile only) */}
      {showBottomNav && <BottomNav />}
    </div>
  );
}
