# Bookstore-R-Us - Product Requirements Document

> **Version:** 2.0  
> **Status:** DRAFT  
> **Last Updated:** December 9, 2024  
> **Author:** Generated from Source Analysis

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.0 | 2024-12-09 | Requirements Generator | Regenerated with additional source materials (architecture, features, modernization plan) |
| 1.0 | 2024-12-09 | Requirements Generator | Initial generation |

### Source Materials Analyzed

| Source ID | Type | Description | Date |
|-----------|------|-------------|------|
| SRC-001 | STAKEHOLDER_TRANSCRIPT | Stakeholder Interview - VP Digital Experience (Sarah Mitchell) - Modernization Initiative | 2024-12-09 |
| SRC-002 | TECHNICAL_DISCUSSION | Technical Team Migration Planning (Mike Chen, Priya Sharma, Jordan Brooks, Alex Kim) | 2024-12-11 |
| SRC-003 | STAKEHOLDER_TRANSCRIPT | Stakeholder Interview - Mobile User Expansion Strategy (Sarah Mitchell) | 2024-12-12 |
| SRC-004 | TECHNICAL_DISCUSSION | Architecture Diagram - Microservices Component & Class Structure | 2024-12 |
| SRC-005 | EXISTING_FUNCTIONALITY | High-Level Features Document - Current Implementation Status | 2024-12-09 |
| SRC-006 | BUSINESS_DOCUMENT | Modernization Plan - Vision, Framework & Roadmap | 2024-12 |

---

## 1. Executive Summary

Bookstore-R-Us is undergoing a comprehensive modernization initiative to transform from a functional but dated e-commerce platform into a modern, mobile-first, cloud-native marketplace. The platform currently serves ~6,000 products across 18 categories with core e-commerce workflows implemented, but suffers from critical gaps in mobile experience (31% mobile traffic vs. 65-70% industry average), security vulnerabilities (hardcoded user IDs, SQL injection risks), and aging technology (class-based React components, session-based authentication).

This initiative follows an **evolution, not revolution** philosophy with a machine-augmented, human-directed modernization engine. The approach uses a strangler fig pattern to incrementally replace modules while maintaining continuity, with the legacy spec as a factual baseline.

### Key Objectives

1. **Mobile-First Transformation** — Redesign with mobile as primary target; achieve 60%+ mobile traffic share and 2%+ mobile conversion (up from 0.8%)
2. **Modern Visual Experience** — Implement distinctive, warm design aesthetic ("like walking into a nice bookstore") with animations and microinteractions
3. **Security Hardening** — Fix critical vulnerabilities including hardcoded user IDs, SQL injection, and implement JWT authentication
4. **Technology Migration** — Migrate to unified stack: Python/FastAPI backend, Next.js frontend with Tailwind CSS per organizational mandate
5. **Performance Optimization** — Achieve <3 second page load on 4G (currently 6 seconds), support 10,000+ concurrent users
6. **AI/ML Enablement** — Position architecture for future AI-assisted features leveraging Python ecosystem

### Success Metrics

| Metric | Current State | Target State | Timeline |
|--------|---------------|--------------|----------|
| Mobile Traffic Share | 31% | 60%+ | Q3 2025 |
| Mobile Conversion Rate | 0.8% | 2-2.5% | Q3 2025 |
| Desktop Conversion Rate | 3.2% | 4%+ | Q3 2025 |
| Mobile Cart Abandonment | 78% | <50% | Q2 2025 |
| Page Load Time (4G) | 6 seconds | <3 seconds | Q2 2025 |
| API Response Time (P95) | Not measured | ≤200ms | Q2 2025 |
| Uptime SLO | Not monitored | 99.9% | Q3 2025 |
| Concurrent Users | Not tested | 10,000+ | Q3 2025 |
| Security Vulnerabilities | 5 critical | 0 critical | Q2 2025 |

---

## 2. Stakeholder Analysis

### Primary Stakeholders

| Stakeholder | Role | Key Concerns | Priority Requirements |
|-------------|------|--------------|----------------------|
| Sarah Mitchell | VP Digital Experience | Brand perception, mobile conversion, competitive positioning, board presentation Q2 | FR-001, FR-002, UX-001, NFR-001 |
| Jennifer (Executive Team) | Executive Sponsor | Digital revenue growth, market share, ROI | BR-001, BR-002 |
| Mike Chen | Technical Lead, Platform Engineering | Code quality, migration risk, team execution, org mandate compliance | TR-001, TR-002, TR-003 |
| Priya Sharma | Senior Backend Developer | Backend migration complexity, checkout service security | TR-004, TR-005 |
| Jordan Brooks | Full-Stack Developer | Frontend modernization, auth implementation | TR-006, FR-003 |
| Alex Kim | DevOps Engineer | Infrastructure simplification, deployment automation | TR-007, NFR-003 |
| Marketing Team | Marketing | Mobile ad campaign ROI, customer acquisition, Gen Z capture | UX-002, FR-004 |
| Marcus (IT Security) | Security | Hardcoded user vulnerability, authentication gaps | NFR-005, NFR-006 |

