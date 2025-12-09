# Bookstore-R-Us - Product Requirements Document

> **Version:** 3.0  
> **Status:** DRAFT  
> **Last Updated:** December 9, 2024  
> **Author:** Generated from Source Analysis

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 3.0 | 2024-12-09 | Requirements Generator | Fresh generation with user-resolved conflicts |

### Source Materials Analyzed

| Source ID | Type | Description | Date |
|-----------|------|-------------|------|
| SRC-001 | STAKEHOLDER_TRANSCRIPT | Modernization Interview - Sarah Mitchell, VP Digital Experience | 2024-12-09 |
| SRC-002 | STAKEHOLDER_TRANSCRIPT | Mobile Expansion Interview - Sarah Mitchell | 2024-12-12 |
| SRC-003 | TECHNICAL_DISCUSSION | Stack Migration Planning - Mike Chen, Priya Sharma, Jordan Brooks, Alex Kim | 2024-12-11 |
| SRC-004 | EXISTING_FUNCTIONALITY | High-Level Features & Business Rules Document | 2024-12-09 |
| SRC-005 | BUSINESS_DOCUMENT | Modernization Plan - Vision & Strategy | 2024-12 |
| SRC-006 | TECHNICAL_DISCUSSION | Architecture Diagram (Mermaid) | 2024-12 |

**Input Directory:** `docs/inputs/`

---

## 1. Executive Summary

Bookstore-R-Us is a microservices-based e-commerce platform serving approximately 6,000 products across 18 categories. The platform requires comprehensive modernization to address critical gaps: poor mobile experience (31% mobile traffic vs. 65-70% industry average), dated visual design, security vulnerabilities (hardcoded user IDs, SQL injection risks), and technical debt in the frontend codebase.

This initiative follows an **evolution, not revolution** approach using a **strangler fig pattern** to incrementally modernize the platform. The frontend will be rebuilt with Next.js and mobile-first design, while backend services migrate to Python/FastAPI over time. Security fixes are non-negotiable for Phase 1; Apple Pay/Google Pay integration is a Phase 1 stretch goal.

### Key Objectives

1. **Mobile-First Transformation** — Achieve 60%+ mobile traffic share and 2%+ mobile conversion rate (from current 0.8%)
2. **Modern Visual Experience** — Implement distinctive, warm design aesthetic ("like walking into a nice bookstore") with cream tones, serif typography, and rich accent colors
3. **Security Hardening** — Fix critical vulnerabilities including hardcoded user IDs (u1001, user_id=1), SQL/CQL injection risks, and disabled CSRF protection
4. **Technology Migration** — Incrementally migrate to unified stack: Python/FastAPI backend, Next.js frontend with Tailwind CSS (strangler fig pattern)
5. **Payment Friction Reduction** — Apple Pay and Google Pay integration (Phase 1 stretch goal)
6. **Performance** — Page load ≤2 seconds for initial render on 4G connections

### Success Metrics

| Metric | Current State | Target State | Measurement Method | Timeline |
|--------|---------------|--------------|-------------------|----------|
| Mobile Traffic Share | 31% | 60%+ | Google Analytics | Q3 2025 |
| Mobile Conversion Rate | 0.8% | 2-2.5% | E-commerce tracking | Q3 2025 |
| Mobile Cart Abandonment | 78% | <50% | Funnel analysis | Q2 2025 |
| Page Load Time (4G) | 6 seconds | ≤2 seconds | Lighthouse/WebPageTest | Q2 2025 |
| API Response Time (P95) | Not measured | ≤200ms | APM monitoring | Q2 2025 |
| Critical Security Vulnerabilities | 5 | 0 | Security audit | Q2 2025 |
| Uptime SLO | Not monitored | 99.9% | Infrastructure monitoring | Q3 2025 |

---

## 2. Stakeholder Analysis

### Primary Stakeholders

