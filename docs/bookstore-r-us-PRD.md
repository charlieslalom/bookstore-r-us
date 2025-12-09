# Bookstore-R-Us - Product Requirements Document

> **Version:** 1.0  
> **Status:** DRAFT  
> **Last Updated:** December 9, 2024  
> **Author:** Generated from Source Analysis

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2024-12-09 | Requirements Generator | Initial generation with user-resolved conflicts |

### Source Materials Analyzed

| Source ID | Type | Description | Date |
|-----------|------|-------------|------|
| SRC-001 | STAKEHOLDER_TRANSCRIPT | Modernization Interview - Sarah Mitchell, VP Digital Experience | 2024-12-09 |
| SRC-002 | STAKEHOLDER_TRANSCRIPT | Mobile Expansion Interview - Sarah Mitchell | 2024-12-12 |
| SRC-003 | TECHNICAL_DISCUSSION | Stack Migration Planning - Mike Chen, Priya Sharma, Jordan Brooks, Alex Kim | 2024-12-11 |
| SRC-004 | EXISTING_FUNCTIONALITY | High-Level Features Document | 2024-12-09 |
| SRC-005 | BUSINESS_DOCUMENT | Modernization Plan - Vision & Strategy | 2024-12 |
| SRC-006 | TECHNICAL_DISCUSSION | Architecture Diagram (Mermaid) | 2024-12 |

**Input Directory:** `docs/inputs/`

---

## 1. Executive Summary

Bookstore-R-Us is a microservices-based e-commerce platform serving ~6,000 products across 18 categories. The platform requires comprehensive modernization to address critical gaps: poor mobile experience (31% mobile traffic vs. 65-70% industry average), dated visual design, security vulnerabilities (hardcoded user IDs, SQL injection risks), and technical debt in the frontend codebase.

This initiative follows an **evolution, not revolution** approach using a strangler fig pattern to incrementally modernize the platform. The frontend will be rebuilt with Next.js and mobile-first design, while backend services migrate to Python/FastAPI over time. Security fixes and Apple Pay/Google Pay integration are hard requirements for Phase 1.

### Key Objectives

1. **Mobile-First Transformation** — Achieve 60%+ mobile traffic share and 2%+ mobile conversion (from 0.8%)
2. **Modern Visual Identity** — Distinctive, warm "bookstore" aesthetic with animations and microinteractions
3. **Security Hardening** — Fix hardcoded user IDs, implement JWT authentication, eliminate SQL injection
4. **Performance** — Page load ≤2 seconds for initial render
5. **Payment Friction Reduction** — Apple Pay and Google Pay in Phase 1 (hard requirement)
6. **Incremental Backend Migration** — Strangler fig pattern to Python/FastAPI, frontend-first priority

### Success Metrics

| Metric | Current State | Target State | Timeline |
|--------|---------------|--------------|----------|
| Mobile Traffic Share | 31% | 60%+ | Q3 2025 |
| Mobile Conversion Rate | 0.8% | 2-2.5% | Q3 2025 |
| Mobile Cart Abandonment | 78% | <50% | Q2 2025 |
| Page Load Time | 6 seconds | ≤2 seconds | Q2 2025 |
| API Response Time (P95) | Not measured | ≤200ms | Q2 2025 |
| Security Vulnerabilities | 5 critical | 0 critical | Q2 2025 |
| Uptime SLO | Not monitored | 99.9% | Q3 2025 |

---

## 2. Stakeholder Analysis

### Primary Stakeholders

| Stakeholder | Role | Key Concerns | Priority Requirements |
|-------------|------|--------------|----------------------|
| Sarah Mitchell | VP Digital Experience | Brand perception, mobile conversion, board presentation Q2, distinctive identity | FR-001, FR-002, FR-009, UX-001 |
| Jennifer | Executive Sponsor | Digital revenue growth, competitive positioning | BR-001, BR-002 |
| Mike Chen | Technical Lead | Migration execution, org mandate compliance, team capacity | TR-001, TR-002 |
| Priya Sharma | Senior Backend Developer | Checkout security, products service migration | TR-003, NFR-005 |
| Jordan Brooks | Full-Stack Developer | Cart/login migration, frontend modernization | TR-004, FR-003 |
| Alex Kim | DevOps Engineer | Infrastructure simplification, deployment | TR-005 |
| Marcus (IT Security) | Security | Hardcoded user vulnerability | NFR-005, NFR-006 |
| Marketing (Priya) | Marketing | Mobile ad campaign ROI (currently paused) | UX-002, BR-003 |