### Stakeholder Priority Matrix

| Requirement Area | Sarah Mitchell | Tech Team | Executive | Marketing |
|------------------|----------------|-----------|-----------|-----------|
| Visual Modernization | HIGH | MEDIUM | MEDIUM | HIGH |
| Mobile Experience | HIGH | HIGH | HIGH | HIGH |
| Security Fixes | HIGH | HIGH | HIGH | MEDIUM |
| Backend Migration | LOW | HIGH | HIGH | LOW |
| Payment Integration | HIGH | MEDIUM | HIGH | HIGH |
| Search Functionality | HIGH | MEDIUM | MEDIUM | HIGH |
| Performance | MEDIUM | HIGH | MEDIUM | HIGH |

---

## 3. Current State Analysis

### 3.1 Architecture Overview

The platform consists of 6 Spring Boot microservices with React frontend:

| Service | Port | Database | Current Status |
|---------|------|----------|----------------|
| Eureka Server | 8761 | - | ✅ Running (to be deprecated) |
| API Gateway | 8081 | - | ✅ Running |
| Products Service | 8082 | YCQL (Cassandra) + YSQL | ✅ Running |
| Cart Service | 8083 | YSQL (PostgreSQL) | ⚠️ Session-scoped issues |
| Login Service | 8085 | YSQL (PostgreSQL) | ⚠️ Basic implementation |
| Checkout Service | 8086 | YCQL (Cassandra) | ⚠️ Security vulnerabilities |
| React UI | 8080 | - | ⚠️ Outdated patterns |

### 3.2 Existing Functionality

| Feature | Current Status | Gap Analysis |
|---------|----------------|--------------|
| Product Catalog (6,000+ SKUs) | ✅ Implemented | Missing search, filtering, sorting |
| Category Navigation (18 categories) | ✅ Implemented | Needs visual enhancement |
| Product Recommendations | ✅ Implemented | Based on also_bought/also_viewed data |
| Shopping Cart | ✅ Implemented | Hardcoded user ID (u1001), no wishlist |
| Checkout with Inventory | ✅ Core Implemented | No payment, hardcoded user, SQL injection |
| User Authentication | ⚠️ Partial | Session-based, not integrated, no JWT |
| Order Records | ✅ Implemented | No user-facing history (all orders → user_id=1) |
| Product Reviews | ⚠️ Display Only | Cannot write reviews |
| Service Discovery | ✅ Implemented | Eureka (to be replaced) |
| Product Search | ❌ Missing | Critical gap |
| Wishlists | ❌ Missing | Feature not built |
| Payment Processing | ❌ Missing | No gateway integration |
| Apple Pay / Google Pay | ❌ Missing | Major mobile friction |
| Order History View | ❌ Missing | Backend exists, no UI |

### 3.3 Technical Debt / Known Issues

| Issue ID | Description | Severity | Impact |
|----------|-------------|----------|--------|
| TD-001 | Hardcoded user_id "u1001" in cart service | CRITICAL | All carts share same user |
| TD-002 | `Order.setUser_id(1)` in checkout | CRITICAL | All orders attributed to user 1 |
| TD-003 | Raw CQL string concatenation | CRITICAL | SQL injection vulnerability |
| TD-004 | Session-scoped beans in microservices | HIGH | Breaks with load balancing |
| TD-005 | CSRF protection disabled | HIGH | Security vulnerability |
| TD-006 | React class components with deprecated lifecycle | MEDIUM | `componentWillReceiveProps`, maintenance burden |
| TD-007 | Scattered CSS files (40+ directories) | MEDIUM | Inconsistent styling |
| TD-008 | YCQL/YSQL hybrid data model | MEDIUM | Operational complexity |
| TD-009 | No parameterized queries in checkout | CRITICAL | Injection risk |
| TD-010 | 6-second page load on mobile | HIGH | User abandonment |

---

## 4. Functional Requirements

### 4.1 Visual Modernization

#### [FR-001] Modern Visual Design System
- **Priority:** MUST
- **Status:** [NEW]
- **Source(s):** SRC-001, SRC-003, SRC-006
- **Description:** Implement a distinctive, warm visual design that evokes "walking into a nice bookstore." The design must avoid generic corporate/AI aesthetics and establish a unique brand identity with personality and warmth.
- **Acceptance Criteria:**
  - [ ] Typography system with distinctive, non-generic fonts (avoid Inter, Roboto, Arial)
  - [ ] Warm color palette (cream tones, rich accents, bookish feel)
  - [ ] Design tokens/CSS variables for consistency
  - [ ] Component library using shadcn/ui with custom theming
  - [ ] Visual distinction from competitors
  - [ ] WCAG AA compliance for accessibility
- **Dependencies:** TR-006
- **Notes:** Sarah: "If it could feel like walking into a nice bookstore? That vibe? That would be amazing."