| Stakeholder | Role | Key Concerns | Priority Requirements |
|-------------|------|--------------|----------------------|
| Sarah Mitchell | VP Digital Experience | Brand perception, mobile conversion, board presentation Q2, distinctive identity | FR-001, FR-002, FR-009, UX-001 |
| Jennifer | Executive Sponsor | Digital revenue growth, competitive positioning, year-over-year growth | BR-001, BR-002 |
| Mike Chen | Technical Lead | Migration execution, organizational mandate compliance, team capacity | TR-001, TR-002 |
| Priya Sharma | Senior Backend Developer | Checkout security (SQL injection), products service migration | TR-003, NFR-005 |
| Jordan Brooks | Full-Stack Developer | Cart/login migration, frontend modernization | TR-004, FR-003 |
| Alex Kim | DevOps Engineer | Infrastructure simplification, Eureka removal, deployment | TR-005 |
| Marcus (IT Security) | Security | Hardcoded user vulnerability, CSRF disabled | NFR-005, NFR-006 |
| Priya (Marketing) | Marketing | Mobile ad campaign ROI (campaigns currently paused) | UX-002, BR-003 |

---

## 3. Current State Analysis

### Architecture Overview

| Service | Port | Database | Technology | Status |
|---------|------|----------|------------|--------|
| Eureka Server | 8761 | - | Spring Cloud Netflix | ✅ Running (to be deprecated) |
| API Gateway | 8081 | - | Spring Cloud Gateway + Feign | ✅ Running |
| Products Service | 8082 | YCQL (Cassandra) | Spring Boot + CassandraRepository | ✅ Running |
| Cart Service | 8083 | YSQL (PostgreSQL) | Spring Boot + JPA (session-scoped) | ⚠️ Session scope issues |
| Login Service | 8085 | YSQL (PostgreSQL) | Spring Security + Sessions | ⚠️ No JWT, basic auth |
| Checkout Service | 8086 | YCQL (Cassandra) | Spring Boot + raw CQL | ⚠️ Security vulnerabilities |
| React UI | 8080 | - | React + Class Components | ⚠️ Legacy patterns, 40+ CSS files |

### Existing Functionality Status

| Feature | Implementation Status | Gap Analysis |
|---------|----------------------|--------------|
| Product Catalog (6,000+ SKUs) | ✅ Fully Implemented | Missing: search bar, advanced filters |
| Category Navigation (18 categories) | ✅ Fully Implemented | Text-only links; needs visual category cards |
| Product Recommendations | ✅ Fully Implemented | Uses also_bought, also_viewed, bought_together |
| Product Sorting | ✅ Fully Implemented | By rating, reviews, sales, pageviews |
| Shopping Cart | ✅ Fully Implemented | Hardcoded user ID "u1001"; session-scoped beans |
| Checkout with Inventory | ✅ Core Implemented | SQL injection risk, hardcoded user_id=1 |
| User Authentication | ⚠️ Basic Only | BCrypt good, but session-based, no JWT/OAuth/MFA |
| Product Search | ❌ Not Implemented | Critical gap—6,000 products require search |
| Wishlists/Save for Later | ❌ Not Implemented | Critical for Gen Z cross-device behavior |
| Apple Pay / Google Pay | ❌ Not Implemented | Major mobile checkout friction |
| Order History UI | ❌ Not Implemented | Backend exists, no customer-facing view |
| Newsletter Backend | ⚠️ UI Only | Form exists, no backend integration |

### Technical Debt Register