---

## 3. Current State Analysis

### Architecture Overview

| Service | Port | Database | Status |
|---------|------|----------|--------|
| Eureka Server | 8761 | - | ✅ Running (to be deprecated) |
| API Gateway | 8081 | - | ✅ Running |
| Products Service | 8082 | YCQL (Cassandra) | ✅ Running |
| Cart Service | 8083 | YSQL (PostgreSQL) | ⚠️ Session-scoped issues |
| Login Service | 8085 | YSQL (PostgreSQL) | ⚠️ Basic, no JWT |
| Checkout Service | 8086 | YCQL (Cassandra) | ⚠️ Security vulnerabilities |
| React UI | 8080 | - | ⚠️ Class components, scattered CSS |

### Existing Functionality

| Feature | Status | Gap |
|---------|--------|-----|
| Product Catalog (6,000+ SKUs) | ✅ Implemented | No search, no advanced filters |
| Category Navigation (18 categories) | ✅ Implemented | Text-only, needs visual cards |
| Product Recommendations | ✅ Implemented | Based on also_bought/viewed data |
| Shopping Cart | ✅ Implemented | Hardcoded user ID (u1001) |
| Checkout with Inventory | ✅ Core | SQL injection risk, hardcoded user_id=1 |
| User Authentication | ⚠️ Partial | Session-based, not integrated |
| Product Search | ❌ Missing | Critical gap |
| Wishlists | ❌ Missing | Not built |
| Apple Pay / Google Pay | ❌ Missing | Major mobile friction |
| Order History | ❌ Missing | Backend exists, no UI |

### Technical Debt

| ID | Issue | Severity |
|----|-------|----------|
| TD-001 | Hardcoded user_id "u1001" in cart | CRITICAL |
| TD-002 | `Order.setUser_id(1)` in checkout | CRITICAL |
| TD-003 | Raw CQL string concatenation (injection risk) | CRITICAL |
| TD-004 | Session-scoped beans break load balancing | HIGH |
| TD-005 | CSRF protection disabled | HIGH |
| TD-006 | React class components, deprecated lifecycle | MEDIUM |
| TD-007 | 40+ scattered CSS files | MEDIUM |
| TD-008 | 6-second page load on mobile | HIGH |

---

## 4. Functional Requirements

### 4.1 Visual Modernization

#### [FR-001] Modern Visual Design System
- **Priority:** MUST
- **Status:** [NEW]
- **Source(s):** SRC-001
- **Description:** Implement distinctive, warm visual design evoking "walking into a nice bookstore." Avoid generic corporate aesthetics. Use warm tones, cream colors, rich accents, and bookish serif typography.
- **Acceptance Criteria:**
  - [ ] Distinctive typography (not Roboto/Inter/Arial)
  - [ ] Warm color palette with brand personality
  - [ ] Design tokens via CSS variables
  - [ ] shadcn/ui component library with custom theming
  - [ ] Visually distinct from competitors
- **Notes:** Sarah: "I don't want it to look like every other website... if it could feel like walking into a nice bookstore"

#### [FR-002] Animations and Microinteractions
- **Priority:** MUST
- **Status:** [NEW]
- **Source(s):** SRC-001
- **Description:** Add polish through page transitions, hover effects, and satisfying add-to-cart feedback (Amazon/Target quality).
- **Acceptance Criteria:**
  - [ ] Page transition animations
  - [ ] Product card hover effects
  - [ ] Add-to-cart animation with feedback
  - [ ] Loading skeleton states
  - [ ] Interactive hero section (not static PNG)

### 4.2 Authentication & Security

#### [FR-003] JWT User Authentication
- **Priority:** MUST
- **Status:** [MIGRATE] [RESOLVED]
- **Source(s):** SRC-001, SRC-003
- **Description:** Replace session-based auth with JWT. Fix hardcoded user IDs. User identity must flow through all services.
- **Acceptance Criteria:**
  - [ ] JWT authentication with token refresh
  - [ ] Cart uses actual authenticated user ID
  - [ ] Orders created with real user ID from token
  - [ ] Cross-device session continuity
  - [ ] BCrypt password compatibility (existing users can log in)
- **Conflict Resolution:** User chose hybrid migration approach; JWT auth is Phase 1 priority

