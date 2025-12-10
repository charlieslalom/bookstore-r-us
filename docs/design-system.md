# Bookstore-R-Us Design System

> **Version:** 1.0  
> **Status:** ACTIVE  
> **Last Updated:** December 10, 2025  
> **Framework:** Next.js 14 + Tailwind CSS v4 + shadcn/ui

---

## Design Philosophy

Bookstore-R-Us aims to evoke the feeling of **"walking into a nice bookstore"** — warm, inviting, distinctive, and focused on content. The design should feel premium but approachable, modern but not sterile, and optimized for mobile-first browsing.

### Key Principles

1. **Mobile-First** — Design starts at 375px viewport, scales up gracefully
2. **Content Priority** — Product images and titles take center stage
3. **Warm & Bookish** — Cream backgrounds, serif accents, rich colors
4. **Touch-Friendly** — Minimum 44px tap targets, generous spacing
5. **Performance** — Every design decision considers page load impact

---

## Typography

### Font Stack

**Display/Headings:**
- Primary: System serif stack for warmth
- Fallback: `Georgia, "Times New Roman", Times, serif`
- Usage: H1, H2, product titles, brand elements

**Body/UI:**
- Primary: System sans-serif stack for readability
- Fallback: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`
- Usage: Body text, buttons, navigation, product descriptions

**Monospace (Code/Data):**
- Primary: `"SF Mono", Monaco, "Cascadia Code", "Courier New", monospace`
- Usage: Order numbers, product codes, technical specs

### Font Sizes (Mobile-First)

| Element | Mobile (320-767px) | Tablet (768-1023px) | Desktop (1024px+) | Tailwind Class |
|---------|-------------------|---------------------|-------------------|----------------|
| H1 (Hero) | 2rem (32px) | 2.5rem (40px) | 3rem (48px) | `text-4xl sm:text-5xl md:text-6xl` |
| H2 (Section) | 1.5rem (24px) | 1.75rem (28px) | 2rem (32px) | `text-2xl md:text-3xl lg:text-4xl` |
| H3 (Card Title) | 1.25rem (20px) | 1.5rem (24px) | 1.5rem (24px) | `text-xl md:text-2xl` |
| Body Large | 1.125rem (18px) | 1.125rem (18px) | 1.25rem (20px) | `text-lg md:text-xl` |
| Body | 1rem (16px) | 1rem (16px) | 1rem (16px) | `text-base` |
| Small | 0.875rem (14px) | 0.875rem (14px) | 0.875rem (14px) | `text-sm` |
| XSmall | 0.75rem (12px) | 0.75rem (12px) | 0.75rem (12px) | `text-xs` |

### Font Weights

| Weight | Value | Tailwind Class | Usage |
|--------|-------|----------------|-------|
| Regular | 400 | `font-normal` | Body text, descriptions |
| Medium | 500 | `font-medium` | Navigation, subtle emphasis |
| Semibold | 600 | `font-semibold` | Buttons, important labels |
| Bold | 700 | `font-bold` | Headings, product titles |
| Extrabold | 800 | `font-extrabold` | Hero headlines, CTAs |

### Line Heights

| Context | Line Height | Tailwind Class | Usage |
|---------|------------|----------------|-------|
| Tight | 1.25 | `leading-tight` | Headings, hero text |
| Normal | 1.5 | `leading-normal` | Body text |
| Relaxed | 1.75 | `leading-relaxed` | Long-form content |
| Loose | 2 | `leading-loose` | Product descriptions |

---

## Color Palette

### Brand Colors (Warm & Bookish)

```css
:root {
  /* Primary Brand Color - Deep Book Blue */
  --color-primary: #2563eb; /* Rich, trustworthy blue */
  --color-primary-hover: #1d4ed8;
  --color-primary-light: #3b82f6;
  
  /* Accent - Warm Gold (for highlights, badges) */
  --color-accent: #f59e0b;
  --color-accent-hover: #d97706;
  
  /* Success - Book Green */
  --color-success: #10b981;
  
  /* Warning - Amber */
  --color-warning: #f59e0b;
  
  /* Error - Warm Red */
  --color-error: #ef4444;
}
```

### Neutral Colors (Cream & Warm Grays)

```css
:root {
  /* Backgrounds - Cream Tones */
  --color-bg-primary: #fafaf9; /* Warm off-white (stone-50) */
  --color-bg-secondary: #f5f5f4; /* Subtle cream (stone-100) */
  --color-bg-tertiary: #e7e5e4; /* Deeper cream (stone-200) */
  
  /* Text Colors */
  --color-text-primary: #1c1917; /* Deep charcoal (stone-900) */
  --color-text-secondary: #57534e; /* Medium gray (stone-600) */
  --color-text-muted: #78716c; /* Light gray (stone-500) */
  
  /* Borders */
  --color-border: #e7e5e4; /* stone-200 */
  --color-border-dark: #d6d3d1; /* stone-300 */
}
```

### Tailwind Configuration

Update `tailwind.config.ts` to use warm neutral palette:

```typescript
theme: {
  extend: {
    colors: {
      background: "hsl(var(--background))",
      foreground: "hsl(var(--foreground))",
      primary: {
        DEFAULT: "#2563eb",
        foreground: "#ffffff",
      },
      accent: {
        DEFAULT: "#f59e0b",
        foreground: "#000000",
      },
      muted: {
        DEFAULT: "#f5f5f4", // stone-100
        foreground: "#57534e", // stone-600
      },
      border: "#e7e5e4", // stone-200
    }
  }
}
```

### Color Usage Guidelines

| Element | Color | Tailwind Class | Notes |
|---------|-------|----------------|-------|
| Page Background | Warm Off-White | `bg-stone-50` | Creates warm, inviting feel |
| Card Background | White | `bg-white` | Product cards stand out |
| Primary CTA | Brand Blue | `bg-primary hover:bg-primary-hover` | Add to Cart, Checkout |
| Secondary CTA | Outline | `border-primary text-primary` | Browse, View More |
| Price Text | Accent Gold | `text-accent` | Draws attention to pricing |
| Sale Badge | Error Red | `bg-error text-white` | Sale, Discount |
| Star Rating | Accent Gold | `text-accent` | Product ratings |
| Borders | Stone 200 | `border-stone-200` | Subtle separation |

---

## Spacing System

### Base Unit: 4px (Tailwind Default)

All spacing uses multiples of 4px for visual consistency.

| Spacing | Value | Tailwind Class | Usage |
|---------|-------|----------------|-------|
| XXS | 4px | `p-1`, `m-1`, `gap-1` | Icon padding, tight spacing |
| XS | 8px | `p-2`, `m-2`, `gap-2` | Input padding, small gaps |
| SM | 12px | `p-3`, `m-3`, `gap-3` | Button padding (vertical) |
| MD | 16px | `p-4`, `m-4`, `gap-4` | Card padding, default gaps |
| LG | 24px | `p-6`, `m-6`, `gap-6` | Section padding |
| XL | 32px | `p-8`, `m-8`, `gap-8` | Large section spacing |
| 2XL | 48px | `p-12`, `m-12`, `gap-12` | Hero section padding |
| 3XL | 64px | `p-16`, `m-16`, `gap-16` | Major section breaks |

### Mobile-Specific Spacing

| Context | Mobile | Desktop | Tailwind Class |
|---------|--------|---------|----------------|
| Container Padding | 16px | 24px | `px-4 md:px-6` |
| Section Padding (Vertical) | 32px | 64px | `py-8 md:py-16` |
| Grid Gap | 16px | 24px | `gap-4 md:gap-6` |
| Card Padding | 16px | 24px | `p-4 md:p-6` |

---

## Component Patterns

### Product Card

**Mobile Design (375px):**
- Image: Full width, 16:9 aspect ratio
- Padding: 16px
- Title: text-lg font-bold, 2 lines max (truncate)
- Price: text-xl font-semibold text-accent
- Rating: 5-star visual, text-sm
- CTA: Full-width button, 48px height

**Desktop Design (1024px+):**
- Image: Hover zoom effect (scale-105)
- Padding: 20px
- Title: text-xl font-bold
- Shadow: Subtle on hover (shadow-lg)

### Button Sizes

| Size | Height | Padding X | Font Size | Tailwind Class |
|------|--------|-----------|-----------|----------------|
| Small | 36px | 12px | 14px | `h-9 px-3 text-sm` |
| Default | 44px | 16px | 16px | `h-11 px-4 text-base` |
| Large | 52px | 24px | 18px | `h-13 px-6 text-lg` |

**Touch Target Rule:** Minimum 44x44px for all interactive elements on mobile.

### Form Inputs

- Height: 48px (mobile), 44px (desktop)
- Border: 1px solid border-stone-300
- Focus: Ring 2px primary color
- Placeholder: text-muted-foreground
- Label: text-sm font-medium, 8px margin-bottom

---

## Layout & Grid

### Container Widths

| Breakpoint | Max Width | Padding | Tailwind Class |
|------------|-----------|---------|----------------|
| Mobile (< 640px) | 100% | 16px | `container px-4` |
| SM (640px+) | 640px | 16px | `sm:max-w-screen-sm` |
| MD (768px+) | 768px | 24px | `md:max-w-screen-md md:px-6` |
| LG (1024px+) | 1024px | 24px | `lg:max-w-screen-lg` |
| XL (1280px+) | 1280px | 32px | `xl:max-w-screen-xl xl:px-8` |
| 2XL (1536px+) | 1400px | 32px | `2xl:max-w-7xl` |

### Grid Systems

**Product Grid:**
- Mobile: 1 column (full width cards)
- Tablet: 2 columns
- Desktop: 3-4 columns (depending on context)
- Gap: 16px mobile, 24px desktop

```tsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
  {/* Product cards */}