#### [FR-002] Animations and Microinteractions
- **Priority:** MUST
- **Status:** [NEW]
- **Source(s):** SRC-001
- **Description:** Add polish through animations and microinteractions including page transitions, hover effects, and satisfying add-to-cart feedback comparable to Amazon/Target.
- **Acceptance Criteria:**
  - [ ] Page transition animations
  - [ ] Product card hover effects with visual feedback
  - [ ] Add-to-cart animation with satisfying feedback
  - [ ] Loading state animations (skeleton screens)
  - [ ] Smooth scroll behaviors
  - [ ] Hero section with interactivity (not static PNG)
- **Dependencies:** FR-001, TR-006

### 4.2 Authentication & User Management

#### [FR-003] Proper User Authentication Flow
- **Priority:** MUST
- **Status:** [MIGRATE]
- **Source(s):** SRC-001, SRC-002, SRC-005
- **Description:** Implement complete JWT-based user authentication that flows through all services. Replace hardcoded user IDs with actual authenticated user identity. Enable cross-device session continuity.
- **Acceptance Criteria:**
  - [ ] JWT-based authentication replacing session-based auth
  - [ ] User ID flows from auth token to all service calls
  - [ ] Cart associated with authenticated user (not hardcoded u1001)
  - [ ] Orders created with actual user ID (not hardcoded 1)
  - [ ] Cross-device session continuity via tokens
  - [ ] Proper logout with token invalidation
  - [ ] BCrypt password compatibility with existing users
- **Dependencies:** TR-004, TR-005
- **Notes:** Marcus from IT Security flagged hardcoded user as critical concern

#### [FR-004] Wishlist / Save for Later
- **Priority:** SHOULD
- **Status:** [NEW]
- **Source(s):** SRC-003, SRC-005
- **Description:** Allow users to save products for later purchase. Essential for cross-device shopping behavior and younger demographics who browse on mobile, buy later.
- **Acceptance Criteria:**
  - [ ] Save/unsave products to wishlist
  - [ ] Wishlist persists across sessions and devices
  - [ ] Move items from wishlist to cart
  - [ ] Share wishlist functionality
  - [ ] Wishlist count in navigation
- **Dependencies:** FR-003

#### [FR-005] Order History
- **Priority:** SHOULD
- **Status:** [NEW]
- **Source(s):** SRC-001, SRC-005
- **Description:** Provide users visibility into their past orders. Backend order records exist but no UI is available.
- **Acceptance Criteria:**
  - [ ] List of past orders with dates and totals
  - [ ] Order detail view with items purchased
  - [ ] Order status tracking (if fulfillment added)
  - [ ] Reorder functionality
- **Dependencies:** FR-003

### 4.3 Product Discovery

#### [FR-006] Product Search
- **Priority:** SHOULD
- **Status:** [NEW]
- **Source(s):** SRC-001, SRC-005
- **Description:** Implement full-text product search functionality. With 6,000+ products, customers cannot effectively browse without search. Sarah: "People expect to type in what they want and find it."
- **Acceptance Criteria:**
  - [ ] Search bar prominently in navigation
  - [ ] Full-text search across title, description, brand
  - [ ] Search suggestions/autocomplete
  - [ ] Search results with relevance ranking
  - [ ] Filter search results by category, price, rating
  - [ ] Mobile-optimized search experience
- **Dependencies:** Backend search service (Elasticsearch/OpenSearch)
- **Notes:** Phase 2 feature per stakeholder prioritization

#### [FR-007] Enhanced Category Navigation
- **Priority:** MUST
- **Status:** [ENHANCE]
- **Source(s):** SRC-001, SRC-005
- **Description:** Transform utilitarian text-based navigation into visual category browsing with imagery and better discovery.
- **Acceptance Criteria:**
  - [ ] Visual category cards with imagery on homepage
  - [ ] Touch-friendly category navigation
  - [ ] Mobile drawer/hamburger menu
  - [ ] Bestseller highlights per category (Books, Music, Beauty, Electronics)
  - [ ] Support for all 18 categories
- **Dependencies:** FR-001, UX-002

#### [FR-008] Advanced Product Filtering
- **Priority:** SHOULD
- **Status:** [NEW]
- **Source(s):** SRC-005
- **Description:** Add filtering capabilities to help users narrow product results.
- **Acceptance Criteria:**
  - [ ] Filter by price range
  - [ ] Filter by brand
  - [ ] Filter by rating
  - [ ] Sticky filter bar on mobile
  - [ ] Preserved filters on back navigation
- **Dependencies:** FR-007

### 4.4 Checkout & Payments

#### [FR-009] Mobile Payment Integration
- **Priority:** MUST
- **Status:** [NEW]
- **Source(s):** SRC-003
- **Description:** Integrate Apple Pay and Google Pay to dramatically reduce mobile checkout friction. Studies show 20-30% improvement in mobile checkout completion.
- **Acceptance Criteria:**
  - [ ] Apple Pay integration on iOS Safari
  - [ ] Google Pay integration on Android browsers
  - [ ] Payment method selection UI
  - [ ] Fallback to standard checkout
  - [ ] Proper error handling for failed payments