#### [FR-004] Wishlist / Save for Later
- **Priority:** SHOULD
- **Status:** [NEW]
- **Source(s):** SRC-002, SRC-004
- **Description:** Allow users to save products for later. Critical for Gen Z cross-device behavior.
- **Acceptance Criteria:**
  - [ ] Save/unsave products
  - [ ] Persist across sessions and devices
  - [ ] Move from wishlist to cart
- **Dependencies:** FR-003

#### [FR-005] Order History
- **Priority:** SHOULD
- **Status:** [NEW]
- **Source(s):** SRC-001, SRC-004
- **Description:** User-facing order history view. Backend exists but no UI.
- **Acceptance Criteria:**
  - [ ] List of past orders
  - [ ] Order detail view
- **Dependencies:** FR-003

### 4.3 Product Discovery

#### [FR-006] Product Search
- **Priority:** SHOULD
- **Status:** [NEW]
- **Source(s):** SRC-001, SRC-004
- **Description:** Full-text search for 6,000+ product catalog.
- **Acceptance Criteria:**
  - [ ] Search bar in navigation
  - [ ] Search across title, description, brand
  - [ ] Autocomplete suggestions
  - [ ] Results with relevance ranking
- **Dependencies:** Backend search service (Elasticsearch/OpenSearch)
- **Notes:** Phase 2 feature

#### [FR-007] Visual Category Navigation
- **Priority:** MUST
- **Status:** [ENHANCE]
- **Source(s):** SRC-001
- **Description:** Replace text-only navigation with visual category cards with imagery.
- **Acceptance Criteria:**
  - [ ] Category cards with images on homepage
  - [ ] Touch-friendly navigation
  - [ ] Mobile drawer menu
  - [ ] Bestseller highlights per category

#### [FR-008] Advanced Filtering
- **Priority:** SHOULD
- **Status:** [NEW]
- **Source(s):** SRC-004
- **Description:** Filter products by price, brand, rating.
- **Acceptance Criteria:**
  - [ ] Price range filter
  - [ ] Brand filter
  - [ ] Rating filter
  - [ ] Sticky filter bar on mobile

### 4.4 Checkout & Payments

#### [FR-009] Apple Pay & Google Pay Integration
- **Priority:** MUST
- **Status:** [NEW] [RESOLVED]
- **Source(s):** SRC-002
- **Description:** Integrate Apple Pay and Google Pay to reduce mobile checkout friction. 20-30% improvement in checkout completion expected.
- **Acceptance Criteria:**
  - [ ] Apple Pay on iOS Safari
  - [ ] Google Pay on Android
  - [ ] Fallback to standard checkout
  - [ ] Proper error handling
- **Conflict Resolution:** User confirmed this is a **hard Phase 1 requirement** - no slip to Phase 2

#### [FR-010] Mobile Checkout Redesign
- **Priority:** MUST
- **Status:** [ENHANCE]
- **Source(s):** SRC-001, SRC-002
- **Description:** Single-column mobile checkout with large form fields, progress indicators, autofill support.
- **Acceptance Criteria:**
  - [ ] Progress indicator
  - [ ] Single-column layout
  - [ ] 44px+ touch targets
  - [ ] Autofill support
  - [ ] Visual order confirmation

---

## 5. Non-Functional Requirements

### 5.1 Performance

| ID | Requirement | Target | Priority |
|----|-------------|--------|----------|
| NFR-001 | Page load time | ≤2 seconds | MUST |
| NFR-002 | API Response Time (P95) | ≤200ms | MUST |
| NFR-003 | First Contentful Paint | <1.5s | SHOULD |
| NFR-004 | JS bundle size | <200KB initial | SHOULD |

**Conflict Resolution:** User chose **≤2 seconds** (Option B - more aggressive target from SRC-004)

### 5.2 Security

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-005 | Eliminate SQL/CQL injection | MUST |
| NFR-006 | Parameterized queries everywhere | MUST |
| NFR-007 | JWT authentication | MUST |
| NFR-008 | CSRF protection | MUST |
| NFR-009 | Rate limiting on auth | SHOULD |
| NFR-010 | HTTPS/TLS everywhere | MUST |

### 5.3 Scalability & Reliability

| ID | Requirement | Target | Priority |
|----|-------------|--------|----------|
| NFR-011 | Concurrent users | 10,000+ | SHOULD |
| NFR-012 | Uptime SLO | 99.9% | SHOULD |
| NFR-013 | Stateless services | Database/JWT only | MUST |
| NFR-014 | Zero-downtime deployments | Blue-green | SHOULD |

### 5.4 Accessibility