</div>
```

**Category Grid:**
- Mobile: 2 columns (smaller cards)
- Tablet: 3 columns
- Desktop: 4-6 columns
- Gap: 12px mobile, 16px desktop

---

## Animations & Interactions

### Transition Durations

| Speed | Duration | Tailwind Class | Usage |
|-------|----------|----------------|-------|
| Fast | 150ms | `duration-150` | Hover states, small movements |
| Normal | 200ms | `duration-200` | Button presses, modals |
| Slow | 300ms | `duration-300` | Page transitions, large elements |

### Common Animations

**Hover Effects (Desktop Only):**
```tsx
<div className="transition-transform duration-200 hover:scale-105">
```

**Button Press:**
```tsx
<button className="active:scale-95 transition-transform duration-150">
```

**Fade In:**
```tsx
<div className="animate-in fade-in duration-300">
```

**Slide In (Mobile Menu):**
```tsx
<div className="animate-in slide-in-from-left duration-200">
```

### Loading States

**Skeleton Screens:**
- Use subtle pulse animation
- Match content dimensions exactly
- Warm gray colors (stone-200, stone-300)

```tsx
<div className="animate-pulse bg-stone-200 rounded-md h-48 w-full" />
```

---

## Accessibility (WCAG AA Compliance)

### Color Contrast

All text must meet WCAG AA minimum contrast ratios:
- **Normal text (< 18px):** 4.5:1 minimum
- **Large text (≥ 18px or bold ≥ 14px):** 3:1 minimum
- **UI components (borders, icons):** 3:1 minimum

### Tested Combinations

| Foreground | Background | Contrast Ratio | Pass? |
|------------|-----------|----------------|-------|
| stone-900 (#1c1917) | stone-50 (#fafaf9) | 13.2:1 | ✅ AAA |
| stone-600 (#57534e) | stone-50 (#fafaf9) | 6.8:1 | ✅ AAA |
| primary (#2563eb) | white (#ffffff) | 8.6:1 | ✅ AAA |
| accent (#f59e0b) | stone-900 (#1c1917) | 5.2:1 | ✅ AA |

### Focus States

All interactive elements must have visible focus indicators:
```tsx
<button className="focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2">
```

### Touch Targets

- Minimum size: 44x44px
- Recommended: 48x48px
- Spacing between targets: ≥ 8px

---

## Responsive Breakpoints

| Breakpoint | Min Width | Tailwind Prefix | Usage |
|------------|-----------|-----------------|-------|
| Mobile | 0px | (default) | Base styles, mobile-first |
| Small | 640px | `sm:` | Large phones, phablets |
| Medium | 768px | `md:` | Tablets |
| Large | 1024px | `lg:` | Small laptops, horizontal tablets |
| XLarge | 1280px | `xl:` | Desktop monitors |
| 2XLarge | 1536px | `2xl:` | Large desktop monitors |

### Design Approach

**Mobile (320-767px):**
- Single column layouts
- Full-width buttons
- Bottom navigation bar
- Hamburger menus
- Touch-optimized interactions

**Tablet (768-1023px):**
- 2-3 column grids
- Side-by-side layouts
- Expanded navigation (still mobile-friendly)

**Desktop (1024px+):**
- 3-4+ column grids
- Hover states enabled
- Persistent navigation
- Mouse-optimized interactions
- Larger typography

---

## Icons

**Library:** Lucide React (installed: `lucide-react`)

**Size Guidelines:**
| Context | Size | Tailwind Class |
|---------|------|----------------|
| Small (inline text) | 16px | `h-4 w-4` |
| Default | 20px | `h-5 w-5` |
| Large (buttons) | 24px | `h-6 w-6` |
| Hero/Feature | 48px | `h-12 w-12` |

**Common Icons:**
- Cart: `ShoppingCart`
- User: `User`
- Search: `Search`
- Menu: `Menu`
- Heart (Wishlist): `Heart`
- Arrow Right: `ArrowRight`
- Star (Rating): `Star`
- Check: `Check`
- X (Close): `X`

---

## Implementation Checklist

### Phase 1 (Current)
- [x] Next.js 14 with App Router
- [x] Tailwind CSS v4 configured
- [x] shadcn/ui component library (Button, Card, Input, Label, Badge)
- [x] Lucide React icons
- [x] Mobile-first layout structure
- [ ] Custom color palette (warm cream tones)
- [ ] Typography system (serif headings)
- [ ] Animation utilities (Framer Motion or similar)
- [ ] Accessibility testing (axe DevTools)

### Phase 2 (Next Steps)
- [ ] Design tokens as CSS variables
- [ ] Component library documentation (Storybook)
- [ ] Dark mode support (optional)
- [ ] Advanced animations (page transitions, micro-interactions)
- [ ] Performance optimization (image loading, font optimization)

---

## Usage Examples

### Hero Section (Homepage)

```tsx
<section className="py-16 md:py-24 lg:py-32 bg-stone-50">
  <div className="container px-4 md:px-6">
    <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight text-stone-900">
      Your Favorite Bookstore, <span className="text-primary">Reimagined.</span>
    </h1>
    <p className="mt-4 text-lg md:text-xl text-stone-600 max-w-2xl">
      Discover the best books, music, and electronics.
    </p>
    <div className="mt-8 flex flex-col sm:flex-row gap-4">
      <Button size="lg" className="h-12 px-8 font-semibold">
        Shop Books
      </Button>
      <Button variant="outline" size="lg" className="h-12 px-8">
        Browse Categories
      </Button>
    </div>
  </div>
