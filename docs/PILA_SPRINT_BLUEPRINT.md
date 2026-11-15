# Pila Sprint Blueprint

## Purpose

This document is the implementation blueprint for the Pila MVP. It converts the product milestones into one-week sprints with individually estimable features.

The delivery order is intentionally strict:

1. Establish a pnpm monorepo with a frontend-only Next.js application and a separate Node.js/Express API.
2. Reproduce the existing Pila proof of concept using typed mock data and local UI state.
3. Review and approve the complete frontend, including exact theme colors and responsive behavior.
4. Implement the database, authentication, backend services, and queue engine.
5. Connect the approved frontend to real backend behavior.
6. Add realtime updates, notifications, security, and pilot operations.

The proof-of-concept reference is:

- <https://claude.ai/artifact/QzSmBKWsZF24QUdQvNm4VZ>

The Express application shell and a health endpoint are established in Phase 1. Production database work and business API features must not start before the frontend sign-off gate at the end of Phase 2.

## Sprint rules

- Sprint length: one week.
- Maximum capacity: 35 story points per sprint.
- Every feature must be estimated at 3, 4, or 5 points.
- Work larger than 5 points must be divided before entering a sprint.
- A sprint may contain fewer than 35 points when that produces a safer delivery boundary.
- Unfinished work moves to the next sprint. The sprint capacity is not increased.
- Bugs discovered within a feature are part of that feature until it meets its acceptance criteria.
- New scope requires backlog review and cannot silently enter an active sprint.

### Point definitions

| Points | Expected characteristics |
|---:|---|
| 3 | Small, well-understood feature with limited integration and straightforward testing. |
| 4 | Medium feature with some state, validation, responsive behavior, or integration risk. |
| 5 | Complex feature with several states, important business rules, cross-component integration, or significant testing. |

## Global definition of ready

A feature is ready for a sprint when:

- Its user or system outcome is clear.
- Its acceptance criteria are testable.
- Required designs, reference screens, and copy are available.
- Dependencies are complete or committed earlier in the same sprint.
- The feature is no larger than 5 points.
- Known security, privacy, localization, and accessibility implications are identified.

## Global definition of done

A feature is done when:

- Its acceptance criteria pass.
- Type-checking, linting, and relevant automated tests pass.
- New behavior has appropriate unit, integration, visual, or end-to-end coverage.
- English and Bisaya behavior is considered where applicable.
- Mobile behavior is verified at a minimum width of 360 pixels.
- Loading, empty, error, disabled, and success states are handled where applicable.
- No customer personal data is exposed in the UI, logs, fixtures, or test output.
- Documentation is updated when the feature changes a workflow or technical contract.
- The feature is demonstrable from the sprint's integrated build.

---

# Phase 1 - Boilerplate

## Boilerplate architecture

The repository uses a pnpm monorepo with explicit application boundaries:

```text
pila/
|-- apps/
|   |-- web/          # Next.js frontend only
|   |-- api/          # Node.js + Express REST API
|   `-- worker/       # Added later for background jobs
|-- packages/
|   |-- contracts/    # Shared request, response, and validation contracts
|   |-- configuration/ # Shared repository configuration
|   `-- testing/      # Shared test utilities and configuration
|-- docs/
|-- package.json
`-- pnpm-workspace.yaml
```

Architecture rules:

- `apps/web` owns presentation, browser state, accessibility, and API consumption. It does not access the database or implement business APIs.
- `apps/api` owns REST endpoints, authentication integration, business rules, and database access when backend implementation begins.
- `packages/contracts` contains framework-neutral schemas and TypeScript types shared by the web and API applications.
- Local development uses the Next.js application on port `3000` and the Express API on port `4000` by default.
- The Next.js development and production configuration rewrites `/api/*` requests to Express so the browser has one application origin and does not require local CORS configuration.
- During the frontend-reproduction phase, Express exposes only operational endpoints such as health status; proof-of-concept behavior continues to use typed mock data until frontend sign-off.

## Sprint 1 - Project foundation

**Objective:** Create a reliable monorepo containing an independently runnable Next.js frontend and Node.js/Express API foundation that can support the full proof-of-concept reproduction.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| FND-001 | Initialize the Next.js frontend application | 5 | `apps/web` uses TypeScript, App Router, Tailwind CSS, and pnpm; development and production builds run successfully, and the application is documented as a frontend-only boundary. |
| FND-002 | Establish the monorepo and Express API foundation | 5 | The root pnpm workspace contains `apps/web`, `apps/api`, and the planned shared-package boundaries; the TypeScript Express API starts independently, shuts down cleanly, and exposes a tested health endpoint without a database dependency. |
| FND-003 | Enable strict TypeScript and import aliases | 3 | Strict mode is enabled, path aliases resolve in development, tests, and production builds, and no unchecked TypeScript errors remain. |
| FND-004 | Configure linting, formatting, and repository standards | 3 | Lint and formatting commands are available, documented, and pass on the initial codebase. |
| FND-005 | Configure unit, component, and end-to-end test foundations | 5 | Vitest, React Testing Library, and Playwright each execute at least one passing example test. |
| FND-006 | Add typed environment configuration | 3 | The web and API applications validate their own environment values, fail fast with clear messages, and keep browser-safe variables separate from API secrets. |
| FND-007 | Add continuous integration checks | 5 | Pull-request or branch checks run installation, linting, type-checking, tests, and production builds for both the web and API workspaces. |
| FND-008 | Create the frontend shell and API proxy boundary | 5 | Public, customer, merchant, and future admin route areas render through a shared root layout; `/api/*` requests are rewritten to Express, and no business API is implemented inside Next.js. |

**Sprint total: 34 points**

**Sprint deliverable:** A clean, tested monorepo with a deployable Next.js frontend and an independently runnable Express health service, ready for visual implementation.

**Excluded:** Database integration, authentication, external APIs, realtime behavior, business API endpoints, and production queue logic.

---

# Phase 2 - Reproduce the proof of concept

## Sprint 2 - Visual system and mock application foundation

**Objective:** Extract the proof-of-concept design language and establish the exact reusable visual and mock-data foundations.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| UI-001 | Create the proof-of-concept screen and state inventory | 3 | Customer, merchant, settings, queue, language, sample-clock, disabled, open, closed, and full states are recorded in a traceable checklist. |
| UI-002 | Implement exact Pila color and theme tokens | 5 | Backgrounds, surfaces, borders, primary cyan, muted text, success, warning, and disabled colors match sampled proof-of-concept values and are exposed as semantic tokens. |
| UI-003 | Implement typography and text hierarchy | 3 | Logo, headings, labels, body copy, statistics, and helper text match the reference hierarchy across mobile and desktop. |
| UI-004 | Build the responsive application frame | 5 | The app frame matches the reference proportions at mobile width and remains usable at tablet and desktop widths. |
| UI-005 | Build the Pila header and demo-status badge | 3 | Logo, product statement, and demo indicator match the reference appearance and responsive wrapping. |
| UI-006 | Build the English and Bisaya language selector | 3 | The selector visually matches the reference, changes the mock locale, and exposes an accessible selected state. |
| UI-007 | Build the customer and merchant role tabs | 3 | Tabs match the reference, support keyboard navigation, and switch views without a page reload. |
| UI-008 | Create shared buttons, fields, cards, tabs, badges, and metric primitives | 5 | Shared components reproduce default, hover, focus, active, disabled, error, and success states. |
| UI-009 | Create typed fixtures and the local mock-state store | 5 | Sample shops, services, employees, schedules, and tickets are type-safe and drive the UI without hardcoded component data. |

**Sprint total: 35 points**

**Sprint deliverable:** The exact Pila visual foundation and an interactive mock application shell.

## Sprint 3 - Customer service discovery UI

**Objective:** Reproduce the proof-of-concept customer discovery experience using mock data.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| UI-010 | Build the service selector | 5 | Haircut, shave, massage, car wash, and check-up options match the reference and display the number of currently open sample shops. |
| UI-011 | Build the shop availability card | 5 | Each card shows shop name, sample status, location, hours, service, price, duration, queue metrics, cutoff time, and the join action. |
| UI-012 | Build customer-side filtering and shop ordering | 5 | Selecting a service filters fixtures and orders shops by join availability followed by estimated wait. |
| UI-013 | Implement shop availability variants | 5 | Open, closed, full, no qualified staff, and cannot-finish-before-closing states display the correct message and button behavior. |
| UI-014 | Reproduce the sample-clock control | 3 | Real time, 10:00 AM, 2:00 PM, 6:45 PM, and 8:30 PM update only the simulated UI state. |
| UI-015 | Implement the location and map-link presentation | 3 | Shop addresses match the reference presentation and open a correctly encoded external map search. |
| UI-016 | Complete responsive customer-card behavior | 5 | Customer content remains readable and touch-friendly at 360-pixel mobile width and approved tablet and desktop widths. |
| UI-017 | Establish screenshot-based visual regression coverage | 4 | Baseline screenshots cover the main customer screen at agreed viewport sizes and can be compared in automated tests. |

**Sprint total: 35 points**

**Sprint deliverable:** A visually faithful customer discovery page with all proof-of-concept availability states.

## Sprint 4 - Customer queue UI

**Objective:** Reproduce the complete customer queue journey using local mock state only.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| UI-018 | Build the join-queue sheet | 5 | The selected shop, service, price, first-name field, privacy note, confirm action, and cancel action match the proof of concept. |
| UI-019 | Add customer-form validation and feedback | 3 | Required, length, invalid-character, submitting, and failure states are visible and accessible without backend calls. |
| UI-020 | Build the customer ticket screen | 5 | Queue number, position, customers ahead, estimated wait, shop details, service, and current status are clearly presented. |
| UI-021 | Build all customer ticket status variants | 5 | Waiting, called, arrived, serving, completed, cancelled, expired, and no-show states are reproducible from fixtures. |
| UI-022 | Build arrival and cancellation confirmations | 3 | Confirm-arrival and cancel-ticket flows use accessible confirmation behavior and update local mock state. |
| UI-023 | Implement customer privacy and consent presentation | 3 | Data-use and retention copy is visible at the appropriate step and does not imply production behavior that is not implemented. |
| UI-024 | Complete Bisaya customer copy | 4 | All customer discovery, join, ticket, status, validation, and availability text has reviewed Bisaya placeholders ready for native-language approval. |
| UI-025 | Test customer keyboard and screen-reader behavior | 5 | The service, join, ticket, arrival, and cancellation flows can be completed using a keyboard and expose meaningful accessible names and status updates. |

**Sprint total: 33 points**

**Sprint deliverable:** A complete customer queue experience that behaves locally like the intended product.

## Sprint 5 - Merchant queue-desk UI

**Objective:** Reproduce the proof-of-concept merchant operating screen with realistic mock interactions.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| UI-026 | Build the merchant shop selector and daily summary | 3 | The selected shop, open status, closing time, and on-duty count match fixture state. |
| UI-027 | Build queue-desk and store-settings tabs | 3 | The tab treatment matches the reference and retains local state when switching views. |
| UI-028 | Build the being-served list | 5 | Active tickets display number, customer, service, employee, elapsed progress, done, and no-show actions. |
| UI-029 | Build the waiting list | 5 | Waiting tickets display number, customer, service, wait age, call state, and remove action. |
| UI-030 | Build the add-walk-in form | 5 | Staff can enter a customer, select a service, validate the form, and add a ticket to local mock state. |
| UI-031 | Implement call-next and unavailable explanations | 4 | Call-next updates mock state when possible and clearly explains no-free-staff and other disabled conditions. |
| UI-032 | Build daily statistics and new-day controls | 3 | Served, no-show, and waiting counts update from local state; new-day uses a confirmation step. |
| UI-033 | Implement merchant mock queue transitions | 4 | Call, start, complete, no-show, remove, and add-walk-in transitions update all affected mock metrics consistently. |
| UI-034 | Complete responsive and accessible queue-desk behavior | 3 | The desk is usable at 360 pixels, important controls remain reachable, and status changes are announced accessibly. |

**Sprint total: 35 points**

**Sprint deliverable:** A merchant can operate a full simulated queue day without a database.

## Sprint 6 - Merchant settings UI

**Objective:** Reproduce the complete merchant configuration experience using local fixtures.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| UI-035 | Build store-detail and capacity settings | 4 | Shop name, location, and waiting capacity match the proof-of-concept layout and validate locally. |
| UI-036 | Build weekly store-hours editing | 5 | Each day supports open/closed state and opening and closing times with validation for invalid ranges. |
| UI-037 | Implement copy-Monday-to-all-days | 3 | The action copies Monday's current values to every day and gives visible confirmation. |
| UI-038 | Build services, prices, and duration settings | 5 | Services can be enabled or disabled and locally edited with price and duration validation. |
| UI-039 | Build employee and service-skill management | 5 | Employees can be added, removed, marked on duty, and assigned supported services in local state. |
| UI-040 | Build the add-shop form | 3 | The proof-of-concept add-shop path is represented with required fields and local creation behavior. |
| UI-041 | Implement settings validation and save feedback | 3 | Dirty, saving, saved, invalid, and failed mock states are consistently represented. |
| UI-042 | Complete Bisaya merchant copy | 3 | Merchant queue and settings terminology has complete Bisaya placeholders ready for native-language review. |
| UI-043 | Complete proof-of-concept visual parity review | 4 | Customer and merchant screens are compared against the reference checklist; color, spacing, border, typography, and control discrepancies are resolved or documented. |

**Sprint total: 35 points**

**Sprint deliverable:** All visible proof-of-concept customer and merchant features exist in the local frontend.

## Sprint 7 - Frontend stabilization and sign-off

**Objective:** Make the frontend complete, testable, responsive, and ready for explicit approval before backend work begins.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| UI-044 | Add loading, empty, error, offline, and stale-data UI states | 5 | Every major customer and merchant area has a coherent non-happy-path state driven by fixtures. |
| UI-045 | Complete cross-page responsive review | 5 | All approved screens pass review at mobile, tablet, laptop, and wide-desktop viewports without clipping or unusable controls. |
| UI-046 | Perform final theme and visual-difference audit | 5 | Exact semantic colors are documented; automated screenshots and manual review show no unexplained high-impact differences from the proof of concept. |
| UI-047 | Perform the frontend accessibility audit | 5 | Critical flows meet the agreed WCAG AA target for keyboard use, accessible names, focus, contrast, and status messaging. |
| UI-048 | Run the supported-browser UI matrix | 3 | Critical mock workflows pass in current Chrome, Edge, Firefox, and Safari-equivalent automated coverage where available. |
| UI-049 | Document the component and fixture system | 5 | Developers can identify reusable components, theme tokens, fixture factories, supported states, and localization conventions. |
| UI-050 | Add proof-of-concept workflow end-to-end tests | 5 | Automated tests cover customer discovery, joining, ticket tracking, merchant walk-in, calling, completion, settings, language, and sample clock. |

**Sprint total: 33 points**

**Sprint deliverable:** An approved, backend-independent reproduction of the Pila proof of concept.

### Phase 2 exit gate - Frontend approval

Backend work may begin only when:

- The customer and merchant reference checklists are complete.
- Exact Pila theme tokens have been approved.
- Main screenshots have no unexplained material visual differences.
- Mobile and desktop workflows pass.
- English and Bisaya coverage is complete enough for native review.
- Mock end-to-end tests pass.
- The product owner explicitly accepts the frontend reproduction.

---

# Phase 3 - Database, authentication, and merchant persistence

## Sprint 8 - Backend foundation

**Objective:** Introduce the production data and identity foundations without changing the approved UI.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| BE-001 | Provision PostgreSQL and configure Drizzle | 5 | Local and test databases connect through validated configuration; migrations can run from an empty database. |
| BE-002 | Implement user, merchant-account, membership, and role schema | 5 | The schema supports staff, manager, owner, and administrator membership without cross-merchant ambiguity. |
| BE-003 | Implement shop, hours, service, employee, and skill schema | 5 | All merchant settings represented in the approved UI have normalized persistent models and constraints. |
| BE-004 | Add migrations and reproducible seed data | 4 | A single documented command creates the schema and proof-of-concept sample shops, services, employees, and schedules. |
| BE-005 | Implement authentication and secure sessions | 5 | Supported sign-in creates a secure session and protected routes reject unauthenticated access. |
| BE-006 | Implement role and shop authorization | 5 | Every protected merchant operation checks membership and role on the server; cross-shop access tests fail safely. |
| BE-007 | Establish database integration-test isolation | 3 | Integration tests run against isolated data and clean up deterministically. |
| BE-008 | Establish the immutable audit-event foundation | 3 | Security- and merchant-relevant mutations can record actor, shop, action, metadata, and timestamp. |

**Sprint total: 35 points**

**Sprint deliverable:** Secure identity, tenancy, schema, migrations, and reproducible test data.

## Sprint 9 - Merchant settings persistence

**Objective:** Replace merchant settings fixtures with authorized backend persistence.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| BE-009 | Implement shop profile and capacity services | 5 | Authorized owners and managers can read and update shop profile and capacity with validation and audit events. |
| BE-010 | Implement weekly hours and schedule overrides | 5 | Weekly schedules and special-date closures or hours persist and return in the UI contract. |
| BE-011 | Implement service, price, duration, and buffer persistence | 5 | Services can be created, updated, enabled, and disabled with valid monetary and duration constraints. |
| BE-012 | Implement employee and skill persistence | 5 | Employees and their supported services persist with shop-scoped authorization. |
| BE-013 | Implement staff attendance state | 5 | Authorized users can clock staff in, place them on break, and clock them out without invalid overlapping attendance. |
| BE-014 | Define API validation and error contracts | 3 | Merchant endpoints return consistent field errors, authorization errors, conflict errors, and server errors. |
| BE-015 | Connect approved merchant settings UI to backend services | 4 | The approved UI loads and saves real settings without visual regressions or direct database access from components. |
| BE-016 | Add merchant authorization integration tests | 3 | Staff, managers, owners, outsiders, and cross-shop attempts are covered for every settings area. |

**Sprint total: 35 points**

**Sprint deliverable:** Merchant configuration is persistent, authorized, audited, and connected to the approved frontend.

---

# Phase 4 - Queue engine and availability

## Sprint 10 - Core queue engine

**Objective:** Implement a transaction-safe daily queue and its complete state machine.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| QUE-001 | Implement the daily queue lifecycle | 4 | A shop can open, pause, resume, and close one queue per business date with valid transitions. |
| QUE-002 | Implement transaction-safe ticket numbering | 5 | Concurrent joins never receive duplicate sequence numbers; uniqueness is enforced by the database. |
| QUE-003 | Implement the ticket state machine | 5 | Waiting, called, arrived, serving, completed, cancelled, expired, and no-show transitions are validated centrally. |
| QUE-004 | Implement core join eligibility rules | 5 | Closed, paused, full, unavailable-service, duplicate-active-ticket, and invalid-shop attempts are rejected consistently. |
| QUE-005 | Implement merchant walk-in creation | 4 | Authorized merchant users can create valid walk-in tickets through the same queue engine. |
| QUE-006 | Implement merchant call, start, complete, cancel, and no-show commands | 5 | Commands enforce ticket state, employee qualification, attendance, and active-session constraints. |
| QUE-007 | Record immutable queue events | 3 | Every accepted and operationally important rejected command produces the required audit or queue event. |
| QUE-008 | Add queue concurrency and rollback tests | 4 | Parallel joins, duplicate commands, conflicting assignments, and failed transactions leave the queue consistent. |

**Sprint total: 35 points**

**Sprint deliverable:** A tested queue engine that is correct without relying on the UI.

## Sprint 11 - Availability, estimation, and merchant integration

**Objective:** Calculate trustworthy customer availability and connect the real queue engine to the merchant desk.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| QUE-009 | Implement waiting-capacity calculation | 4 | Remaining capacity is derived from active waiting tickets and configured shop capacity. |
| QUE-010 | Implement shop, service, and qualified-staff availability | 5 | Availability reflects hours, overrides, queue status, service state, staff attendance, skills, breaks, and active sessions. |
| QUE-011 | Implement multi-employee waiting-time simulation | 5 | Waiting tickets are simulated across qualified employees and return deterministic estimated start times. |
| QUE-012 | Implement closing-time completion cutoff | 4 | A customer cannot join when estimated service completion exceeds the shop's effective closing time. |
| QUE-013 | Define public availability reason codes | 3 | The domain returns stable reason codes and customer-safe messages for every unavailable state. |
| QUE-014 | Connect the approved merchant queue desk to the queue engine | 5 | Walk-in, call, start, complete, no-show, cancel, pause, and new-day actions use real backend commands. |
| QUE-015 | Add idempotency and optimistic-version protection | 4 | Retried and stale merchant commands cannot duplicate or incorrectly overwrite queue changes. |
| QUE-016 | Complete queue-domain unit and integration coverage | 5 | State, capacity, availability, estimation, cutoff, qualification, and conflict scenarios have automated coverage. |

**Sprint total: 35 points**

**Sprint deliverable:** The real merchant queue desk operates on a safe queue engine with calculated availability and wait estimates.

---

# Phase 5 - Public discovery and customer queue backend

## Sprint 12 - Public shop discovery

**Objective:** Replace customer discovery fixtures with public, rate-limited backend data.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| CUS-001 | Implement the public service catalog | 4 | Active service categories are returned with localized display values and stable identifiers. |
| CUS-002 | Implement public shop discovery and filtering | 5 | Customers can filter participating shops by service and receive only public, active merchant data. |
| CUS-003 | Implement the shop availability endpoint | 5 | Each shop result includes current hours, price, duration, queue metrics, estimated wait, cutoff, and availability reason. |
| CUS-004 | Connect approved customer cards to public APIs | 5 | The approved discovery UI loads real public data without visual regressions and handles loading and failure states. |
| CUS-005 | Implement location and distance-ready data contracts | 3 | Addresses and coordinates are normalized, map links work, and the API can support future distance sorting without enabling GPS tracking. |
| CUS-006 | Add safe caching and revalidation | 3 | Static shop data is cached appropriately while queue-dependent availability is never served beyond the approved freshness window. |
| CUS-007 | Add public endpoint rate limits | 4 | Discovery and availability endpoints resist abusive request volume without blocking normal pilot traffic. |
| CUS-008 | Add public-discovery end-to-end tests | 5 | Service selection, filtering, sorting, open and closed shops, unavailable reasons, and API failure states are covered. |

**Sprint total: 34 points**

**Sprint deliverable:** Customers view real shops and live calculated availability through the approved interface.

## Sprint 13 - Customer identity and queue journey

**Objective:** Connect the approved customer join and ticket experience to secure queue services.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| CUS-009 | Implement customer mobile verification | 5 | A rate-limited OTP flow verifies the customer before real remote queue creation. |
| CUS-010 | Implement secure public ticket tokens | 5 | Ticket links use high-entropy tokens stored only as hashes and expose only the ticket owner's public data. |
| CUS-011 | Implement the customer join endpoint | 5 | Verified customers can join an eligible queue exactly once through a transaction-safe, idempotent command. |
| CUS-012 | Implement the customer ticket-status endpoint | 4 | A valid public token returns the current ticket, position, estimate, shop, service, and customer-safe status. |
| CUS-013 | Implement customer arrival and cancellation commands | 4 | Valid ticket owners can confirm arrival or cancel only when the current state permits it. |
| CUS-014 | Connect the approved join and ticket UI to backend services | 5 | The approved customer workflow uses real verification, queue, status, arrival, and cancellation behavior. |
| CUS-015 | Implement initial PII and retention controls | 3 | Phone values are protected, ordinary logs exclude PII, and closed tickets receive a documented initial retention policy. |
| CUS-016 | Add complete customer-journey end-to-end tests | 4 | Verification, join, duplicate prevention, ticket access, arrival, cancellation, expiry, and unauthorized access are covered. |

**Sprint total: 35 points**

**Sprint deliverable:** A customer can securely discover a shop, join its real queue, and manage their own ticket.

---

# Phase 6 - Realtime updates and notifications

## Sprint 14 - Realtime synchronization and worker foundation

**Objective:** Keep customer and merchant screens synchronized and establish reliable asynchronous processing.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| RT-001 | Define shop and ticket realtime channel contracts | 4 | Channel authorization and payloads expose only the minimum identifiers required to trigger authoritative refetches. |
| RT-002 | Add merchant queue subscriptions | 5 | Merchant queue changes appear without manual refresh and unauthorized shops cannot be subscribed to. |
| RT-003 | Add customer ticket subscriptions | 5 | A customer sees their ticket change without receiving other customers' ticket data. |
| RT-004 | Add polling and reconnect fallback | 3 | Temporary realtime failure falls back to bounded polling and reconnects without duplicate UI updates. |
| RT-005 | Implement the transactional outbox schema and publisher | 4 | Relevant queue changes write durable events in the same transaction as the business change. |
| RT-006 | Bootstrap the standalone Node.js worker | 4 | The worker starts independently, acquires jobs safely, reports health, and shuts down gracefully. |
| RT-007 | Create the notification-provider abstraction | 5 | OTP and queue notifications can use a provider interface with test doubles and structured outcomes. |
| RT-008 | Test stale, disconnected, and reconnected clients | 5 | Automated tests demonstrate correct recovery without lost, duplicated, or cross-customer state. |

**Sprint total: 35 points**

**Sprint deliverable:** Customer and merchant views update automatically, supported by a durable worker foundation.

## Sprint 15 - Notifications and queue automation

**Objective:** Deliver timely customer messages and automate lifecycle deadlines safely.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| NTF-001 | Integrate the selected OTP provider | 5 | OTP delivery, verification, expiry, resend limits, and provider failures are handled without exposing secrets. |
| NTF-002 | Implement near-turn notifications | 4 | A customer is notified at the configured threshold once per relevant queue progression. |
| NTF-003 | Implement called and arrival-deadline notifications | 4 | Called customers receive the required deadline and do not receive duplicate messages on retries. |
| NTF-004 | Implement ticket expiry and no-show jobs | 5 | Deadlines transition eligible tickets exactly once and trigger queue recalculation. |
| NTF-005 | Implement notification retries and deduplication | 4 | Temporary failures retry with backoff; permanent failures are recorded; duplicate sends are prevented. |
| NTF-006 | Add notification consent, preferences, and delivery records | 3 | Customer consent and delivery outcome are recorded without exposing message content unnecessarily. |
| NTF-007 | Implement end-of-day processing | 4 | Open tickets, sessions, attendance, and queue-day closure follow documented end-of-day rules. |
| NTF-008 | Add worker and notification integration tests | 5 | Jobs, retries, deduplication, deadlines, failure handling, and end-of-day behavior are covered. |

**Sprint total: 34 points**

**Sprint deliverable:** Customers receive reliable queue notifications and time-based queue rules operate automatically.

---

# Phase 7 - Security, reliability, and pilot deployment

## Sprint 16 - Production hardening

**Objective:** Prepare Pila to handle real pilot customers and merchant operations safely.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| SEC-001 | Perform the authorization and tenancy review | 5 | Every API, action, channel, job, and query has a documented authorization decision and cross-tenant tests. |
| SEC-002 | Implement abuse and fake-ticket protection | 5 | IP, phone hash, shop, session, OTP, join, and cancellation limits block tested abuse patterns. |
| SEC-003 | Harden cookies, CSRF, headers, and content policy | 5 | Production sessions and state-changing requests use the agreed cookie, origin, CSRF, CSP, and security-header protections. |
| SEC-004 | Implement PII encryption and log redaction | 5 | Sensitive customer values are encrypted where required and cannot appear in normal logs, error reports, or analytics. |
| SEC-005 | Implement retention and anonymization jobs | 4 | Closed ticket PII is removed or anonymized according to the documented schedule without breaking aggregate reporting. |
| SEC-006 | Verify backup and restore procedures | 3 | Automated backups are enabled and a documented restore exercise succeeds in a non-production environment. |
| SEC-007 | Add monitoring, health checks, and error reporting | 4 | Web, database, worker, job, and provider failures are observable with actionable alerts. |
| SEC-008 | Run load, contention, and recovery tests | 4 | Expected pilot load, burst joins, worker restarts, database contention, and provider downtime meet defined thresholds. |

**Sprint total: 35 points**

**Sprint deliverable:** A security-reviewed and operationally observable pilot candidate.

## Sprint 17 - Pilot deployment and release readiness

**Objective:** Deploy the pilot, onboard merchants, and complete operational readiness.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| OPS-001 | Provision staging and production environments | 5 | Environments have separate secrets, databases, storage, domains, and access controls. |
| OPS-002 | Implement automated deployment and migration workflow | 5 | Approved changes deploy predictably with safe migrations and a documented rollback path. |
| OPS-003 | Configure production dashboards and alerts | 4 | Queue failures, latency, job backlog, notification failures, authentication abuse, and uptime have useful thresholds. |
| OPS-004 | Build merchant onboarding and invitation workflow | 4 | A pilot merchant can be created, invited, assigned roles, and guided through initial configuration. |
| OPS-005 | Produce shop QR codes and customer instructions | 3 | Each pilot shop has a tested customer entry link, printable QR code, and concise bilingual instructions. |
| OPS-006 | Implement pilot analytics and wait-accuracy reporting | 5 | Joins, arrivals, cancellations, no-shows, completions, estimate error, and merchant usage are measurable without exposing PII. |
| OPS-007 | Create support, incident, and recovery runbooks | 4 | Staff can respond to queue errors, account issues, notification outages, bad data, and rollback scenarios. |
| OPS-008 | Complete release regression and user acceptance testing | 5 | Critical customer and merchant workflows pass in production-like conditions and pilot blockers are resolved. |

**Sprint total: 35 points**

**Sprint deliverable:** A deployed production pilot that is ready for controlled merchant and customer use.

---

# Phase 8 - Controlled pilot and learning

## Sprint 18 - Pilot launch week

**Objective:** Launch with a small merchant group, monitor real use, and protect operational reliability.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| PIL-001 | Onboard the first pilot merchants | 5 | Three to five shops have verified configuration, users, services, employees, hours, capacity, and QR materials. |
| PIL-002 | Capture the pilot baseline | 3 | Pre-launch queue process, approximate waits, customer volume, and current merchant pain points are documented. |
| PIL-003 | Train merchant owners and staff | 3 | Staff can add walk-ins, call, start, complete, cancel, no-show, pause, and recover from common mistakes. |
| PIL-004 | Operate launch-week support and monitoring | 5 | Issues are triaged within the agreed response window and critical incidents have owners and timelines. |
| PIL-005 | Run structured defect triage | 4 | Pilot findings are classified by severity, recurrence, affected workflow, workaround, and target sprint. |
| PIL-006 | Review wait-estimate accuracy daily | 4 | Estimate error is measured by shop, service, employee coverage, queue size, and time of day. |
| PIL-007 | Collect customer feedback | 3 | Customers are asked consistent questions about clarity, trust, arrival, notification, and reuse intention. |
| PIL-008 | Collect merchant feedback | 4 | Owners and staff are interviewed about workload, missed actions, accuracy, customer behavior, and willingness to continue. |

**Sprint total: 31 points**

**Sprint deliverable:** A monitored live pilot with evidence about operational fit, queue accuracy, and user trust.

## Sprint 19 - Pilot stabilization and decision

**Objective:** Resolve the most important pilot findings and make an evidence-based continuation decision.

| ID | Feature | Points | Acceptance criteria |
|---|---|---:|---|
| PIL-009 | Resolve critical and high-priority pilot defects | 5 | Accepted blockers and severe defects have verified fixes or documented product decisions. |
| PIL-010 | Tune the wait-estimation model | 5 | Approved adjustments reduce measured estimate error without introducing unfair queue ordering. |
| PIL-011 | Improve merchant queue workflows | 5 | High-frequency merchant friction is reduced and the revised flow passes staff retesting. |
| PIL-012 | Tune notification timing and wording | 4 | Message timing and copy reflect observed arrival behavior and reduce confusion or unnecessary sends. |
| PIL-013 | Improve reliability from pilot incidents | 4 | Recurring failure modes have monitoring, prevention, retry, fallback, or documented recovery. |
| PIL-014 | Produce the pilot metrics report | 4 | The report covers usage, arrival, no-show, completion, retention, wait accuracy, reliability, and support demand. |
| PIL-015 | Conduct merchant pricing interviews | 3 | Pilot merchants respond to a consistent pricing and willingness-to-pay discussion without being charged automatically. |
| PIL-016 | Complete the go, revise, narrow, or pause review | 5 | The product team records an evidence-based decision, reasons, risks, and the next approved roadmap. |

**Sprint total: 35 points**

**Sprint deliverable:** A stabilized pilot and a formal decision on Pila's next stage.

---

# Release checkpoints

## Checkpoint A - Boilerplate complete

Reached after Sprint 1.

- The repository builds, tests, and deploys.
- Development standards and project boundaries are established.

## Checkpoint B - Proof-of-concept frontend complete

Reached after Sprint 7.

- Customer and merchant workflows match the reference using mock data.
- Exact theme tokens are approved.
- Responsive, accessibility, localization, and visual checks pass.
- Backend implementation is now permitted.

## Checkpoint C - Merchant backend alpha

Reached after Sprint 11.

- Merchant settings persist.
- The real queue engine is safe under concurrency.
- Merchant queue operations use calculated availability and wait estimates.

## Checkpoint D - End-to-end customer alpha

Reached after Sprint 13.

- Customers can discover real shops, verify identity, join, view, arrive, and cancel.

## Checkpoint E - Pilot release candidate

Reached after Sprint 17.

- Realtime updates, notifications, privacy, security, monitoring, deployment, onboarding, and runbooks are complete.

## Checkpoint F - Pilot decision

Reached after Sprint 19.

- Live evidence supports a go, revise, narrow, or pause decision.

---

# Blueprint totals

| Phase | Sprints | Planned points |
|---|---:|---:|
| Phase 1 - Boilerplate | 1 | 34 |
| Phase 2 - Reproduce the proof of concept | 6 | 206 |
| Phase 3 - Database, authentication, and merchant persistence | 2 | 70 |
| Phase 4 - Queue engine and availability | 2 | 70 |
| Phase 5 - Public discovery and customer queue backend | 2 | 69 |
| Phase 6 - Realtime updates and notifications | 2 | 69 |
| Phase 7 - Security, reliability, and pilot deployment | 2 | 70 |
| Phase 8 - Controlled pilot and learning | 2 | 66 |
| **Total** | **19 sprints** | **654 points** |

The point total is a planning baseline, not a commitment to fixed scope. After every phase gate, remaining estimates should be reviewed using what the team has learned.

## Change-control rule

This blueprint should be updated before execution whenever a feature is added, removed, split, merged, or re-estimated. The sprint total must always remain at or below 35 points, and the frontend sign-off gate must remain intact unless the product owner explicitly changes the delivery strategy.