| ID | Requirement | Target | Priority |
|----|-------------|--------|----------|
| NFR-015 | Touch targets | 44px minimum | MUST |
| NFR-016 | WCAG compliance | AA | SHOULD |
| NFR-017 | Keyboard navigation | Full support | SHOULD |

---

## 6. Technical Requirements

| ID | Requirement | Rationale | Source |
|----|-------------|-----------|--------|
| TR-001 | Migrate frontend to Next.js | Modern React, SSR, hooks | SRC-003 |
| TR-002 | Implement Tailwind + shadcn/ui | Replace scattered CSS | SRC-003 |
| TR-003 | Incremental backend migration to FastAPI | Org mandate, strangler fig | SRC-003, SRC-005 |
| TR-004 | Stateless cart service | Fix session-scoped issues | SRC-003 |
| TR-005 | Remove Eureka, use env vars + K8s | Simplify infrastructure | SRC-003 |
| TR-006 | Unify database on YSQL | Eliminate YCQL complexity | SRC-003 |
| TR-007 | PWA capabilities | Android install, offline | SRC-002 |
| TR-008 | Async HTTP with HTTPX | Replace Feign clients | SRC-003 |

### Technology Stack

| Layer | Current | Target |
|-------|---------|--------|
| Frontend | React (class components) | Next.js 14 (App Router, hooks) |
| Styling | Bootstrap + scattered CSS | Tailwind CSS + shadcn/ui |
| Backend | Spring Boot | FastAPI (incremental migration) |
| Auth | Spring Security (sessions) | FastAPI + JWT |
| Database | YCQL + YSQL | YSQL only (PostgreSQL) |
| Service Discovery | Eureka | Env vars / K8s service mesh |

### Migration Order (Strangler Fig)

| Order | Service | Phase | Owner |
|-------|---------|-------|-------|
| 1 | Frontend (Next.js) | Phase 1 | Jordan |
| 2 | Products Service | Phase 1 | Priya |
| 3 | Cart Service | Phase 1 | Jordan |
| 4 | Login Service | Phase 2 | Jordan |
| 5 | Checkout Service | Phase 2 | Priya |
| 6 | API Gateway | Phase 2 | Alex |

**Conflict Resolution:** User chose **Option C - Hybrid approach** with strangler fig pattern, prioritizing frontend first

---

## 7. User Experience Requirements

### Design Principles

1. **Warm & Distinctive** — "Like walking into a nice bookstore"
2. **Mobile-First** — Design for mobile, scale up to desktop
3. **Thumb-Zone Aware** — Key actions in bottom navigation
4. **Performance is UX** — ≤2 second loads are mandatory
5. **Satisfying Feedback** — Amazon/Target quality interactions

### Specific UX Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| UX-001 | Distinctive typography (no generic fonts) | MUST |
| UX-002 | Bottom navigation bar on mobile | MUST |
| UX-003 | Feed-style product browsing (vertical scroll) | MUST |
| UX-004 | Preserved scroll position on back | SHOULD |
| UX-005 | Sticky filter bar | SHOULD |
| UX-006 | Swipeable product images | SHOULD |

---

## 8. Business Requirements

| ID | Requirement | Driver | Source |
|----|-------------|--------|--------|
| BR-001 | Mobile conversion 0.8% → 2%+ | Revenue growth (~3x) | SRC-002 |
| BR-002 | Capture Gen Z demographic | Customer diversification | SRC-002 |
| BR-003 | Enable mobile ad campaigns | Marketing ROI (currently paused) | SRC-002 |
| BR-004 | Board presentation Q2 2025 | Executive visibility | SRC-001 |

---

## 9. Constraints & Assumptions

### Constraints

| ID | Constraint | Impact |
|----|------------|--------|
| CON-001 | Python/FastAPI organizational mandate | Backend migration required |
| CON-002 | Board presentation Q2 2025 | Phase 1 deadline |
| CON-003 | No native app budget | PWA only |
| CON-004 | BCrypt password compatibility | Existing users must not reset |

### Assumptions

| ID | Assumption | Risk if Invalid |
|----|------------|-----------------|
| ASM-001 | PWA sufficient without native app | May need native investment |
| ASM-002 | Apple Pay/Google Pay lifts conversion 20-30% | ROI not achieved |
| ASM-003 | Strangler fig won't cause disruptions | Service failures |

---

## 10. Resolved Conflicts

**All conflicts were resolved with user input before PRD generation.**