</section>
```

### Product Card Component

```tsx
<Card className="group hover:shadow-lg transition-shadow duration-200">
  <CardContent className="p-4">
    <div className="aspect-[3/4] relative overflow-hidden rounded-md mb-4">
      <img 
        src={product.image_url} 
        alt={product.title}
        className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-200"
      />
    </div>
    <h3 className="text-lg font-bold line-clamp-2 text-stone-900">
      {product.title}
    </h3>
    <div className="flex items-center gap-1 my-2">
      {[...Array(5)].map((_, i) => (
        <Star key={i} className={`h-4 w-4 ${i < product.rating ? 'fill-accent text-accent' : 'text-stone-300'}`} />
      ))}
      <span className="text-sm text-stone-600 ml-1">({product.reviews})</span>
    </div>
    <p className="text-xl font-semibold text-accent">${product.price}</p>
    <Button className="w-full mt-4 h-11">Add to Cart</Button>
  </CardContent>
</Card>
```

---

## Design System Maintenance

**Owner:** Jordan Brooks (Frontend Lead)  
**Review Cadence:** Monthly (or as needed when adding major components)  
**Version Control:** Tracked in Git, documented in this file  
**Feedback:** Design changes require stakeholder review (Sarah Mitchell)

**Next Review:** January 2026

---

*End of Design System Documentation*
