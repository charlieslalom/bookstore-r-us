# Business Requirements & Features - Bookstore E-Commerce Platform

## **1. Executive Summary**

This document establishes the **business requirements, functional capabilities, and technical implementation** for a **cloud-native, scalable, resilient microservices-based e-commerce platform** (Yugastore/Bookstore-R-Us).

The platform is designed as a **technology-agnostic**, forward-looking system that supports **AI-assisted, spec-driven development workflows**, ensuring durable engineering discipline and predictable delivery.

**Last Updated:** 2025-12-09

---

## **2. Business Requirements**

### **2.1 Purpose and Scope**

The system supports:
- Online bookstore shopping experience (expandable to multi-category retail)
- Product catalog and search capabilities
- Cart and checkout workflows
- Order lifecycle & fulfillment
- Identity, authentication & authorization
- Payment routing (future/optional)
- Inventory management and data storage
- API gateway & routing
- Observability, resilience, and performance monitoring

### **2.2 Target Performance Objectives**

#### **Performance**
- API response time target: ≤ 200 ms at P95
- Catalog & cart endpoints must support burst traffic
- Page load time: ≤ 2 seconds for initial render

#### **Scalability**
- Horizontal scaling for compute and storage
- Services must avoid single points of failure
- Support for concurrent users: 10,000+ simultaneous sessions

#### **Reliability & Availability**
- SLO: 99.9% uptime
- Redundancy for critical services
- Graceful degradation & fallback strategies
- Zero-downtime deployments

#### **Resilience**
- Circuit breakers, retries, backoff strategies
- Rate limiting and API quota enforcement
- Fault isolation between microservices

#### **Accessibility (UI)**
- WCAG AA compliance target
- Keyboard navigation support
- Alternative text for images
- Semantic HTML structure

#### **Internationalization (Future)**
- Multi-language content support
- Configurable currency and locale formats
- Timezone-aware order processing

---

## **3. Functional Features - Current Implementation**

### **3.1 Product Catalog**

**Business Requirement:** Browse/search products with rich metadata, pricing, and availability information. Support category filtering and pagination for optimal user experience.

**Implementation Status:** ✅ **Fully Implemented**

#### Features:
- **Product Listing**
  - Browse all products with pagination (12 items per page)
  - Navigate between pages (Previous/Next)
  - View product thumbnails, titles, prices, and star ratings
  - Quick "Add to Cart" button on each product card

- **Category Navigation**
  - Primary categories in navigation bar: Books, Music, Beauty, Electronics
  - Extended categories (18 total): Kitchen & Dining, Toys & Games, Pet Supplies, Grocery & Gourmet Food, Video Games, Movies & TV, Arts, Crafts & Sewing, Home & Kitchen, Patio, Lawn & Garden, Health & Personal Care, Cell Phones & Accessories, Industrial & Scientific, Sports & Outdoors

- **Product Details Page**
  - Full product image display
  - Product title and description
  - Price display
  - Star rating visualization (5-star system with half-stars)
  - Number of reviews and total stars
  - Brand information
  - "Add to Cart" button

- **Product Recommendations**
  - "Also Bought" section showing related products
  - Based on `also_bought`, `also_viewed`, `bought_together`, and `buy_after_viewing` data
  - Cross-sell and upsell opportunities

- **Product Sorting**
  - By highest rating (`num_stars`)
  - By most reviews (`num_reviews`)
  - By best selling (`num_buys`)
  - By most pageviews (`num_views`)

**Gap Analysis:**
- ⚠️ Product search functionality not implemented (no search bar)
- ⚠️ Advanced filtering (price range, brand, etc.) not implemented

---

### **3.2 Shopping Cart**

**Business Requirement:** Add/remove/update items with stateless operations backed by durable storage. Persist carts for authenticated users.

**Implementation Status:** ✅ **Fully Implemented**

#### Features:
- **Cart Management**
  - Add items to cart from product listings or detail pages
  - Remove items from cart
  - View cart contents with product images and details
  - Real-time cart count display in navigation bar
  - Visual feedback on cart errors

- **Cart Display**
  - Product image, title, and link to product page
  - Individual product price
  - Quantity of each item
  - Running subtotal calculation
  - Tax display (currently $0.00)

- **Cart Persistence**
  - Cart data persisted per user session
  - Cart automatically fetched on page load
  - Cart state maintained during navigation
  - Backed by YugabyteDB YCQL storage

**Performance:** Cart operations are stateless and horizontally scalable.

---

### **3.3 Checkout & Order Processing**

**Business Requirement:** Tax/shipping calculation, order summary, payment flow (future), order creation & order tracking lifecycle.

**Implementation Status:** ✅ **Core Features Implemented** | ⚠️ **Payment Integration Pending**

#### Features:
- **Checkout Process**
  - Single-click checkout from cart page
  - Inventory validation before purchase
  - Out-of-stock detection with appropriate messaging
  - Transactional order creation (using Cassandra transactions)

- **Order Confirmation**
  - Order number generation (UUID-based)
  - Order details summary (products, quantities, total)
  - "Thank you" confirmation message
  - Order number displayed as `#kmp-{orderNumber}`

- **Inventory Management**
  - Real-time inventory quantity tracking
  - Automatic inventory deduction on successful checkout
  - Validation against available stock
  - Transaction-safe operations

- **Order Records**
  - Order ID (UUID)
  - User ID association
  - Order details (items purchased)
  - Order timestamp
  - Order total amount

**Gap Analysis:**
- ⚠️ Payment processing not integrated
- ⚠️ Shipping cost calculation not implemented
- ⚠️ Order tracking/history view not available to users
- ⚠️ Order status updates not implemented

---

### **3.4 User Authentication**

**Business Requirement:** Support login/signup with token-based session management. Integrate with cloud identity provider (Cognito/Okta/etc.).

**Implementation Status:** ✅ **Basic Implementation** | ⚠️ **Cloud Identity Integration Pending**

#### Features:
- **User Registration**
  - Registration form with validation
  - Username and password fields
  - Password confirmation
  - Redirect to login after successful registration

- **User Login**
  - Username/password authentication
  - Error messaging for invalid credentials
  - Logout functionality with confirmation message
  - Session-based authentication

- **User Management**
  - User role support (role-based access)
  - User validation (via UserValidator)
  - Secure password handling
  - Data stored in YugabyteDB YSQL (PostgreSQL-compatible)

**Gap Analysis:**
- ⚠️ Cloud identity provider integration not implemented
- ⚠️ OAuth/SSO support not available
- ⚠️ Multi-factor authentication not implemented
- ⚠️ Password reset functionality not visible

---

### **3.5 Homepage & Marketing**

**Business Requirement:** Engaging landing page with promotional content to drive conversions and category exploration.

**Implementation Status:** ✅ **Implemented**

#### Features:
- **Hero Section**
  - Full-width promotional banner/image
  - Brand showcase area

- **Bestseller Highlights**
  - Featured products from each major category (4 items each):
    - Bestsellers in Books
    - Bestsellers in Music
    - Bestsellers in Beauty
    - Bestsellers in Electronics
  - Quick links to category pages