| ID | Issue | Location | Severity | Business Impact |
|----|-------|----------|----------|-----------------|
| TD-001 | Hardcoded user_id "u1001" in cart | ShoppingCartController | CRITICAL | All cart operations attributed to wrong user |
| TD-002 | `Order.setUser_id(1)` in checkout | CheckoutServiceImpl | CRITICAL | All orders attributed to user_id=1 |
| TD-003 | Raw CQL string concatenation | CheckoutServiceImpl | CRITICAL | SQL/CQL injection vulnerability |
| TD-004 | Session-scoped beans | ShoppingCartImpl | HIGH | Breaks under load balancing |
| TD-005 | CSRF protection disabled | SecurityConfiguration | HIGH | Cross-site request forgery vulnerability |
| TD-006 | React class components | frontend/*.js | MEDIUM | Deprecated patterns |
| TD-007 | 40+ scattered CSS files | frontend/css/ | MEDIUM | No design system |
| TD-008 | 6-second page load on mobile | - | HIGH | 78% cart abandonment rate |

---

## 4. Functional Requirements

### 4.1 Visual Modernization

#### [FR-001] Modern Visual Design System
- **Priority:** MUST
- **Status:** [NEW]
- **Source(s):** SRC-001
- **Description:** Implement distinctive, warm visual design evoking "walking into a nice bookstore." Use warm tones (cream backgrounds, rich accent colors), bookish serif typography (NOT Roboto/Inter/Arial), and brand personality.
- **Acceptance Criteria:**
  - [ ] Primary font: bookish serif (e.g., Literata, Crimson Pro)
  - [ ] Color palette: cream (#FDF8F3 or similar) background, warm brown/burgundy accents
  - [ ] Design tokens implemented as CSS variables
  - [ ] Component library: shadcn/ui with custom warm theming
  - [ ] A/B test shows users describe design as "warm," "inviting," "bookstore-like" (>60% sentiment)
  - [ ] Stakeholder sign-off from Sarah Mitchell before launch

#### [FR-002] Animations and Microinteractions
- **Priority:** MUST
- **Status:** [NEW]
- **Source(s):** SRC-001
- **Description:** Add polish through page transitions, hover effects, and satisfying feedback. Current site "just kind of blinks."
- **Acceptance Criteria:**
  - [ ] Page transition animations (fade/slide) between routes
  - [ ] Product card hover: subtle scale (1.02x), shadow elevation, image zoom
  - [ ] Add-to-cart: animated feedback (item flies to cart icon, cart bounces)
  - [ ] Loading states: skeleton screens (not spinners)
  - [ ] Hero section: parallax or subtle motion (NOT static PNG)
  - [ ] Animations complete within 300ms

### 4.2 Authentication & Security

#### [FR-003] JWT User Authentication
- **Priority:** MUST
- **Status:** [MIGRATE] [RESOLVED]
- **Source(s):** SRC-001, SRC-003
- **Description:** Replace session-based auth with JWT. Fix all hardcoded user IDs.
- **Acceptance Criteria:**
  - [ ] JWT authentication with access token (15min) and refresh token (7 days)
  - [ ] Cart service uses authenticated user ID from JWT (not "u1001")
  - [ ] Checkout service creates orders with real user ID (not user_id=1)
  - [ ] Cross-device session continuity
  - [ ] BCrypt password verification maintained
  - [ ] Zero hardcoded user IDs in any service
- **Security Tests:**
  - [ ] Verify JWT signature validation
  - [ ] Verify token expiration enforcement
  - [ ] Verify user ID in orders matches authenticated user
- **Conflict Resolution:** User chose hybrid migration approach; JWT auth is Phase 1 priority

#### [FR-004] Wishlist / Save for Later
- **Priority:** SHOULD
- **Status:** [NEW]
- **Source(s):** SRC-002, SRC-004
- **Description:** Allow customers to save products for later. Critical for Gen Z cross-device behavior.
- **Acceptance Criteria:**
  - [ ] Save/unsave products with heart icon
  - [ ] Wishlist persists across sessions and devices
  - [ ] Move item from wishlist to cart in one tap
  - [ ] Wishlist accessible from account menu and bottom navigation
  - [ ] Maximum 100 items per wishlist
- **Dependencies:** FR-003 (JWT authentication)

#### [FR-005] Order History
- **Priority:** SHOULD
- **Status:** [NEW]
- **Source(s):** SRC-001, SRC-004
- **Description:** Customer-facing order history view. Backend exists but no UI.
- **Acceptance Criteria:**
  - [ ] List of past orders with order number, date, total, status
  - [ ] Order detail view showing items, quantities, prices
  - [ ] Orders sorted by date (newest first)
  - [ ] Pagination (20 per page)
- **Dependencies:** FR-003 (JWT authentication)

### 4.3 Product Discovery

#### [FR-006] Product Search
- **Priority:** SHOULD (Phase 2)
- **Status:** [NEW]
- **Source(s):** SRC-001, SRC-004
- **Description:** Full-text search for 6,000+ product catalog.
- **Acceptance Criteria:**
  - [ ] Search bar in navigation header (desktop) and bottom nav (mobile)
  - [ ] Search indexes: title, description, brand, category
  - [ ] Autocomplete suggestions after 2 characters (debounced 300ms)
  - [ ] Results ranked by relevance with text highlighting
  - [ ] No results state with suggestions
  - [ ] Search latency P95 ≤500ms
- **Technical Requirements:** Elasticsearch or OpenSearch backend

#### [FR-007] Visual Category Navigation
- **Priority:** MUST
- **Status:** [ENHANCE]
- **Source(s):** SRC-001
- **Description:** Replace text-only navigation with visual category cards.
- **Acceptance Criteria:**
  - [ ] Homepage: category cards with representative images
  - [ ] Category cards show bestseller count or "Top Picks" indicator
  - [ ] Mobile: drawer menu with category icons and images
  - [ ] Desktop: mega-menu dropdown showing subcategories
  - [ ] Touch-friendly: minimum 48px tap targets
  - [ ] Active category visually highlighted

#### [FR-008] Advanced Filtering
- **Priority:** SHOULD (Phase 2)
- **Status:** [NEW]
- **Source(s):** SRC-004
- **Description:** Filter products by price, brand, rating within category views.
- **Acceptance Criteria:**
  - [ ] Price range filter (slider or min/max inputs)
  - [ ] Brand filter (multi-select checkboxes)
  - [ ] Rating filter (4+ stars, 3+ stars, etc.)
  - [ ] Filter state preserved in URL (shareable/bookmarkable)
  - [ ] Mobile: sticky filter bar or filter sheet
  - [ ] Clear all filters button

### 4.4 Checkout & Payments

#### [FR-009] Apple Pay & Google Pay Integration
- **Priority:** SHOULD (Phase 1 Stretch Goal)
- **Status:** [NEW] [RESOLVED]
- **Source(s):** SRC-002
- **Description:** Integrate Apple Pay and Google Pay to reduce mobile checkout friction. Expected 20-30% improvement in checkout completion.
- **Acceptance Criteria:**
  - [ ] Apple Pay button on iOS Safari when available
  - [ ] Google Pay button on Android Chrome when available
  - [ ] Express checkout option (skip address form if payment method has it)
  - [ ] Graceful fallback to standard checkout if wallet unavailable
  - [ ] Error handling: clear messaging for declined payments
- **Conflict Resolution:** User designated as Phase 1 stretch goal—try for Phase 1, acceptable to slip to Phase 2 if needed
- **Success Metric:** Mobile checkout completion rate increases by ≥15%

#### [FR-010] Mobile Checkout Redesign
- **Priority:** MUST
- **Status:** [ENHANCE]
- **Source(s):** SRC-001, SRC-002
- **Description:** Redesign checkout for mobile-first experience.
- **Acceptance Criteria:**
  - [ ] Single-column layout on mobile (<768px)
  - [ ] Progress indicator (steps: Cart → Shipping → Payment → Confirm)
  - [ ] Form fields minimum 16px font (prevents iOS zoom)
  - [ ] Touch targets minimum 44px height
  - [ ] Autofill support (autocomplete attributes)
  - [ ] Address validation with suggestions
  - [ ] Visual order summary visible throughout

### 4.5 Mobile Experience

#### [FR-011] Bottom Navigation Bar
- **Priority:** MUST
- **Status:** [NEW]
- **Source(s):** SRC-002
- **Description:** Implement thumb-zone navigation for mobile.
- **Acceptance Criteria:**
  - [ ] Bottom nav visible on all pages (mobile only, <768px)
  - [ ] Navigation items: Home, Categories, Search, Cart, Account
  - [ ] Active state clearly indicated
  - [ ] Cart shows item count badge
  - [ ] Safe area insets respected (notched phones)

#### [FR-012] Progressive Web App (PWA)
- **Priority:** SHOULD
- **Status:** [NEW]
- **Source(s):** SRC-002
- **Description:** Enable PWA capabilities for Android install and improved mobile experience.
- **Acceptance Criteria:**
  - [ ] Web app manifest with name, icons, theme color
  - [ ] Service worker for offline product browsing
  - [ ] Add to home screen prompt on Android
  - [ ] Splash screen on launch
  - [ ] Works offline: displays cached products, queues cart actions

#### [FR-013] Social Sharing
- **Priority:** SHOULD
- **Status:** [NEW]
- **Source(s):** SRC-002
- **Description:** Enable easy sharing of products to social media platforms.
- **Acceptance Criteria:**
  - [ ] Share button on product detail pages
  - [ ] Native share sheet on mobile (Web Share API)
  - [ ] Fallback: Copy link, Email, Facebook, Twitter/X, Pinterest
  - [ ] Open Graph meta tags for shared links
  - [ ] UTM tracking on shared links

---

## 5. Non-Functional Requirements

### 5.1 Performance

| ID | Requirement | Target | Measurement | Priority | Source |
|----|-------------|--------|-------------|----------|--------|
| NFR-001 | Page load time (initial) | ≤2 seconds | Lighthouse Score ≥90 | MUST | SRC-002, SRC-004 |
| NFR-002 | API Response Time (P95) | ≤200ms | APM/tracing | MUST | SRC-004 |
| NFR-003 | First Contentful Paint | <1.5 seconds | Lighthouse | SHOULD | SRC-002 |
| NFR-004 | JavaScript bundle (initial) | <200KB gzipped | Webpack analyzer | SHOULD | SRC-002 |
| NFR-005 | Time to Interactive | <3 seconds | Lighthouse | SHOULD | SRC-002 |
| NFR-006 | Image optimization | WebP format, lazy loading | Audit | MUST | SRC-002 |

**Conflict Resolution:** User chose **≤2 seconds** (more aggressive target for Gen Z expectations)

### 5.2 Security

| ID | Requirement | Implementation | Priority | Source |
|----|-------------|----------------|----------|--------|
| NFR-007 | Eliminate SQL/CQL injection | Parameterized queries everywhere | MUST | SRC-003 |
| NFR-008 | Remove hardcoded user IDs | User ID from JWT token only | MUST | SRC-001, SRC-003 |
| NFR-009 | JWT authentication | Access + refresh token pattern | MUST | SRC-003 |
| NFR-010 | CSRF protection | Re-enable with proper token validation | MUST | SRC-003 |
| NFR-011 | Rate limiting | 100 requests/minute per IP on auth | SHOULD | SRC-001 |
| NFR-012 | HTTPS/TLS | TLS 1.2+ on all endpoints | MUST | SRC-004 |
| NFR-013 | Password storage | BCrypt (maintain existing) | MUST | SRC-001 |

### 5.3 Scalability & Reliability

| ID | Requirement | Target | Priority | Source |
|----|-------------|--------|----------|--------|
| NFR-014 | Concurrent users | 10,000+ simultaneous sessions | SHOULD | SRC-004 |
| NFR-015 | Uptime SLO | 99.9% availability | SHOULD | SRC-004 |
| NFR-016 | Stateless services | Database/JWT state only | MUST | SRC-003 |
| NFR-017 | Zero-downtime deployments | Blue-green or rolling | SHOULD | SRC-004 |
| NFR-018 | Circuit breakers | Graceful degradation | SHOULD | SRC-004 |

### 5.4 Accessibility

| ID | Requirement | Target | Priority | Source |
|----|-------------|--------|----------|--------|
| NFR-019 | Touch targets | 44px minimum (48px preferred) | MUST | SRC-002 |
| NFR-020 | WCAG compliance | Level AA | SHOULD | SRC-004 |
| NFR-021 | Keyboard navigation | Full support | SHOULD | SRC-004 |
| NFR-022 | Color contrast | 4.5:1 minimum for text | SHOULD | SRC-004 |
| NFR-023 | Screen reader support | Semantic HTML, ARIA labels | SHOULD | SRC-004 |

---

## 6. Technical Requirements

| ID | Requirement | Rationale | Source | Owner |
|----|-------------|-----------|--------|-------|
| TR-001 | Migrate frontend to Next.js 14 | Modern React (App Router), SSR, hooks | SRC-003 | Jordan |
| TR-002 | Implement Tailwind CSS + shadcn/ui | Replace 40+ scattered CSS files | SRC-003 | Jordan |
| TR-003 | Migrate backend services to FastAPI | Organizational mandate, Python ecosystem | SRC-003, SRC-005 | Priya |
| TR-004 | Make cart service stateless | Fix session-scoped beans | SRC-003 | Jordan |
| TR-005 | Remove Eureka, use env vars + K8s | Simplify infrastructure | SRC-003 | Alex |
| TR-006 | Unify database on YSQL (PostgreSQL) | Eliminate YCQL complexity | SRC-003 | Priya |
| TR-007 | PWA capabilities | Android install, offline browse | SRC-002 | Jordan |
| TR-008 | Async HTTP with HTTPX | Replace synchronous Feign clients | SRC-003 | Priya |

### Technology Stack Migration

| Layer | Current | Target | Rationale |
|-------|---------|--------|-----------|
| Frontend Framework | React (class components) | Next.js 14 (App Router) | Modern patterns, SSR |
| Styling | Bootstrap + 40+ CSS files | Tailwind CSS + shadcn/ui | Design system |
| UI Components | react-materialize, react-bootstrap | shadcn/ui (Radix primitives) | Accessibility |
| Backend Framework | Spring Boot (Java) | FastAPI (Python) | Org mandate |
| Authentication | Spring Security (sessions) | FastAPI + JWT | Stateless |
| Database | YCQL + YSQL hybrid | YSQL only (PostgreSQL) | Simplification |
| Service Discovery | Eureka Server | Environment variables / K8s DNS | Complexity reduction |
| Inter-service HTTP | Feign clients (sync) | HTTPX (async) | Performance |

### Migration Order (Strangler Fig Pattern)

| Order | Service | Phase | Owner | Complexity |
|-------|---------|-------|-------|------------|
| 1 | Frontend (Next.js) | Phase 1 | Jordan | High |
| 2 | Products Service | Phase 1 | Priya | Medium |
| 3 | Cart Service | Phase 1 | Jordan | Low |
| 4 | Login Service | Phase 2 | Jordan | Medium |
| 5 | Checkout Service | Phase 2 | Priya | High |
| 6 | API Gateway | Phase 2 | Alex | Medium |

**Conflict Resolution:** User chose **Hybrid/Strangler Fig pattern** — migrate incrementally, frontend-first

---

## 7. User Experience Requirements

### Design Principles

1. **Warm & Distinctive** — "Like walking into a nice bookstore" — cream tones, rich accents, serif typography
2. **Mobile-First** — Design for mobile viewport first, scale up to desktop
3. **Thumb-Zone Aware** — Key actions in bottom 2/3 of mobile screen
4. **Performance is UX** — ≤2 second loads are mandatory
5. **Satisfying Feedback** — Amazon/Target quality interactions

### Specific UX Requirements

| ID | Requirement | Acceptance Criteria | Priority | Source |
|----|-------------|---------------------|----------|--------|
| UX-001 | Distinctive typography | Serif primary font; consistent type scale | MUST | SRC-001 |
| UX-002 | Bottom navigation (mobile) | Home, Categories, Search, Cart, Account | MUST | SRC-002 |
| UX-003 | Feed-style product browsing | Vertical scroll, full-width cards on mobile | MUST | SRC-002 |
| UX-004 | Preserved scroll position | Back navigation returns to previous position | SHOULD | SRC-002 |
| UX-005 | Sticky filter bar | Filters accessible while scrolling | SHOULD | SRC-002 |
| UX-006 | Swipeable product images | Gesture-based image gallery | SHOULD | SRC-002 |
| UX-007 | Skeleton loading states | Content placeholder during fetch | MUST | SRC-002 |

---

## 8. Business Requirements

| ID | Requirement | Business Driver | Success Metric | Source |
|----|-------------|-----------------|----------------|--------|
| BR-001 | Triple mobile conversion | Revenue growth | 0.8% → 2%+ conversion | SRC-002 |
| BR-002 | Capture Gen Z demographic | Customer diversification | Mobile traffic 31% → 60%+ | SRC-002 |
| BR-003 | Enable mobile ad campaigns | Marketing ROI | Campaigns resumed; positive ROAS | SRC-002 |
| BR-004 | Board presentation Q2 2025 | Executive visibility | Live demo of Phase 1 | SRC-001 |
| BR-005 | Year-over-year digital growth | Competitive positioning | >8% YoY growth | SRC-002 |

---

## 9. Constraints & Assumptions

### Constraints

| ID | Constraint | Type | Impact | Source |
|----|------------|------|--------|--------|
| CON-001 | Python/FastAPI organizational mandate | Technical | Backend migration required | SRC-003 |
| CON-002 | Board presentation Q2 2025 | Timeline | Phase 1 complete by May 2025 | SRC-001 |
| CON-003 | No native app budget | Financial | PWA approach; native deferred | SRC-002 |
| CON-004 | BCrypt password compatibility | Technical | Existing users must not need password reset | SRC-003 |
| CON-005 | Parallel deployment required | Operational | Java and Python run simultaneously | SRC-003 |

### Assumptions

| ID | Assumption | Risk if Invalid | Mitigation |
|----|------------|-----------------|------------|
| ASM-001 | PWA sufficient without native app | Mobile metrics may not improve | Monitor Q3; revisit native if needed |
| ASM-002 | Apple Pay/Google Pay lifts conversion 20-30% | Investment ROI not achieved | A/B test before full rollout |
| ASM-003 | Strangler fig won't cause disruptions | User-facing errors during migration | Feature flags, canary deployments |
| ASM-004 | Team has capacity for timeline | Deadline missed | Weekly velocity tracking |

---

## 10. Resolved Conflicts

**All conflicts were resolved with user input before PRD generation.**

| ID | Conflict | User Decision | Rationale |
|----|----------|---------------|-----------|
| CONFLICT-001 | Backend: Keep Java vs. Full Python migration | **C) Hybrid - Strangler fig pattern, frontend-first** | Balance org mandate with practical execution; prioritize customer-facing changes |
| CONFLICT-002 | Page load target: 3s vs 2s | **B) ≤2 seconds** | More aggressive target aligns with Gen Z expectations |
| CONFLICT-003 | Apple/Google Pay: Phase 1 vs Phase 2 | **C) Phase 1 stretch goal** | Try for Phase 1, acceptable to slip if needed |

---

## 11. Phasing & Roadmap

### Phase 1 (Q2 2025 - Board Presentation)

**Frontend (Owner: Jordan):**
- [ ] Next.js 14 with App Router
- [ ] Tailwind CSS + shadcn/ui component library
- [ ] Warm visual design (cream, serif, distinctive)
- [ ] Mobile-first responsive design
- [ ] Bottom navigation bar
- [ ] Animations and microinteractions
- [ ] PWA manifest + service worker
- [ ] Performance ≤2 seconds page load

**Security (Owner: Priya/Jordan):**
- [ ] JWT authentication implementation
- [ ] Remove all hardcoded user IDs (u1001, user_id=1)
- [ ] Parameterized queries in all services
- [ ] Re-enable CSRF protection

**Payments (Owner: TBD) — Stretch Goal:**
- [ ] Apple Pay integration
- [ ] Google Pay integration

**Backend Migration (Owner: Priya):**
- [ ] Products service → FastAPI
- [ ] Cart service → FastAPI (stateless)

### Phase 2 (Q3 2025)

- [ ] Product search (Elasticsearch/OpenSearch)
- [ ] Login service → FastAPI
- [ ] Checkout service → FastAPI
- [ ] Order history UI
- [ ] Wishlists / Save for Later
- [ ] Advanced filtering
- [ ] Apple Pay/Google Pay (if not Phase 1)

### Phase 3 (Q4 2025)

- [ ] API Gateway migration
- [ ] Remove Eureka Server
- [ ] Customer profiles
- [ ] Email notifications
- [ ] Full observability (distributed tracing, metrics)

---

## 12. Out of Scope

| Item | Reason | Future Consideration |
|------|--------|---------------------|
| Native iOS/Android apps | No budget; PWA first | Revisit Q4 2025 if metrics don't improve |
| Live shopping events | Not ready; requires content capability | Phase 4+ |
| AI personalization | Requires Python migration completion | Phase 4+ |
| Multi-language support | Not requested by stakeholders | Future international expansion |
| Saved payment methods | PCI compliance complexity | Phase 3+ |
| Guest checkout | Conflicts with cross-device sync | Revisit post-Phase 2 |

---

## 13. Open Questions

| ID | Question | Owner | Status | Due Date |
|----|----------|-------|--------|----------|
| Q-001 | Apple Pay/Google Pay budget approval? | Sarah | OPEN | Jan 2025 |
| Q-002 | Brand guidelines for visual design? | Sarah | OPEN | Jan 2025 |
| Q-003 | Search service: OpenSearch vs Elasticsearch? | Alex | OPEN | Phase 2 |
| Q-004 | Redis hosting approach for sessions/cache? | Alex | OPEN | Phase 1 |
| Q-005 | Security audit vendor selection? | Marcus | OPEN | Q1 2025 |

---

## 14. Glossary

| Term | Definition |
|------|------------|
| ASIN | Product identifier (Amazon Standard Identification Number format) |
| Customer | External person using the Bookstore-R-Us platform |
| JWT | JSON Web Token — stateless authentication token |
| PWA | Progressive Web App — web application with native-like capabilities |
| Service | Backend microservice (e.g., Products Service, Cart Service) |
| API | Application Programming Interface — external-facing endpoints |
| Strangler Fig | Migration pattern where new system gradually replaces old |
| YCQL | Yugabyte Cassandra Query Language (being deprecated) |
| YSQL | Yugabyte SQL — PostgreSQL-compatible query language |
| shadcn/ui | React component library built on Radix primitives |

---

## 15. Appendices

### A. Source Summaries

**SRC-001 (Modernization Interview):** Sarah Mitchell emphasized distinctive "bookstore" identity (warm, not generic corporate), security concerns (hardcoded users), mobile improvements, and board presentation deadline Q2.

**SRC-002 (Mobile Interview):** Critical mobile gap — 31% traffic vs 65-70% industry average, 0.8% conversion vs 3.2% desktop, 78% cart abandonment. Mobile-first redesign, PWA, Apple Pay/Google Pay essential.

**SRC-003 (Tech Discussion):** Python/FastAPI mandate from org, Next.js/Tailwind for frontend, strangler fig migration approach, security fixes (SQL injection, hardcoded IDs) non-negotiable.

**SRC-004 (Features Doc):** Comprehensive current implementation status. 6,000 SKUs, 18 categories, 42 documented business rules. Gaps: search, payments, wishlists, order history UI.

**SRC-005 (Modernization Plan):** Evolution not revolution philosophy. API-first, traceability, living documentation. Defines modernization process framework.

**SRC-006 (Architecture):** 6 Spring Boot services (Eureka, Gateway, Products, Cart, Checkout, Login). Feign clients for inter-service. YCQL/YSQL hybrid database layer.

### B. Requirement Traceability Matrix

| Requirement | Source(s) | Related Requirements |
|-------------|-----------|---------------------|
| FR-001 Visual Design | SRC-001 | UX-001 |
| FR-002 Animations | SRC-001 | FR-001 |
| FR-003 JWT Auth | SRC-001, SRC-003 | NFR-008, NFR-009, TD-001, TD-002 |
| FR-009 Apple/Google Pay | SRC-002 | FR-010, BR-001 |
| FR-011 Bottom Nav | SRC-002 | UX-002 |
| NFR-001 Page Load ≤2s | SRC-002, SRC-004 | NFR-003, NFR-004 |
| TR-003 FastAPI Migration | SRC-003, SRC-005 | CON-001 |

---

*Document generated from `docs/inputs/` source analysis*  
*All conflicts resolved with user input*  
*Ready for stakeholder review*
