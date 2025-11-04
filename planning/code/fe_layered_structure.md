# Frontend Layered Architecture

This document outlines the layered architecture for the Next.js frontend application, designed to promote separation of concerns, scalability, and maintainability.

## 1. Directory Structure Overview

```
apps/frontend/
├── app/
│   ├── (features)/
│   │   └── [feature-name]/
│   │       ├── page.tsx
│   │       └── layout.tsx
│   ├── globals.css
│   └── layout.tsx
├── components/
│   ├── common/
│   └── ui/
├── core/
│   ├── guards/
│   └── interceptors/
├── features/
│   └── [feature-name]/
│       ├── components/
│       ├── hooks/
│       └── services/
├── hooks/
├── lib/
├── services/
├── styles/
├── types/
└── utils/
```

## 2. Layer Descriptions

### `app/`

- **Purpose:** Contains all routes, layouts, and pages as per the Next.js App Router convention.
- **`(features)`:** A route group for feature-specific pages, keeping the `app` directory clean.

### `components/`

- **Purpose:** Shared, reusable components across the application.
- **`common/`:** Components that are used in multiple features but are not generic enough to be in `ui/` (e.g., `UserProfileCard`).
- **`ui/`:** Generic, reusable UI components like `Button`, `Input`, `Modal`, etc.

### `core/`

- **Purpose:** Core application logic, such as authentication guards and API interceptors.
- **`guards/`:** Components or hooks that protect routes based on authentication or authorization status.
- **`interceptors/`:** Logic to intercept API requests and responses for handling authentication tokens, errors, etc.

### `features/`

- **Purpose:** Feature-specific modules, each containing its own components, hooks, and services.
- **`[feature-name]/`:** A dedicated folder for each feature (e.g., `project-tracking`, `user-management`).
  - **`components/`:** Components that are specific to this feature.
  - **`hooks/`:** Hooks that are specific to this feature.
  - **`services/`:** Services and API calls related to this feature.

### `hooks/`

- **Purpose:** Global, reusable hooks that can be used across multiple features (e.g., `useLocalStorage`).

### `lib/`

- **Purpose:** Third-party library configurations and instances (e.g., `axios`, `zod`).

### `services/`

- **Purpose:** Global API services and data-fetching logic that is not specific to a single feature.

### `styles/`

- **Purpose:** Global styles, theme configurations, and utility classes.

### `types/`

- **Purpose:** Global TypeScript types and interfaces.

### `utils/`

- **Purpose:** Utility functions that can be used throughout the application (e.g., `formatDate`, `cn`).