- **Newsletter Subscription**
  - Email subscription form
  - Marketing messaging ("Let's keep the conversation going")
  - Call-to-action for newsletter signup

**Gap Analysis:**
- ⚠️ Newsletter backend integration not implemented
- ⚠️ Email marketing automation not connected

---

### **3.6 Navigation & User Interface**

**Business Requirement:** Responsive, accessible, and intuitive user interface adhering to modern web standards.

**Implementation Status:** ✅ **Implemented**

#### Features:
- **Navigation Bar**
  - Logo with link to homepage
  - Category links with icons (Books, Music, Beauty, Electronics)
  - Shopping cart icon with item count badge
  - Scroll-responsive styling (transparent to solid)
  - Active state highlighting for current category

- **Footer**
  - Logo display
  - Brand attribution (YugaByte DB)
  - Copyright notice
  - Extended category links (18 categories)
  - External link to yugabyte.com

- **Responsive Design**
  - Mobile-friendly layouts (Bootstrap grid)
  - Adaptive navigation
  - Responsive product grids (1-4 columns based on viewport)
  - Touch-friendly interactions

**Accessibility Status:** Partial compliance with WCAG AA (needs audit)

---

### **3.7 System Management APIs**

**Business Requirement:** Health checks, service discovery, and operational endpoints for monitoring and management.

**Implementation Status:** ✅ **Implemented**

#### Features:
- Service discovery via Eureka Server (port 8761)
- Health check endpoints on all microservices
- API Gateway routing and aggregation (port 8081)
- Operational observability hooks

---

## **4. Technical Architecture**

### **4.1 Microservices Architecture**

Backend services supporting the features above:

| Service | Port | Responsibility | Technology |
|---------|------|----------------|------------|
| Eureka Server | 8761 | Service discovery and registration | Spring Cloud Netflix |
| API Gateway | 8081 | Request routing and API aggregation | Spring Cloud Gateway |
| Products | 8082 | Product catalog and metadata | Spring Boot |
| Cart | 8083 | Shopping cart operations | Spring Boot |
| Login | 8085 | User authentication | Spring Boot |
| Checkout | 8086 | Order processing and inventory | Spring Boot |
| React UI | 8080 | Frontend web application | React + Node.js |

**Architecture Principles:**
- Stateless services for horizontal scalability
- Domain-driven design with bounded contexts
- Event-driven communication (future: message queue integration)
- API-first design with OpenAPI specifications

---

### **4.2 Data Storage Layer**

Database layer powered by **YugabyteDB** (distributed SQL database).

#### **YCQL (Cassandra-compatible API)**
- Products table (metadata, images, pricing)
- Product inventory tracking
- Product rankings by category
- Orders table
- Shopping cart storage

#### **YSQL (PostgreSQL-compatible API)**
- User authentication data
- Role-based permissions
- Transactional order records

**Benefits:**
- Distributed, fault-tolerant architecture
- Multi-region replication capabilities
- Strong consistency with horizontal scalability
- PostgreSQL and Cassandra compatibility

---

## **5. Implementation Status Matrix**

| Functional Area | Business Requirement | Implementation Status | Gaps |
|----------------|----------------------|-----------------------|------|
| **Product Browsing** | Browse/search products | ✅ Fully Implemented | Search bar not implemented |
| **Category Filtering** | Category navigation | ✅ Fully Implemented | Advanced filters missing |
| **Product Details** | Rich product pages | ✅ Fully Implemented | - |
| **Shopping Cart** | Persistent cart | ✅ Fully Implemented | - |
| **Checkout** | Order creation | ✅ Core Implemented | Payment integration pending |
| **Inventory** | Stock management | ✅ Fully Implemented | - |
| **User Authentication** | Login/signup | ✅ Basic Implemented | Cloud identity provider integration |
| **Order Tracking** | Order lifecycle | ⚠️ Backend Only | No user-facing order history view |
| **Product Reviews** | Customer reviews | ⚠️ Display Only | Cannot write reviews |
| **Recommendations** | Cross-sell/upsell | ✅ Fully Implemented | - |
| **Payment Processing** | Payment flow | ❌ Not Implemented | Payment gateway needed |
| **Wishlists** | Save for later | ❌ Not Implemented | Feature not built |
| **Newsletter** | Email marketing | ⚠️ UI Only | Backend integration pending |
| **Product Search** | Full-text search | ❌ Not Implemented | Search functionality needed |
| **Service Discovery** | Health/monitoring | ✅ Fully Implemented | - |
| **API Gateway** | Request routing | ✅ Fully Implemented | - |

**Legend:**
- ✅ Fully Implemented
- ⚠️ Partially Implemented
- ❌ Not Implemented

---

## **6. Modernization & Enhancement Roadmap**

### **6.1 Critical Gaps (High Priority)**
1. **Payment Integration** - Payment gateway (Stripe, PayPal, etc.)
2. **Product Search** - Full-text search with Elasticsearch or similar
3. **Order History** - User-facing order tracking and history
4. **Cloud Identity Provider** - OAuth/SSO integration (Cognito, Auth0, Okta)

### **6.2 Feature Enhancements (Medium Priority)**
1. **Product Review Writing** - Allow users to submit reviews
2. **Wishlists** - Save items for later
3. **Advanced Filtering** - Price range, brand, rating filters
4. **Email Notifications** - Order confirmations, shipping updates
5. **Newsletter Backend** - Email marketing integration

### **6.3 Infrastructure & Operations (Ongoing)**
1. **Observability** - Distributed tracing, metrics, logging (OpenTelemetry)
2. **Security Hardening** - OWASP compliance, security scanning
3. **Performance Optimization** - Caching strategy, CDN integration
4. **Accessibility Audit** - WCAG AA compliance verification
5. **Load Testing** - Performance benchmarking and capacity planning

---

## **7. Compliance & Quality Standards**

### **7.1 Non-Functional Requirements Tracking**

| Requirement | Target | Current Status | Notes |
|-------------|--------|----------------|-------|
| API Response Time (P95) | ≤ 200ms | To be measured | Needs performance testing |
| Uptime SLO | 99.9% | Not monitored | Requires monitoring setup |
| Concurrent Users | 10,000+ | Not tested | Needs load testing |
| WCAG Compliance | AA | Partial | Accessibility audit needed |
| Mobile Responsiveness | 100% | ✅ Implemented | Bootstrap responsive grid |

### **7.2 Security Requirements**
- HTTPS/TLS encryption for all communications
- Secure password storage (hashing + salting)
- SQL injection prevention (parameterized queries)
- XSS protection (React auto-escaping)
- CSRF protection (token-based)
- Rate limiting on API endpoints

---

## **8. Technology Stack Summary**

**Frontend:**
- React (UI framework)
- Bootstrap (responsive design)
- JavaScript/ES6+

**Backend:**
- Spring Boot (microservices framework)
- Spring Cloud (Netflix stack: Eureka, Gateway)
- Java

**Data Layer:**
- YugabyteDB (distributed SQL)
  - YCQL (Cassandra-compatible)
  - YSQL (PostgreSQL-compatible)