| ID | Conflict | User Decision | Rationale |
|----|----------|---------------|-----------|
| CONFLICT-001 | Backend: Keep Java vs. Full Python migration | **C) Hybrid - Strangler fig pattern, frontend-first** | Balance org mandate with practical execution; prioritize customer-facing changes |
| CONFLICT-002 | Page load target: 3s vs 2s | **B) ≤2 seconds** | More aggressive target aligns with Gen Z expectations |
| CONFLICT-003 | Apple/Google Pay: Phase 1 vs Phase 2 | **A) MUST be Phase 1** | Conversion lift too significant to delay |

---

## 11. Phasing & Roadmap

### Phase 1 (Q2 2025 - Board Presentation)

**Frontend:**
- [ ] Next.js with App Router
- [ ] Tailwind + shadcn/ui
- [ ] Mobile-first design with bottom navigation
- [ ] Warm, distinctive visual identity
- [ ] Animations and microinteractions
- [ ] PWA manifest + service worker
- [ ] Performance ≤2 seconds

**Security:**
- [ ] JWT authentication
- [ ] Fix hardcoded user IDs
- [ ] Parameterized queries

**Payments:**
- [ ] Apple Pay integration (HARD REQUIREMENT)
- [ ] Google Pay integration (HARD REQUIREMENT)

**Backend Migration:**
- [ ] Products service → FastAPI
- [ ] Cart service → FastAPI (stateless)

### Phase 2 (Q3 2025)

- [ ] Product search (Elasticsearch)
- [ ] Login service → FastAPI
- [ ] Checkout service → FastAPI
- [ ] Order history UI
- [ ] Wishlists
- [ ] Advanced filtering

### Phase 3 (Q4 2025)

- [ ] API Gateway migration
- [ ] Remove Eureka
- [ ] User profiles
- [ ] Email notifications
- [ ] Full observability

---

## 12. Out of Scope

| Item | Reason | Future |
|------|--------|--------|
| Native iOS/Android apps | No budget, PWA first | Revisit if metrics don't improve |
| Live shopping | Not ready | Phase 4+ |
| AI personalization | Needs Python migration | Phase 4+ |
| Multi-language | Not requested | Future |
| Saved payment methods | PCI complexity | Phase 3+ |

---

## 13. Open Questions

| ID | Question | Owner | Status |
|----|----------|-------|--------|
| Q-001 | Apple Pay/Google Pay budget approval? | Sarah | OPEN |
| Q-002 | Brand guidelines for visual design? | Sarah | OPEN |
| Q-003 | Search service: OpenSearch vs Elasticsearch? | Alex | OPEN |
| Q-004 | Redis hosting approach? | Alex | OPEN |

---

## 14. Glossary

| Term | Definition |
|------|------------|
| ASIN | Product identifier |
| PWA | Progressive Web App |
| JWT | JSON Web Token |
| Strangler Fig | Incremental migration pattern |
| YCQL | Yugabyte Cassandra Query Language |
| YSQL | Yugabyte SQL (PostgreSQL-compatible) |
| shadcn/ui | React component library |

---

## 15. Appendices

### A. Source Summaries

**SRC-001 (Modernization Interview):** Visual refresh needed, security concerns, distinctive "bookstore" identity wanted, board presentation Q2.

**SRC-002 (Mobile Interview):** 31% mobile traffic (vs 65-70% industry), 0.8% conversion, 78% cart abandonment. Mobile-first, PWA, Apple Pay/Google Pay critical.

**SRC-003 (Tech Discussion):** Python/FastAPI mandate, Next.js/Tailwind for frontend, strangler fig migration, security fixes critical.

**SRC-004 (Features Doc):** Current implementation status, 6,000 SKUs, 18 categories, gaps in search/payments/wishlists.

**SRC-005 (Modernization Plan):** Evolution not revolution, API-first, traceability, incremental approach.

**SRC-006 (Architecture):** 6 Spring Boot services, Feign clients, YCQL/YSQL hybrid database.

### B. Traceability Matrix

| Requirement | Source(s) |
|-------------|-----------|
| FR-001 Visual Design | SRC-001 |
| FR-003 JWT Auth | SRC-001, SRC-003 |
| FR-009 Apple/Google Pay | SRC-002 |
| NFR-001 ≤2s Load | SRC-004 (user decision) |
| TR-003 FastAPI Migration | SRC-003, SRC-005 |

---

*Document generated from `docs/inputs/` source analysis*  
*All conflicts resolved with user input*  
*Ready for stakeholder review*

