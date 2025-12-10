/**
 * Bottom Navigation Component
 * 
 * Mobile-first bottom navigation bar for thumb-zone accessibility.
 * Fixed position on mobile, hidden on desktop (≥768px).
 * 
 * Features:
 * - 5 navigation items: Home, Categories, Search, Cart, Account
 * - Active state indication
 * - Cart badge with item count
 * - 44px minimum touch targets
 * - Safe area insets for notched devices
 * - Smooth transitions
 * 
 * Design System Reference:
 * - Mobile-only display (hidden md:hidden)
 * - Touch-friendly (min 44px height)
 * - Bottom positioning with safe area
 */

'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import {
  Home,
  Grid3x3,
  Search,
  ShoppingCart,
  User,
} from 'lucide-react';

interface NavItem {
  label: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
}

const navItems: NavItem[] = [
  { label: 'Home', href: '/', icon: Home },
  { label: 'Categories', href: '/categories', icon: Grid3x3 },
  { label: 'Search', href: '/search', icon: Search },
  { label: 'Cart', href: '/cart', icon: ShoppingCart },
  { label: 'Account', href: '/account', icon: User },
];

export function BottomNav() {
  const pathname = usePathname();
  
  // For demo: cart count (in real app, this would come from context/state)
  const cartCount = 0;

  return (
    <nav
      className={cn(
        // Mobile only
        'md:hidden',
        // Fixed positioning
        'fixed bottom-0 left-0 right-0 z-50',
        // Background and border
        'bg-white border-t border-stone-200',
        // Safe area for notched devices
        'pb-safe',
        // Shadow for elevation
        'shadow-lg'
      )}
      role="navigation"
      aria-label="Mobile navigation"
    >
      <div className="flex items-center justify-around">
        {navItems.map((item) => {
          const isActive = pathname === item.href || 
                          (item.href !== '/' && pathname.startsWith(item.href));
          const Icon = item.icon;
          const isCart = item.label === 'Cart';

          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                // Flex layout
                'flex flex-col items-center justify-center',
                // Touch target (minimum 44px)
                'min-h-[56px] flex-1',
                // Spacing
                'px-2 py-2',
                // Transitions
                'transition-colors duration-150',
                // Active/inactive states
                isActive
                  ? 'text-primary'
                  : 'text-stone-600 hover:text-stone-900'
              )}
              aria-current={isActive ? 'page' : undefined}
            >
              {/* Icon with badge container */}
              <div className="relative">
                <Icon 
                  className={cn(
                    'h-6 w-6',
                    isActive && 'fill-current'
                  )} 
                />
                
                {/* Cart badge */}
                {isCart && cartCount > 0 && (
                  <span
                    className={cn(
                      'absolute -top-2 -right-2',
                      'flex items-center justify-center',
                      'min-w-[18px] h-[18px] px-1',
                      'text-xs font-semibold',
                      'bg-primary text-white',
                      'rounded-full',
                      'border-2 border-white'
                    )}
                    aria-label={`${cartCount} items in cart`}
                  >
                    {cartCount > 99 ? '99+' : cartCount}
                  </span>
                )}
              </div>

              {/* Label */}
              <span 
                className={cn(
                  'text-xs font-medium mt-1',
                  'leading-none'
                )}
              >
                {item.label}
              </span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