**Infrastructure:**
- Docker (containerization)
- Cloud-ready (deployable to AWS, GCP, Azure)

---

## **9. Business Rules Catalog**

### **9.1 Overview**

This section catalogs all identified business rules extracted from system behavior, including formal API contracts, code validation logic, database constraints, error handling patterns, and inferred business policies. Each rule is classified by severity and traced to its implementation points.

**Rule Severity Classification:**
- **CORE** - Critical business requirement that must not be violated
- **SAFETY** - Prevents data corruption or invalid system states
- **UX** - User experience rule that improves usability
- **POLICY** - Business policy or operational constraint

---

### **9.2 User Authentication & Registration Rules**

#### **BR-AUTH-001: Username Length Constraint**
- **Description:** Username must be between 6 and 32 characters inclusive
- **Severity:** CORE
- **Triggering Conditions:** User registration or username update
- **Inputs Required:** username (String)
- **Validation Logic:** `username.length() >= 6 && username.length() <= 32`
- **Error Message:** "Size.userForm.username"
- **Dependencies:** 
  - Service: login-microservice
  - Component: UserValidator
  - Database: users table (YSQL)
- **Implementation:** [UserValidator.java](login-microservice/src/main/java/com/yugabyte/app/yugastore/validator/UserValidator.java#L23-L25)
- **Example Scenario:** User attempts to register with username "user" → rejected (too short)

#### **BR-AUTH-002: Password Length Constraint**
- **Description:** Password must be between 8 and 32 characters inclusive
- **Severity:** CORE
- **Triggering Conditions:** User registration or password change
- **Inputs Required:** password (String)
- **Validation Logic:** `password.length() >= 8 && password.length() <= 32`
- **Error Message:** "Size.userForm.password"
- **Dependencies:** 
  - Service: login-microservice
  - Component: UserValidator
  - Database: users table (YSQL)
- **Implementation:** [UserValidator.java](login-microservice/src/main/java/com/yugabyte/app/yugastore/validator/UserValidator.java#L29-L31)
- **Example Scenario:** User sets password "pass" → rejected (too short, minimum 8 chars)

#### **BR-AUTH-003: Username Uniqueness Constraint**
- **Description:** Each username must be unique across the system; duplicate usernames are not allowed
- **Severity:** CORE
- **Triggering Conditions:** User registration
- **Inputs Required:** username (String)
- **Validation Logic:** `userService.findByUsername(username) == null`
- **Error Message:** "Duplicate.userForm.username"
- **Dependencies:** 
  - Service: login-microservice
  - Component: UserValidator, UserService
  - Database: users table (YSQL, unique constraint expected)
- **Implementation:** [UserValidator.java](login-microservice/src/main/java/com/yugabyte/app/yugastore/validator/UserValidator.java#L27-L29)
- **Example Scenario:** User tries to register with existing username "johndoe" → rejected

#### **BR-AUTH-004: Password Confirmation Match**
- **Description:** Password and password confirmation fields must match exactly during registration
- **Severity:** UX
- **Triggering Conditions:** User registration
- **Inputs Required:** password (String), passwordConfirm (String)
- **Validation Logic:** `passwordConfirm.equals(password)`
- **Error Message:** "Diff.userForm.passwordConfirm"
- **Dependencies:** 
  - Service: login-microservice
  - Component: UserValidator
- **Implementation:** [UserValidator.java](login-microservice/src/main/java/com/yugabyte/app/yugastore/validator/UserValidator.java#L33-L35)
- **Example Scenario:** User enters password "SecurePass123" and confirmation "SecurePass124" → rejected

#### **BR-AUTH-005: Required Field Validation**
- **Description:** Username and password fields cannot be empty or whitespace-only
- **Severity:** CORE
- **Triggering Conditions:** User registration or login
- **Inputs Required:** username (String), password (String)
- **Validation Logic:** `ValidationUtils.rejectIfEmptyOrWhitespace()`
- **Error Message:** "NotEmpty"
- **Dependencies:** 
  - Service: login-microservice
  - Component: UserValidator
- **Implementation:** [UserValidator.java](login-microservice/src/main/java/com/yugabyte/app/yugastore/validator/UserValidator.java#L22,L28)
- **Example Scenario:** User submits registration form with blank username → rejected

---

### **9.3 Shopping Cart Management Rules**

#### **BR-CART-001: Default Quantity on Add**
- **Description:** When a product is first added to the cart, quantity defaults to 1
- **Severity:** POLICY
- **Triggering Conditions:** User adds a product not currently in their cart
- **Inputs Required:** userId (String), asin (String)
- **Outputs:** ShoppingCart entity created with quantity=1
- **Dependencies:** 
  - Service: cart-microservice
  - Component: ShoppingCartImpl
  - Database: shopping_cart table (YSQL)
  - Constant: DEFAULT_QUANTITY = 1
- **Implementation:** [ShoppingCartImpl.java](cart-microservice/src/main/java/com/yugabyte/app/yugastore/cart/service/ShoppingCartImpl.java#L24,L47)
- **Example Scenario:** User clicks "Add to Cart" on product B00BKQT2OI → cart entry created with quantity=1

#### **BR-CART-002: Quantity Increment on Duplicate Add**
- **Description:** When a product already in the cart is added again, increment quantity by 1 instead of creating duplicate entry
- **Severity:** CORE
- **Triggering Conditions:** User adds a product that already exists in their cart
- **Inputs Required:** userId (String), asin (String)
- **Validation Logic:** `shoppingCartRepository.findById(shoppingCartKeyStr).isPresent()`
- **Outputs:** Existing cart entry quantity incremented
- **Dependencies:** 
  - Service: cart-microservice
  - Component: ShoppingCartImpl
  - Database: shopping_cart table (YSQL)
  - Repository Method: updateQuantityForShoppingCart()
- **Implementation:** [ShoppingCartImpl.java](cart-microservice/src/main/java/com/yugabyte/app/yugastore/cart/service/ShoppingCartImpl.java#L42-L45)
- **Example Scenario:** User has 2x of product B00BKQT2OI, adds again → quantity becomes 3

#### **BR-CART-003: Remove Decrement Logic**
- **Description:** When removing a product from cart, if quantity > 1, decrement by 1; if quantity = 1, delete the cart entry entirely
- **Severity:** CORE
- **Triggering Conditions:** User removes a product from cart
- **Inputs Required:** userId (String), asin (String)
- **Validation Logic:** 
  - If `quantity > 1`: decrement quantity
  - If `quantity == 1`: delete cart entry
- **Outputs:** Cart entry updated or deleted
- **Dependencies:** 
  - Service: cart-microservice
  - Component: ShoppingCartImpl
  - Database: shopping_cart table (YSQL)
  - Repository Methods: decrementQuantityForShoppingCart(), deleteById()
- **Implementation:** [ShoppingCartImpl.java](cart-microservice/src/main/java/com/yugabyte/app/yugastore/cart/service/ShoppingCartImpl.java#L69-L76)
- **Example Scenario:** 
  - User has 3x of product → removes once → quantity becomes 2
  - User has 1x of product → removes once → product removed from cart

#### **BR-CART-004: Cart Key Composite Format**
- **Description:** Shopping cart entries use composite key format: "{userId}-{asin}"
- **Severity:** CORE
- **Triggering Conditions:** All cart operations
- **Inputs Required:** userId (String), asin (String)
- **Key Format:** `cart_key = userId + "-" + asin`
- **Dependencies:** 
  - Service: cart-microservice
  - Component: ShoppingCartImpl, ShoppingCartKey
  - Database: shopping_cart.cart_key (primary key)
- **Implementation:** [ShoppingCartImpl.java](cart-microservice/src/main/java/com/yugabyte/app/yugastore/cart/service/ShoppingCartImpl.java#L41,L69,L87)
- **Example Scenario:** User "u1001" adds product "B00BKQT2OI" → cart_key = "u1001-B00BKQT2OI"

#### **BR-CART-005: Cart Clear on Successful Checkout**
- **Description:** All cart entries for a user are deleted after successful checkout
- **Severity:** CORE
- **Triggering Conditions:** Successful checkout transaction completion
- **Inputs Required:** userId (String)
- **Side Effects:** All shopping_cart rows for user deleted
- **Dependencies:** 
  - Service: cart-microservice, checkout-microservice
  - Component: ShoppingCartImpl
  - Database: shopping_cart table (YSQL)
  - Repository Method: deleteProductsInCartByUserId()
- **Implementation:** [ShoppingCartImpl.java](cart-microservice/src/main/java/com/yugabyte/app/yugastore/cart/service/ShoppingCartImpl.java#L94-L97)
- **Example Scenario:** User completes checkout → cart emptied automatically

#### **BR-CART-006: Cart Timestamp Tracking**
- **Description:** Each cart entry records the timestamp when the product was first added
- **Severity:** POLICY
- **Triggering Conditions:** Product added to cart for first time
- **Inputs Required:** userId (String), asin (String)
- **Outputs:** time_added field set to LocalDateTime.now()
- **Dependencies:** 
  - Service: cart-microservice
  - Component: ShoppingCartImpl
  - Database: shopping_cart.time_added (TEXT)
- **Implementation:** [ShoppingCartImpl.java](cart-microservice/src/main/java/com/yugabyte/app/yugastore/cart/service/ShoppingCartImpl.java#L86)
- **Example Scenario:** User adds product at 2024-01-15T10:30:00 → time_added = "2024-01-15T10:30:00"

---

### **9.4 Checkout & Order Processing Rules**

#### **BR-CHECKOUT-001: Inventory Validation Pre-Checkout**
- **Description:** Before checkout, system must validate that sufficient inventory exists for all cart items
- **Severity:** CORE
- **Triggering Conditions:** User initiates checkout
- **Inputs Required:** userId (String), Map<asin, quantity> from cart
- **Validation Logic:** For each product: `productInventory.getQuantity() >= requestedQuantity`
- **Exception Thrown:** NotEnoughProductsInStockException if validation fails
- **Dependencies:** 
  - Service: checkout-microservice
  - Component: CheckoutServiceImpl
  - Database: product_inventory table (YCQL, transactions enabled)
  - Exception: NotEnoughProductsInStockException
- **Implementation:** [CheckoutServiceImpl.java](checkout-microservice/src/main/java/com/yugabyte/app/yugastore/cronoscheckoutapi/service/CheckoutServiceImpl.java#L63-L65)
- **Example Scenario:** 
  - Cart has 5x of product, inventory shows 3 available → checkout fails with "Not enough products in stock"
  - Cart has 2x of product, inventory shows 10 available → validation passes

#### **BR-CHECKOUT-002: Atomic Inventory Deduction**
- **Description:** Inventory deduction must be atomic using Cassandra transactions to prevent overselling
- **Severity:** SAFETY
- **Triggering Conditions:** Checkout validation passes
- **Transaction Boundaries:** 
  ```
  BEGIN TRANSACTION
    UPDATE product_inventory SET quantity = quantity - {N} WHERE asin = '{asin}'
    INSERT INTO orders (...)
  END TRANSACTION
  ```
- **Rollback Conditions:** Any failure during transaction rolls back all changes
- **Dependencies:** 
  - Service: checkout-microservice
  - Component: CheckoutServiceImpl
  - Database: product_inventory (YCQL with transactions='enabled')
  - CassandraOperations: cassandraTemplate
- **Implementation:** [CheckoutServiceImpl.java](checkout-microservice/src/main/java/com/yugabyte/app/yugastore/cronoscheckoutapi/service/CheckoutServiceImpl.java#L68-L81)
- **Example Scenario:** User checks out 3 items → inventory decremented by 3 and order created, both or neither

#### **BR-CHECKOUT-003: Empty Cart Prevention**
- **Description:** Checkout only proceeds if cart contains at least one product
- **Severity:** UX
- **Triggering Conditions:** User initiates checkout
- **Validation Logic:** `products.size() != 0`
- **Behavior on Empty Cart:** Returns null, no order created
- **Dependencies:** 
  - Service: checkout-microservice
  - Component: CheckoutServiceImpl
- **Implementation:** [CheckoutServiceImpl.java](checkout-microservice/src/main/java/com/yugabyte/app/yugastore/cronoscheckoutapi/service/CheckoutServiceImpl.java#L56)
- **Example Scenario:** User clicks checkout with empty cart → no operation, returns null

#### **BR-CHECKOUT-004: Order ID Generation**
- **Description:** Each order is assigned a unique UUID as the order identifier
- **Severity:** CORE
- **Triggering Conditions:** Order creation during checkout
- **ID Format:** UUID v4 (e.g., "a1b2c3d4-e5f6-7890-abcd-ef1234567890")
- **Outputs:** order.id (UUID string)
- **Dependencies:** 
  - Service: checkout-microservice
  - Component: CheckoutServiceImpl
  - Java Util: UUID.randomUUID()
- **Implementation:** [CheckoutServiceImpl.java](checkout-microservice/src/main/java/com/yugabyte/app/yugastore/cronoscheckoutapi/service/CheckoutServiceImpl.java#L106)
- **Example Scenario:** Checkout creates order with ID "f47ac10b-58cc-4372-a567-0e02b2c3d479"

#### **BR-CHECKOUT-005: Order Total Calculation**
- **Description:** Order total is calculated by summing (product_price × quantity) for all cart items
- **Severity:** CORE
- **Triggering Conditions:** Checkout processing
- **Calculation Logic:** `Σ (productDetails.getPrice() * quantity)`
- **Outputs:** order_total (double)
- **Dependencies:** 
  - Service: checkout-microservice
  - Component: CheckoutServiceImpl
  - External API: ProductCatalogRestClient.getProductDetails()
- **Implementation:** [CheckoutServiceImpl.java](checkout-microservice/src/main/java/com/yugabyte/app/yugastore/cronoscheckoutapi/service/CheckoutServiceImpl.java#L91-L99)
- **Example Scenario:** Cart has 2x $14.99 book + 1x $29.99 product → order_total = $59.97

#### **BR-CHECKOUT-006: Order Details String Format**
- **Description:** Order details are stored as human-readable string summarizing purchased items and total
- **Severity:** POLICY
- **Triggering Conditions:** Order creation
- **String Format:** 
  ```
  "Customer bought these Items: Product: {title}, Quantity: {qty}; ... Order Total is : {total}"
  ```
- **Dependencies:** 
  - Service: checkout-microservice
  - Component: CheckoutServiceImpl
  - Database: orders.order_details (TEXT)
- **Implementation:** [CheckoutServiceImpl.java](checkout-microservice/src/main/java/com/yugabyte/app/yugastore/cronoscheckoutapi/service/CheckoutServiceImpl.java#L54-L73)
- **Example Scenario:** "Customer bought these Items: Product: The Great Gatsby, Quantity: 2; Order Total is : 29.98"

#### **BR-CHECKOUT-007: Order Timestamp Recording**
- **Description:** Order timestamp is recorded as LocalDateTime string when order is created
- **Severity:** CORE
- **Triggering Conditions:** Order creation
- **Timestamp Format:** ISO-8601 LocalDateTime (e.g., "2024-01-15T10:30:00")
- **Dependencies:** 
  - Service: checkout-microservice
  - Component: CheckoutServiceImpl
  - Database: orders.order_time (TEXT)
- **Implementation:** [CheckoutServiceImpl.java](checkout-microservice/src/main/java/com/yugabyte/app/yugastore/cronoscheckoutapi/service/CheckoutServiceImpl.java#L104-L108)
- **Example Scenario:** Order created on Jan 15, 2024 at 10:30 AM → order_time = "2024-01-15T10:30:00"

#### **BR-CHECKOUT-008: Hardcoded User ID Constraint**
- **Description:** All orders are currently assigned to user_id = 1 (hardcoded, not session-based)
- **Severity:** POLICY (KNOWN LIMITATION)
- **Triggering Conditions:** Order creation
- **Current Behavior:** `order.setUser_id(1)`
- **Known Issue:** Should use actual authenticated user ID from session
- **Dependencies:** 
  - Service: checkout-microservice
  - Component: CheckoutServiceImpl
- **Implementation:** [CheckoutServiceImpl.java](checkout-microservice/src/main/java/com/yugabyte/app/yugastore/cronoscheckoutapi/service/CheckoutServiceImpl.java#L107)
- **Example Scenario:** Any user checkout → order.user_id = 1 (incorrect, needs fix)

---

### **9.5 Product Catalog Rules**

#### **BR-PRODUCT-001: Product Recommendation Limit**
- **Description:** Product recommendations (Also Bought) are limited to 10 products with valid images
- **Severity:** UX
- **Triggering Conditions:** Product detail page load, recommendations requested
- **Validation Logic:** 
  - `count <= 10`
  - `temp.isPresent() && !StringUtils.isEmpty(temp.get().getImUrl())`
- **Dependencies:** 
  - Service: products-microservice
  - Component: ProductMetadataRestRepo
  - Database: products table (cronos.products)
- **Implementation:** [ProductMetadataRestRepo.java](products-microservice/src/main/java/com/yugabyte/app/yugastore/repo/rest/ProductMetadataRestRepo.java#L66-L70)
- **Example Scenario:** Product has 15 related items → only first 10 with images shown

#### **BR-PRODUCT-002: Product Ranking Index**
- **Description:** Products are ranked within categories using sales_rank index for efficient top-products queries
- **Severity:** CORE
- **Triggering Conditions:** Category browsing, bestseller retrieval
- **Index Name:** top_products_in_category
- **Index Columns:** (category, sales_rank)
- **Dependencies:** 
  - Database: product_rankings table (YCQL)
  - Index: CREATE INDEX top_products_in_category ON product_rankings (category, sales_rank)
- **Implementation:** [schema.cql](resources/schema.cql#L48-L50)
- **Example Scenario:** Query "top books" → uses index on (category='Books', sales_rank ASC)

#### **BR-PRODUCT-003: Category Set Storage**
- **Description:** Products can belong to multiple categories stored as a set (no duplicates)
- **Severity:** CORE
- **Triggering Conditions:** Product metadata storage
- **Data Type:** `categories set<text>`
- **Dependencies:** 
  - Database: products.categories (YCQL set type)
- **Implementation:** [schema.cql](resources/schema.cql#L21)
- **Example Scenario:** Book product belongs to ["Books", "Fiction", "Bestsellers"]

#### **BR-PRODUCT-004: Related Products Lists**
- **Description:** Products maintain four types of relationships: also_bought, also_viewed, bought_together, buy_after_viewing
- **Severity:** POLICY
- **Data Type:** `frozen<list<text>>` for each relationship type
- **Dependencies:** 
  - Database: products table (YCQL)
  - Columns: also_bought, also_viewed, bought_together, buy_after_viewing
- **Implementation:** [schema.cql](resources/schema.cql#L15-L18)
- **Example Scenario:** Product B00BKQT2OI → also_bought = ["B00BKQT3XT", "B00BKQT4YZ"]

#### **BR-PRODUCT-005: Product Review Aggregation**
- **Description:** Products store aggregated review metrics: num_reviews, num_stars, avg_stars
- **Severity:** POLICY
- **Triggering Conditions:** Product display, sorting
- **Metrics:**
  - num_reviews (int): Total number of reviews
  - num_stars (int): Total star count (sum of all ratings)
  - avg_stars (double): Average star rating
- **Dependencies:** 
  - Database: products table, product_rankings table (YCQL)
- **Implementation:** [schema.cql](resources/schema.cql#L22-L24,L41-L43)
- **Example Scenario:** Product has 50 reviews totaling 230 stars → avg_stars = 4.6

---

### **9.6 Database Transaction Rules**

#### **BR-DB-001: Transactional Tables**
- **Description:** orders and product_inventory tables have transactions enabled for ACID guarantees
- **Severity:** SAFETY
- **Tables with Transactions:**
  - cronos.orders: `transactions = {'enabled': 'true'}`
  - cronos.product_inventory: `transactions = {'enabled': 'true'}`
- **Tables without Transactions:**
  - cronos.products: `transactions = {'enabled': 'false'}`
  - cronos.product_rankings: `transactions = {'enabled': 'false'}`
- **Dependencies:** 
  - Database: YugabyteDB YCQL
- **Implementation:** [schema.cql](resources/schema.cql#L60,L72)
- **Rationale:** Orders and inventory require consistency; catalog data is read-mostly

#### **BR-DB-002: Shopping Cart Primary Key**
- **Description:** Shopping cart uses cart_key (TEXT) as primary key, not composite PK
- **Severity:** CORE
- **Key Format:** "{userId}-{asin}"
- **Dependencies:** 
  - Database: shopping_cart table (YSQL)
  - Primary Key: cart_key
- **Implementation:** [schema.sql](resources/schema.sql#L1-L7)
- **Example:** cart_key = "u1001-B00BKQT2OI"

#### **BR-DB-003: NOT NULL Constraints**
- **Description:** Shopping cart table enforces NOT NULL on all columns to prevent incomplete data
- **Severity:** SAFETY
- **Columns:** cart_key, user_id, asin, time_added, quantity (all NOT NULL)
- **Dependencies:** 
  - Database: shopping_cart table (YSQL)
- **Implementation:** [schema.sql](resources/schema.sql#L2-L6)
- **Example Scenario:** Attempt to insert cart entry with null quantity → rejected by database

---

### **9.7 API Contract Rules**

#### **BR-API-001: Required Query Parameters**
- **Description:** Cart and checkout APIs require userid as a mandatory query parameter
- **Severity:** CORE
- **Endpoints:**
  - /cart-microservice/shoppingCart/addProduct (userid, asin required)
  - /cart-microservice/shoppingCart/productsInCart (userid required)
  - /cart-microservice/shoppingCart/removeProduct (userid, asin required)
  - /cart-microservice/shoppingCart/clearCart (userid required)
- **HTTP Status on Missing Param:** 400 Bad Request (expected)
- **Dependencies:** 
  - Service: cart-microservice
  - OpenAPI Spec: cart-microservice.yaml
- **Implementation:** [cart-microservice.yaml](openapi/cart-microservice.yaml#L22-L27,L50-L55,L78-L83,L106-L111)

#### **BR-API-002: ASIN Format**
- **Description:** Product identifiers follow Amazon Standard Identification Number (ASIN) format
- **Severity:** CORE
- **Format:** Alphanumeric string (typically 10 characters, e.g., "B00BKQT2OI")
- **Usage:** Primary key for products, inventory, cart items
- **Dependencies:** 
  - All microservices
  - Database tables: products, product_inventory, product_rankings, shopping_cart
- **Example:** "B00BKQT2OI", "B00BKQT3XT"

#### **BR-API-003: Checkout Response Status Enum**
- **Description:** Checkout API returns status field with enum values: SUCCESS or FAILURE
- **Severity:** CORE
- **Response Format:**
  ```json
  {
    "status": "SUCCESS|FAILURE",
    "orderNumber": "uuid-string",
    "orderDetails": "human-readable-string"
  }
  ```
- **Dependencies:** 
  - Service: checkout-microservice
  - OpenAPI Spec: checkout-microservice.yaml
- **Implementation:** [checkout-microservice.yaml](openapi/checkout-microservice.yaml#L52-L56)

---

### **9.8 Error Handling & Exception Rules**

#### **BR-ERROR-001: NotEnoughProductsInStockException**
- **Description:** Custom exception thrown when checkout inventory validation fails
- **Severity:** CORE
- **Triggering Conditions:** `productInventory.getQuantity() < requestedQuantity`
- **Exception Message Format:** Includes product title and available quantity
- **HTTP Response:** 200 OK with status="FAILURE" and orderDetails="Product is Out of Stock!"
- **Dependencies:** 
  - Service: checkout-microservice
  - Exception Class: NotEnoughProductsInStockException
  - Handler: CheckoutController
- **Implementation:** 
  - Exception: [NotEnoughProductsInStockException.java](checkout-microservice/src/main/java/com/yugabyte/app/yugastore/cronoscheckoutapi/exception/NotEnoughProductsInStockException.java)
  - Throw: [CheckoutServiceImpl.java](checkout-microservice/src/main/java/com/yugabyte/app/yugastore/cronoscheckoutapi/service/CheckoutServiceImpl.java#L64)
  - Catch: [CheckoutController.java](checkout-microservice/src/main/java/com/yugabyte/app/yugastore/cronoscheckoutapi/controller/CheckoutController.java#L40)
- **Example Scenario:** User tries to buy 5 items when only 2 in stock → exception thrown with message "Product: {title}, Available Quantity: 2"

#### **BR-ERROR-002: Security Exception Handling**
- **Description:** All microservices disable CSRF and configure exception handling via Spring Security
- **Severity:** SAFETY
- **Configuration:** 
  ```java
  http.csrf().disable()
      .exceptionHandling()
      .and().authorizeRequests().anyRequest().permitAll()
  ```
- **Current Policy:** All requests permitted (no authentication enforced at Spring Security level)
- **Dependencies:** 
  - All microservices
  - Component: SecurityConfiguration
- **Implementation:** [SecurityConfiguration.java](products-microservice/src/main/java/com/yugabyte/app/yugastore/config/SecurityConfiguration.java#L12-L14)
- **Rationale:** CSRF disabled for stateless REST APIs; authentication handled by login service

---

### **9.9 Business Logic Invariants**

#### **BR-INVARIANT-001: Cart-Checkout-Inventory Consistency**
- **Description:** System maintains consistency: cart items → inventory validation → inventory deduction → cart clear
- **Severity:** SAFETY
- **Workflow Sequence:**
  1. Cart contains items (cart-microservice)
  2. Checkout validates inventory (checkout-microservice)
  3. Inventory decremented atomically (checkout-microservice, YCQL transaction)
  4. Order created (checkout-microservice)
  5. Cart cleared (cart-microservice)
- **Failure Handling:** If any step fails, transaction rolls back (step 3-4), cart remains unchanged
- **Dependencies:** 
  - Services: cart-microservice, checkout-microservice
  - Database: shopping_cart (YSQL), product_inventory (YCQL transactional)
- **Example Scenario:** Concurrent checkouts for same product → first succeeds and decrements inventory, second validates against updated inventory

#### **BR-INVARIANT-002: Single Product Per Cart Entry**
- **Description:** Each (userId, asin) pair has at most one cart entry; quantity field tracks amount
- **Severity:** CORE
- **Enforcement:** Primary key constraint on cart_key = "{userId}-{asin}"
- **Add Behavior:** Increment quantity if exists, create new if not
- **Dependencies:** 
  - Service: cart-microservice
  - Database: shopping_cart.cart_key (primary key)
- **Example Scenario:** User adds same product 3 times → single cart entry with quantity=3

#### **BR-INVARIANT-003: Non-Negative Inventory**
- **Description:** Product inventory quantity should never go negative (implied constraint, not enforced by database)
- **Severity:** SAFETY
- **Enforcement:** Pre-checkout validation prevents negative inventory
- **Validation:** `if (productInventory.getQuantity() < requestedQuantity) throw Exception`
- **Dependencies:** 
  - Service: checkout-microservice
  - Component: CheckoutServiceImpl
- **Known Risk:** Race condition possible without database-level CHECK constraint
- **Recommendation:** Add CHECK constraint `quantity >= 0` on product_inventory table
- **Example Scenario:** Concurrent checkouts could theoretically create negative inventory if validation race occurs

---

### **9.10 Configuration & Operational Rules**

#### **BR-CONFIG-001: Service Discovery Registration**
- **Description:** All microservices register with Eureka server for service discovery
- **Severity:** CORE
- **Eureka Server:** http://localhost:8761
- **Registered Services:** products-microservice, cart-microservice, login-microservice, checkout-microservice
- **Dependencies:** 
  - Service: eureka-server-local
  - Framework: Spring Cloud Netflix Eureka
- **Example:** checkout-microservice registers as "CHECKOUT-MICROSERVICE" with Eureka

#### **BR-CONFIG-002: API Gateway Routing**
- **Description:** All client requests route through API Gateway for service aggregation
- **Severity:** CORE
- **Gateway Port:** 8081
- **Routing Patterns:**
  - /cart-microservice/** → cart-microservice:8083
  - /checkout-microservice/** → checkout-microservice:8086
  - /products-microservice/** → products-microservice:8082
  - /login-microservice/** → login-microservice:8085
- **Dependencies:** 
  - Service: api-gateway-microservice
  - Framework: Spring Cloud Gateway

#### **BR-CONFIG-003: Session-Scoped Services**
- **Description:** Cart and checkout services use session-scoped beans to maintain user state
- **Severity:** CORE
- **Scope Annotation:** 
  ```java
  @Scope(value = WebApplicationContext.SCOPE_SESSION, proxyMode = ScopedProxyMode.TARGET_CLASS)
  ```
- **Affected Services:** ShoppingCartImpl, CheckoutServiceImpl
- **Dependencies:** 
  - Services: cart-microservice, checkout-microservice
  - Spring Context: WebApplicationContext
- **Implementation:** 
  - [ShoppingCartImpl.java](cart-microservice/src/main/java/com/yugabyte/app/yugastore/cart/service/ShoppingCartImpl.java#L20)
  - [CheckoutServiceImpl.java](checkout-microservice/src/main/java/com/yugabyte/app/yugastore/cronoscheckoutapi/service/CheckoutServiceImpl.java#L27)
- **Rationale:** Maintains per-user cart and checkout state across requests within same session

---

### **9.11 UI/UX Business Rules**

#### **BR-UX-001: Pagination Default**
- **Description:** Product listings display 12 items per page by default
- **Severity:** UX
- **Triggering Conditions:** Browse products, category pages
- **Page Size:** 12 products
- **Navigation:** Previous/Next buttons
- **Dependencies:** 
  - Service: react-ui
  - Component: Product listing pages

#### **BR-UX-002: Star Rating Display**
- **Description:** Product ratings display as visual stars with support for half-stars (5-star system)
- **Severity:** UX
- **Rating Range:** 0.0 to 5.0 (double)
- **Display Logic:** Render filled, half-filled, or empty stars based on avg_stars value
- **Dependencies:** 
  - Service: react-ui
  - Data Source: products.avg_stars
- **Example:** avg_stars=4.3 → ★★★★☆ (4.5 stars shown)

#### **BR-UX-003: Cart Count Badge**
- **Description:** Navigation bar displays cart item count badge showing total quantity of all items
- **Severity:** UX
- **Calculation:** Sum of all quantities across cart entries for current user
- **Real-time Update:** Badge updates when items added/removed
- **Dependencies:** 
  - Service: react-ui
  - API: /cart-microservice/shoppingCart/productsInCart
- **Example:** Cart has 2x Book + 3x Music album → badge shows "5"

#### **BR-UX-004: Newsletter Email Format**
- **Description:** Newsletter subscription form accepts email input (validation not currently enforced)
- **Severity:** UX
- **Current State:** UI component present, backend integration pending
- **Expected Format:** Valid email address (e.g., user@example.com)
- **Dependencies:** 
  - Service: react-ui
  - Component: Newsletter subscription form (footer)
- **Gap:** Backend integration and email validation not implemented

---

## **10. Business Rules Summary Matrix**

| Rule ID | Category | Severity | Description | Enforced By |
|---------|----------|----------|-------------|-------------|
| BR-AUTH-001 | Authentication | CORE | Username 6-32 chars | UserValidator |
| BR-AUTH-002 | Authentication | CORE | Password 8-32 chars | UserValidator |
| BR-AUTH-003 | Authentication | CORE | Unique username | UserValidator + DB |
| BR-AUTH-004 | Authentication | UX | Password confirmation match | UserValidator |
| BR-AUTH-005 | Authentication | CORE | Required fields not empty | UserValidator |
| BR-CART-001 | Cart | POLICY | Default quantity = 1 | ShoppingCartImpl |
| BR-CART-002 | Cart | CORE | Increment on duplicate add | ShoppingCartImpl |
| BR-CART-003 | Cart | CORE | Decrement or delete on remove | ShoppingCartImpl |
| BR-CART-004 | Cart | CORE | Cart key format {userId}-{asin} | ShoppingCartImpl |
| BR-CART-005 | Cart | CORE | Clear cart on checkout | ShoppingCartImpl |
| BR-CART-006 | Cart | POLICY | Track time_added | ShoppingCartImpl |
| BR-CHECKOUT-001 | Checkout | CORE | Validate inventory pre-checkout | CheckoutServiceImpl |
| BR-CHECKOUT-002 | Checkout | SAFETY | Atomic inventory deduction | Cassandra Transaction |
| BR-CHECKOUT-003 | Checkout | UX | Prevent empty cart checkout | CheckoutServiceImpl |
| BR-CHECKOUT-004 | Checkout | CORE | UUID order ID | CheckoutServiceImpl |
| BR-CHECKOUT-005 | Checkout | CORE | Calculate order total | CheckoutServiceImpl |
| BR-CHECKOUT-006 | Checkout | POLICY | Order details string format | CheckoutServiceImpl |
| BR-CHECKOUT-007 | Checkout | CORE | Record order timestamp | CheckoutServiceImpl |
| BR-CHECKOUT-008 | Checkout | POLICY | Hardcoded user_id=1 (bug) | CheckoutServiceImpl |
| BR-PRODUCT-001 | Catalog | UX | Limit recommendations to 10 | ProductMetadataRestRepo |
| BR-PRODUCT-002 | Catalog | CORE | Category ranking index | YCQL Index |
| BR-PRODUCT-003 | Catalog | CORE | Categories as set | YCQL Schema |
| BR-PRODUCT-004 | Catalog | POLICY | Four relationship types | YCQL Schema |
| BR-PRODUCT-005 | Catalog | POLICY | Review aggregation metrics | YCQL Schema |
| BR-DB-001 | Database | SAFETY | Transactional tables | YCQL Schema |
| BR-DB-002 | Database | CORE | Cart primary key format | YSQL Schema |
| BR-DB-003 | Database | SAFETY | NOT NULL constraints | YSQL Schema |
| BR-API-001 | API | CORE | Required query params | OpenAPI Spec |
| BR-API-002 | API | CORE | ASIN format | All Services |
| BR-API-003 | API | CORE | Checkout response enum | OpenAPI Spec |
| BR-ERROR-001 | Error Handling | CORE | Out of stock exception | CheckoutServiceImpl |
| BR-ERROR-002 | Security | SAFETY | CSRF disabled for REST | SecurityConfiguration |
| BR-INVARIANT-001 | Consistency | SAFETY | Cart-checkout-inventory flow | Multi-service |
| BR-INVARIANT-002 | Consistency | CORE | Single cart entry per product | DB + ShoppingCartImpl |
| BR-INVARIANT-003 | Consistency | SAFETY | Non-negative inventory (implied) | CheckoutServiceImpl |
| BR-CONFIG-001 | Operations | CORE | Eureka service discovery | Spring Cloud |
| BR-CONFIG-002 | Operations | CORE | API Gateway routing | Spring Cloud Gateway |
| BR-CONFIG-003 | Operations | CORE | Session-scoped services | Spring Framework |
| BR-UX-001 | UI/UX | UX | 12 items per page | React UI |
| BR-UX-002 | UI/UX | UX | 5-star rating display | React UI |
| BR-UX-003 | UI/UX | UX | Cart count badge | React UI |
| BR-UX-004 | UI/UX | UX | Newsletter email format | React UI (incomplete) |

---

## **11. Business Rules Traceability**

### **11.1 Source Code to Business Rule Mapping**

| Source File | Line(s) | Rule ID(s) |
|-------------|---------|------------|
| UserValidator.java | 23-25 | BR-AUTH-001 |
| UserValidator.java | 29-31 | BR-AUTH-002 |
| UserValidator.java | 27-29 | BR-AUTH-003 |
| UserValidator.java | 33-35 | BR-AUTH-004 |
| UserValidator.java | 22, 28 | BR-AUTH-005 |
| ShoppingCartImpl.java | 24, 47 | BR-CART-001 |
| ShoppingCartImpl.java | 42-45 | BR-CART-002 |
| ShoppingCartImpl.java | 69-76 | BR-CART-003 |
| ShoppingCartImpl.java | 41, 69, 87 | BR-CART-004 |
| ShoppingCartImpl.java | 94-97 | BR-CART-005 |
| ShoppingCartImpl.java | 86 | BR-CART-006 |
| CheckoutServiceImpl.java | 63-65 | BR-CHECKOUT-001 |
| CheckoutServiceImpl.java | 68-81 | BR-CHECKOUT-002 |
| CheckoutServiceImpl.java | 56 | BR-CHECKOUT-003 |
| CheckoutServiceImpl.java | 106 | BR-CHECKOUT-004 |
| CheckoutServiceImpl.java | 91-99 | BR-CHECKOUT-005 |
| CheckoutServiceImpl.java | 54-73 | BR-CHECKOUT-006 |
| CheckoutServiceImpl.java | 104-108 | BR-CHECKOUT-007 |
| CheckoutServiceImpl.java | 107 | BR-CHECKOUT-008 |
| ProductMetadataRestRepo.java | 66-70 | BR-PRODUCT-001 |
| schema.cql | 48-50 | BR-PRODUCT-002 |
| schema.cql | 21 | BR-PRODUCT-003 |
| schema.cql | 15-18 | BR-PRODUCT-004 |
| schema.cql | 22-24, 41-43 | BR-PRODUCT-005 |
| schema.cql | 60, 72 | BR-DB-001 |
| schema.sql | 1-7 | BR-DB-002, BR-DB-003 |
| cart-microservice.yaml | Various | BR-API-001 |
| checkout-microservice.yaml | 52-56 | BR-API-003 |
| CheckoutController.java | 40 | BR-ERROR-001 |
| SecurityConfiguration.java | 12-14 | BR-ERROR-002 |

### **11.2 Database Constraints to Business Rules**

| Table | Constraint Type | Constraint | Rule ID |
|-------|----------------|------------|---------|
| shopping_cart | PRIMARY KEY | cart_key | BR-DB-002, BR-CART-004 |
| shopping_cart | NOT NULL | All columns | BR-DB-003 |
| cronos.orders | TRANSACTIONS | enabled: true | BR-DB-001 |
| cronos.product_inventory | TRANSACTIONS | enabled: true | BR-DB-001 |
| cronos.product_rankings | INDEX | top_products_in_category | BR-PRODUCT-002 |
| users (implied) | UNIQUE | username | BR-AUTH-003 |

### **11.3 API Endpoint to Business Rules**

| Endpoint | Method | Rule ID(s) |
|----------|--------|------------|
| /cart-microservice/shoppingCart/addProduct | GET | BR-CART-001, BR-CART-002, BR-API-001 |
| /cart-microservice/shoppingCart/removeProduct | GET | BR-CART-003, BR-API-001 |
| /cart-microservice/shoppingCart/clearCart | GET | BR-CART-005, BR-API-001 |
| /checkout-microservice/shoppingCart/checkout | POST | BR-CHECKOUT-001 through BR-CHECKOUT-008, BR-INVARIANT-001 |

---

## **12. Known Business Rule Gaps & Recommendations**

### **12.1 Critical Gaps**

1. **BR-CHECKOUT-008 Hardcoded User ID**
   - **Issue:** All orders assigned to user_id=1 regardless of actual user
   - **Impact:** Order tracking broken, security vulnerability
   - **Recommendation:** Use authenticated user ID from session

2. **BR-INVARIANT-003 No Non-Negative Inventory Constraint**
   - **Issue:** Database doesn't enforce quantity >= 0
   - **Impact:** Race conditions could create negative inventory
   - **Recommendation:** Add CHECK constraint `quantity >= 0` on product_inventory

3. **Missing Email Validation (BR-UX-004)**
   - **Issue:** Newsletter form lacks backend and email format validation
   - **Impact:** Invalid emails could be stored
   - **Recommendation:** Implement email regex validation

### **12.2 Recommended New Rules**

1. **BR-CART-007: Maximum Cart Quantity Limit**
   - Prevent users from adding excessive quantities (e.g., max 999 per product)
   - Severity: UX
   - Implementation: Add validation in ShoppingCartImpl

2. **BR-CHECKOUT-009: Order Status Tracking**
   - Track order lifecycle (PENDING, CONFIRMED, SHIPPED, DELIVERED)
   - Severity: CORE
   - Implementation: Add order_status column to orders table

3. **BR-PRODUCT-006: Price Non-Negativity**
   - Product prices must be >= 0
   - Severity: CORE
   - Implementation: Add CHECK constraint on products.price

4. **BR-AUTH-006: Rate Limiting**
   - Limit login attempts (e.g., 5 attempts per 15 minutes)
   - Severity: SECURITY
   - Implementation: Add rate limiter to login-microservice

---

## **13. Conclusion**

This platform represents a **solid foundation for a cloud-native e-commerce system** with strong architectural patterns including microservices, distributed data storage, and service discovery. The current implementation fulfills core e-commerce workflows (browse → cart → checkout) while maintaining clear gaps in areas like payment processing, search, and order tracking.

The comprehensive **business rules catalog** documents 42 identified rules across authentication, cart management, checkout processing, product catalog, database integrity, API contracts, error handling, and operational configuration. Each rule is traced to its implementation in source code, database schemas, and API specifications, providing a complete map of system behavior.

**Key Strengths:**
- Strong transaction guarantees for critical operations (checkout, inventory)
- Comprehensive validation in authentication and cart management
- Well-defined API contracts with OpenAPI specifications
- Atomic operations prevent data inconsistencies

**Critical Improvements Needed:**
- Fix hardcoded user_id in checkout (BR-CHECKOUT-008)
- Add database constraint for non-negative inventory (BR-INVARIANT-003)
- Implement missing validation rules (email, quantity limits)
- Add order lifecycle tracking

The architecture is well-positioned for **modernization and enhancement** through AI-assisted development workflows, with clear requirements, implementation status, and documented business rules providing a roadmap for future development.