- **Dependencies:** TR-005

#### [FR-010] Checkout Flow Improvements
- **Priority:** MUST
- **Status:** [ENHANCE]
- **Source(s):** SRC-001, SRC-003, SRC-005
- **Description:** Redesign checkout for mobile-first experience with progress indicators, better form UX, and visual feedback.
- **Acceptance Criteria:**
  - [ ] Progress indicator showing checkout steps
  - [ ] Single-column mobile layout
  - [ ] Large, touch-friendly form fields (44px+ touch targets)
  - [ ] Autofill support for addresses
  - [ ] Order summary always visible
  - [ ] Visual confirmation on successful order
  - [ ] Order number display (format: #kmp-{orderNumber})
- **Dependencies:** UX-002, TR-005

### 4.5 Marketing & Engagement

#### [FR-011] Newsletter Integration
- **Priority:** COULD
- **Status:** [ENHANCE]
- **Source(s):** SRC-005
- **Description:** Connect newsletter UI to backend email marketing service.
- **Acceptance Criteria:**
  - [ ] Email validation
  - [ ] Backend integration with email service
  - [ ] Success/error feedback
- **Dependencies:** External email service

#### [FR-012] Social Sharing
- **Priority:** COULD
- **Status:** [NEW]
- **Source(s):** SRC-003
- **Description:** Enable easy product sharing to social media for Gen Z engagement.
- **Acceptance Criteria:**
  - [ ] Share buttons on product pages
  - [ ] Open Graph meta tags for rich previews
  - [ ] Copy link functionality
- **Dependencies:** None

---

## 5. Non-Functional Requirements

### 5.1 Performance

| ID | Requirement | Metric | Target | Priority |
|----|-------------|--------|--------|----------|
| NFR-001 | Page load time on mobile 4G | Time to Interactive | <3 seconds | MUST |
| NFR-002 | First Contentful Paint | FCP | <1.5 seconds | MUST |
| NFR-003 | API Response Time | P95 Latency | ≤200ms | MUST |
| NFR-004 | JavaScript bundle size | Compressed KB | <200KB initial | SHOULD |
| NFR-005 | Image optimization | Format/size | WebP, lazy loaded | MUST |

**Source(s):** SRC-003, SRC-005

**Implementation Notes:**
- Currently 6 seconds on 4G - unacceptable
- Image optimization required
- JavaScript bundle reduction via code splitting
- Implement caching strategy
- Lazy loading for below-fold content
- CDN for static assets

### 5.2 Security

| ID | Requirement | Compliance | Priority |
|----|-------------|------------|----------|
| NFR-006 | Eliminate SQL/CQL injection | OWASP Top 10 | MUST |
| NFR-007 | Parameterized queries everywhere | OWASP Top 10 | MUST |
| NFR-008 | JWT token authentication | Industry Standard | MUST |
| NFR-009 | CSRF protection | OWASP Top 10 | MUST |
| NFR-010 | Rate limiting on auth endpoints | Industry Standard | SHOULD |
| NFR-011 | HTTPS/TLS for all traffic | Industry Standard | MUST |
| NFR-012 | Secure password storage | BCrypt | ✅ EXISTS |
| NFR-013 | XSS protection | OWASP Top 10 | MUST |

**Source(s):** SRC-001, SRC-002, SRC-005

### 5.3 Scalability

| ID | Requirement | Metric | Target | Priority |
|----|-------------|--------|--------|----------|
| NFR-014 | Concurrent users | Simultaneous sessions | 10,000+ | SHOULD |
| NFR-015 | Horizontal scaling | Service instances | Auto-scale 1-10 | SHOULD |
| NFR-016 | Stateless services | Session storage | Database/JWT only | MUST |
| NFR-017 | Database connection pooling | Connections | 100 concurrent | SHOULD |

### 5.4 Reliability & Availability

| ID | Requirement | Metric | Target | Priority |
|----|-------------|--------|--------|----------|
| NFR-018 | Uptime SLO | Percentage | 99.9% | SHOULD |
| NFR-019 | Zero-downtime deployments | Deployment strategy | Blue-green/canary | SHOULD |
| NFR-020 | Circuit breakers | Fault isolation | Per service | SHOULD |
| NFR-021 | Graceful degradation | Fallback strategies | Defined per service | SHOULD |

### 5.5 Accessibility

| ID | Requirement | Standard | Target | Priority |
|----|-------------|----------|--------|----------|
| NFR-022 | Touch target size | WCAG 2.1 | 44px minimum | MUST |
| NFR-023 | Color contrast | WCAG 2.1 AA | 4.5:1 minimum | SHOULD |
| NFR-024 | Keyboard navigation | WCAG 2.1 | Full support | SHOULD |
| NFR-025 | Screen reader compatibility | WCAG 2.1 | ARIA labels | SHOULD |
| NFR-026 | Alternative text | WCAG 2.1 | All images | SHOULD |

---

## 6. Technical Requirements

| ID | Requirement | Rationale | Source |
|----|-------------|-----------|--------|
| TR-001 | Migrate backend to Python/FastAPI | Organizational mandate - unified stack, AI/ML enablement | SRC-002, SRC-006 |
| TR-002 | Migrate frontend to Next.js | Modern React, SSR for SEO, App Router, hooks | SRC-002, SRC-006 |
| TR-003 | Unify database on YSQL (PostgreSQL) | Eliminate YCQL complexity, simplify operations | SRC-002 |
| TR-004 | Implement stateless cart service | Current session-scoped pattern breaks load balancing | SRC-002, SRC-004 |
| TR-005 | Rewrite checkout with parameterized queries | Security - eliminate injection risk | SRC-002 |
| TR-006 | Implement Tailwind CSS + shadcn/ui | Replace scattered CSS, consistent components | SRC-002, SRC-006 |
| TR-007 | Remove Eureka, use env vars + K8s | Simplify infrastructure, modern service mesh | SRC-002, SRC-006 |
| TR-008 | Implement PWA capabilities | Android home screen install, offline browsing | SRC-003 |
| TR-009 | Async HTTP with HTTPX | FastAPI native, replace Feign clients | SRC-002 |
| TR-010 | Implement observability stack | OpenTelemetry tracing, metrics, logging | SRC-005, SRC-006 |

### Technology Stack Decisions

| Layer | Current | Target | Rationale |
|-------|---------|--------|-----------|
| Backend Framework | Spring Boot 2.6.3 | FastAPI | Org mandate, Python ecosystem for AI/ML |
| Frontend Framework | React (class components) | Next.js 14 (App Router) | SSR, modern React, better DX |
| Styling | Scattered CSS + Bootstrap | Tailwind CSS + shadcn/ui | Consistency, maintainability |
| Database | YCQL + YSQL hybrid | YSQL (PostgreSQL) only | Operational simplicity |
| ORM | JPA/Hibernate | SQLModel/SQLAlchemy | Python native |
| Authentication | Spring Security (sessions) | FastAPI + JWT | Stateless, cross-device |
| Service Discovery | Eureka | Env vars / K8s | Simplification |
| HTTP Client | Feign | HTTPX (async) | Async native |
| Caching | None | Redis | Performance, session state |
| Search | None | OpenSearch/Elasticsearch | Full-text search |

### Service Migration Plan

| Order | Service | Current | Target | Complexity | Owner |
|-------|---------|---------|--------|------------|-------|
| 1 | Products | Spring Boot + JPA + YCQL | FastAPI + SQLModel | Medium | Priya |
| 2 | Cart | Spring Boot + JPA (session-scoped) | FastAPI + SQLModel (stateless) | Low | Jordan |
| 3 | Login | Spring Security + Sessions | FastAPI + JWT | Medium | Jordan |
| 4 | Checkout | Spring Boot + CQL Templates | FastAPI + SQLAlchemy | High | Priya |
| 5 | API Gateway | Spring Cloud + Feign | FastAPI or lightweight proxy | Medium | Alex |
| 6 | Eureka | Spring Cloud Netflix | Remove entirely | Low | Alex |

### Integration Requirements

| System | Integration Type | Requirements |
|--------|------------------|--------------|
| Apple Pay | Payment API | Web Payments API integration |
| Google Pay | Payment API | Google Pay API for Web |
| YugabyteDB | Database | SQLAlchemy/SQLModel ORM, YSQL only |
| Redis | Cache | Session state, API caching |
| OpenSearch | Search API | Product search indexing |
| Email Service | Marketing | Newsletter, order confirmations |

---

## 7. User Experience Requirements

### 7.1 Design Principles

Extracted from stakeholder input (SRC-001, SRC-003, SRC-006):

1. **Warm & Distinctive** — "Like walking into a nice bookstore" - avoid generic corporate aesthetics
2. **Mobile-First** — Design for mobile, scale up to desktop
3. **Thumb-Zone Aware** — Key interactions in bottom 2/3 of screen; bottom navigation
4. **Performance is UX** — Speed is a feature; <3s load time is mandatory
5. **Satisfying Feedback** — Meaningful animations and microinteractions (Amazon/Target quality)
6. **Preserve Key Journeys** — Maintain browse → cart → checkout flow integrity
7. **Progressive Enhancement** — PWA capabilities for enhanced mobile experience

### 7.2 Specific UX Requirements

| ID | Requirement | Rationale | Priority |
|----|-------------|-----------|----------|
| UX-001 | Distinctive typography (not Inter/Roboto/Arial) | Brand differentiation, premium feel, bookish character | MUST |
| UX-002 | Bottom navigation bar on mobile | Thumb accessibility, follows Instagram/banking app patterns | MUST |
| UX-003 | Feed-style product browsing on mobile | Natural mobile scroll pattern, full-width cards | MUST |
| UX-004 | Preserved scroll position on back | Prevent frustrating UX, state management | SHOULD |
| UX-005 | Sticky filter bar on product lists | Easy access to refinement | SHOULD |
| UX-006 | Swipeable product images | Touch-native gallery | SHOULD |
| UX-007 | Social sharing for products | Gen Z engagement, virality | COULD |
| UX-008 | Single-column mobile checkout | Reduce friction, large form fields | MUST |
| UX-009 | Infinite scroll with pagination fallback | Product browsing flexibility | SHOULD |

### 7.3 Mobile-Specific Requirements

| Requirement | Current | Target |
|-------------|---------|--------|
| Touch targets | 24px | 44px minimum |
| Navigation | Top header only | Bottom nav + simplified header |
| Product grid | 4-column small tiles | Full-width feed cards |
| Checkout forms | Tiny fields, pinch-to-zoom | Large fields, no zoom needed |
| Page load | 6 seconds | <3 seconds |
| Payment | Card forms only | Apple Pay, Google Pay |

---

## 8. Business Requirements

| ID | Requirement | Business Driver | Source |
|----|-------------|-----------------|--------|
| BR-001 | Increase mobile conversion to 2%+ | Digital revenue growth (~3x mobile revenue) | SRC-003 |
| BR-002 | Capture Gen Z demographic | Customer base diversification, future growth | SRC-003 |
| BR-003 | Board presentation by Q2 | Executive visibility, continued investment | SRC-001 |
| BR-004 | Enable mobile ad campaigns | Marketing ROI (currently paused due to poor mobile UX) | SRC-003 |
| BR-005 | Align with unified tech stack | Organizational mandate, hiring efficiency, AI/ML enablement | SRC-002, SRC-006 |

### Business Rules

| Rule ID | Description | Conditions | Actions |
|---------|-------------|------------|---------|
| BR-R001 | Inventory check on checkout | Always before order creation | Reject if insufficient stock, show "out of stock" |
| BR-R002 | Cart association | On cart operations | Associate with authenticated user ID |
| BR-R003 | Order attribution | On order creation | Set user_id from JWT token, not hardcoded |
| BR-R004 | Price display | All product views | Show price, calculated subtotal in cart |
| BR-R005 | Tax calculation | Checkout | Currently $0.00 (future: calculate by region) |

---

## 9. Constraints & Assumptions

### Constraints

| ID | Constraint | Type | Impact |
|----|------------|------|--------|
| CON-001 | Python/FastAPI mandate from architecture governance Q1 | Technical | Full backend rewrite required |
| CON-002 | Board presentation Q2 2025 | Timeline | Phase 1 must be complete by May |
| CON-003 | No native mobile app budget | Business | Must achieve results with mobile web/PWA |
| CON-004 | Existing user password hashes must migrate | Technical | BCrypt compatibility required |
| CON-005 | Parallel deployment during migration | Operational | Both stacks running simultaneously (strangler fig) |
| CON-006 | 6,000+ existing products | Data | Must maintain catalog integrity |
| CON-007 | YugabyteDB as data layer | Technical | Migrate to YSQL only, eliminate YCQL |

### Assumptions

| ID | Assumption | Risk if Invalid | Validation Plan |
|----|------------|-----------------|-----------------|
| ASM-001 | PWA will be sufficient without native app | May need native app investment | Monitor metrics post-launch |
| ASM-002 | Team can learn FastAPI within timeline | Delays, quality issues | Training, pair programming |
| ASM-003 | Apple Pay/Google Pay will lift conversion 20-30% | ROI not achieved | A/B test, industry benchmarks |
| ASM-004 | Strangler fig migration won't cause disruptions | User-facing issues | Canary deployments, monitoring |
| ASM-005 | Mobile-first design improves desktop too | Desktop regression | Parallel testing both viewports |
| ASM-006 | AI/ML features will leverage Python ecosystem | Limited benefit from migration | Validate with AI team roadmap |

---

## 10. Conflicts & Resolutions

### Identified Conflicts

#### CONFLICT-001: Migration Timeline vs. Feature Requests
- **Sources:** SRC-001 vs SRC-002
- **Nature:** Stakeholders want visual refresh and mobile improvements by Q2, but technical team must migrate entire backend to Python per organizational mandate.
- **Option A:** Delay visual refresh until after migration
- **Option B:** Build visual refresh in old stack, then migrate
- **Option C:** Parallel effort - frontend team on Next.js, backend team migrates services
- **Recommendation:** Option C - decouple frontend/backend work via strangler fig pattern
- **Status:** RESOLVED
- **Resolution:** API contracts remain stable; teams work in parallel

#### CONFLICT-002: Security Fixes Priority
- **Sources:** SRC-001, SRC-002
- **Nature:** Security vulnerabilities are critical but less visible than visual improvements to executives
- **Recommendation:** Security fixes are non-negotiable foundation - include in Phase 1
- **Status:** RESOLVED
- **Resolution:** Sarah agreed security hardening is "tied for number one" priority

#### CONFLICT-003: Eureka vs. Simplification
- **Sources:** SRC-002, SRC-004
- **Nature:** Current architecture uses Eureka for service discovery; Python migration doesn't need it
- **Recommendation:** Drop Eureka, use environment variables + Kubernetes service mesh
- **Status:** RESOLVED
- **Resolution:** Alex confirmed this "makes the deployment story cleaner"

### Conflict Summary

| ID | Type | Severity | Status | Owner |
|----|------|----------|--------|-------|
| CONFLICT-001 | Timeline | MEDIUM | RESOLVED | Mike Chen |
| CONFLICT-002 | Priority | HIGH | RESOLVED | Sarah Mitchell |
| CONFLICT-003 | Architecture | LOW | RESOLVED | Alex Kim |

---

## 11. Phasing & Roadmap

### Modernization Framework

Per SRC-006, the modernization follows a closed-loop AI-augmented process:

```
Constitution (Principles & Constraints)
         │
         ▼
Human Input Repository (Requirements, Interviews, Decisions)
         │
         ▼
Legacy Extractor → Finished Legacy Spec
         │
         ▼
Process Engine (Spec Generation & Validation)
         │
         ▼
Future-State Spec → Human Review → Iterate → Build
```

### Phase Overview

| Phase | Scope | Target Date | Key Deliverables |
|-------|-------|-------------|------------------|
| **Phase 1** | Visual refresh, mobile-first, security fixes, PWA | May 2025 (Q2) | Next.js frontend, JWT auth, mobile optimization, Apple Pay/Google Pay, Products & Cart services migrated |
| **Phase 2** | Search, navigation, remaining migrations | Q3 2025 | Product search, Checkout & Login services migrated, enhanced category browsing |
| **Phase 3** | User features, engagement | Q4 2025 | Wishlists, order history, user profiles, email notifications, reviews |
| **Phase 4** | Operations, sunset legacy | Q1 2026 | Full Python migration complete, Eureka removed, admin dashboard, observability |

### Phase 1 Detail (Q2 2025)

**Frontend:**
- [ ] Next.js setup with App Router
- [ ] Tailwind CSS + shadcn/ui component library
- [ ] Mobile-first responsive design with bottom navigation
- [ ] Visual design system (warm, distinctive typography)
- [ ] Animations and microinteractions
- [ ] PWA manifest and service worker
- [ ] Performance optimization (<3s load)

**Backend:**
- [ ] Products service → FastAPI + SQLModel
- [ ] Cart service → FastAPI + SQLModel (stateless)
- [ ] JWT authentication implementation
- [ ] Fix hardcoded user IDs
- [ ] Parameterized queries

**Payments:**
- [ ] Apple Pay integration
- [ ] Google Pay integration

**Infrastructure:**
- [ ] Docker containers for new services
- [ ] Parallel deployment setup
- [ ] Basic monitoring

### Service Migration Order (Strangler Fig)

| Order | Service | Phase | Rationale |
|-------|---------|-------|-----------|
| 1 | Products | Phase 1 | Simplest, read-heavy, good learning exercise |
| 2 | Cart | Phase 1 | Simple CRUD, needs stateless rewrite anyway |
| 3 | Login | Phase 2 | JWT implementation, dependency for other fixes |
| 4 | Checkout | Phase 2 | Most complex, security critical |
| 5 | API Gateway | Phase 2 | Depends on downstream services |
| 6 | Eureka | Phase 4 | Remove after all services migrated |

---

## 12. Out of Scope

Items explicitly excluded from this requirements document:

| Item | Reason | Future Consideration |
|------|--------|---------------------|
| Native iOS/Android apps | Budget, PWA should suffice | Revisit if metrics don't improve |
| Live shopping / streaming | Not ready operationally | Phase 4+ |
| AI/ML personalization | Requires Python migration first | Phase 4+ |
| Admin dashboard | Not customer-facing | Phase 4 |
| Multi-language support (i18n) | Not requested | Future |
| Multi-currency | Not requested | Future |
| Subscription/recurring orders | Not in current scope | Future |
| Saved payment methods | PCI compliance complexity | Phase 3+ |
| Guest checkout | Auth integration priority | Phase 2 |
| Physical store integration | Out of scope | N/A |

---

## 13. Open Questions

| ID | Question | Owner | Due Date | Status |
|----|----------|-------|----------|--------|
| Q-001 | What is the budget for Apple Pay / Google Pay integration? | Sarah Mitchell | 2024-12-20 | OPEN |
| Q-002 | Are there brand guidelines for visual design? | Sarah Mitchell | 2024-12-15 | OPEN |
| Q-003 | OpenSearch vs. Elasticsearch licensing for search? | Alex Kim | 2024-12-20 | OPEN |
| Q-004 | API backward compatibility during migration? | Mike Chen | 2024-12-15 | OPEN |
| Q-005 | Analytics/tracking tools to integrate? | Marketing | 2024-12-20 | OPEN |
| Q-006 | Redis hosting - managed service or self-hosted? | Alex Kim | 2024-12-20 | OPEN |
| Q-007 | Email service provider for notifications? | Marketing | 2024-12-20 | OPEN |
| Q-008 | Load testing baseline - current capacity? | Mike Chen | 2024-12-20 | OPEN |

---

## 14. Glossary

| Term | Definition |
|------|------------|
| ASIN | Amazon Standard Identification Number - unique product identifier |
| PWA | Progressive Web App - web application with native-like capabilities |
| JWT | JSON Web Token - secure token for stateless authentication |
| Strangler Fig | Migration pattern where new system gradually replaces old |
| YCQL | Yugabyte Cloud Query Language (Cassandra-compatible) |
| YSQL | Yugabyte Structured Query Language (PostgreSQL-compatible) |
| FastAPI | Modern Python web framework for building APIs |
| SQLModel | Python library combining SQLAlchemy and Pydantic |
| shadcn/ui | React component library built on Radix UI |
| MoSCoW | Prioritization method: Must, Should, Could, Won't |
| Touch Target | Interactive UI element sized for finger/thumb tapping (44px min) |
| Thumb Zone | Area of mobile screen easily reachable by thumb (bottom 2/3) |
| SSR | Server-Side Rendering - generating HTML on server |
| OpenTelemetry | Observability framework for traces, metrics, logs |

---

## 15. Appendices

### A. Source Material Summaries

**SRC-001: Modernization Interview (Sarah Mitchell)**
Visual refresh needed ("looks dated"), security concerns about hardcoded users, wants distinctive brand identity ("like a bookstore"), board presentation Q2. Priorities: visual + security, mobile, navigation, nice-to-haves.

**SRC-002: Technical Migration Discussion**
Mandate to migrate to Python/FastAPI ("the org has decided Python is the future"). Frontend to Next.js/Tailwind. Critical security fixes: hardcoded IDs, SQL injection. Strangler fig approach. Timeline Q2-Q3.

**SRC-003: Mobile Expansion Interview (Sarah Mitchell)**
Alarming metrics: 31% mobile traffic (vs 65-70% industry), 0.8% mobile conversion, 78% cart abandonment. Mobile-first design priority. PWA over native app. Apple Pay/Google Pay critical. Gen Z capture.

**SRC-004: Architecture Diagram**
6 Spring Boot services documented: Eureka, Gateway, Products, Cart, Checkout, Login. Feign clients for inter-service communication. YCQL for products/orders, YSQL for cart/users.

**SRC-005: High-Level Features Document**
Comprehensive feature inventory: Product catalog ✅, Cart ✅, Checkout ⚠️, Auth ⚠️, Search ❌, Wishlists ❌, Payments ❌. Performance targets: ≤200ms P95, 10,000 concurrent users, 99.9% uptime.

**SRC-006: Modernization Plan**
Vision: "machine-augmented, human-directed modernization engine." Principles: evolution not revolution, API-first, traceability, modularity. Tech stack: FastAPI, React/Next.js, PostgreSQL, Redis, OpenSearch.

### B. Requirement Traceability Matrix

| Requirement ID | Source(s) | Related Requirements | Test Approach |
|----------------|-----------|---------------------|---------------|
| FR-001 | SRC-001, SRC-003 | UX-001, TR-006 | Visual design review, A/B testing |
| FR-002 | SRC-001 | FR-001, TR-006 | Animation audit, user testing |
| FR-003 | SRC-001, SRC-002, SRC-005 | TR-004, TR-005, NFR-006 | Auth flow E2E tests, security scan |
| FR-009 | SRC-003 | TR-005 | Payment integration tests |
| FR-010 | SRC-001, SRC-003 | UX-002, UX-008 | Checkout flow E2E, mobile testing |
| NFR-001 | SRC-003, SRC-005 | TR-008 | Lighthouse audit, WebPageTest |
| NFR-006-009 | SRC-002 | TR-005 | OWASP ZAP scan, penetration test |
| TR-001-010 | SRC-002, SRC-006 | All | Integration tests, smoke tests |

### C. Architecture Diagrams

See `docs/inputs/architecture.mmd` for detailed Mermaid diagram of current microservices architecture.

### D. Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2024-12-09 | 1.0 | Initial document generation | Requirements Generator |
| 2024-12-09 | 2.0 | Added architecture, features, modernization plan sources | Requirements Generator |

---

*Document generated from source analysis*  
*Review required before SDD specification generation*

---

## Next Steps

1. **Stakeholder Review** — Circulate to Sarah, Mike, Jennifer for validation
2. **Prioritization Workshop** — Finalize Phase 1 scope with trade-offs
3. **Design Kickoff** — Engage design team on visual identity exploration
4. **Technical Spikes** — FastAPI setup, Next.js POC, Apple Pay sandbox
5. **Constitution Document** — Formalize architectural principles for SDD generation
