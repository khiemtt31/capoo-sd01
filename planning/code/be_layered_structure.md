# Backend Layered Architecture (NestJS)

This document outlines the layered architecture for the NestJS backend application, designed to align with the microservices-oriented strategy and promote a clean, scalable, and maintainable codebase.

## 1. Directory Structure Overview

```
apps/backend/
├── src/
│   ├── main.ts
│   ├── app.module.ts
│   ├── core/
│   │   ├── guards/
│   │   ├── interceptors/
│   │   └── middleware/
│   ├── features/
│   │   └── [feature-name]/
│   │       ├── [feature-name].module.ts
│   │       ├── [feature-name].controller.ts
│   │       ├── [feature-name].service.ts
│   │       ├── entities/
│   │       └── dto/
│   ├── shared/
│   │   ├── config/
│   │   ├── constants/
│   │   ├── decorators/
│   │   └── utils/
│   └── types/
└── test/
```

## 2. Layer Descriptions

### `src/`

- **Purpose:** The main application source code.
- **`main.ts`:** The application entry point, responsible for bootstrapping the NestJS application.
- **`app.module.ts`:** The root module of the application.

### `core/`

- **Purpose:** Core application logic that is shared across all features.
- **`guards/`:** Authentication and authorization guards (e.g., `JwtAuthGuard`, `RolesGuard`).
- **`interceptors/`:** Request/response interceptors (e.g., for logging, transforming responses).
- **`middleware/`:** Custom middleware functions.

### `features/`

- **Purpose:** Contains all business-logic-related modules, each corresponding to a specific domain or feature (e.g., `user-management`, `project-tracking`).
- **`[feature-name]/`:** A dedicated folder for each feature module.
  - **`[feature-name].module.ts`:** The module definition file, encapsulating all related components.
  - **`[feature-name].controller.ts`:** Handles incoming requests and delegates to the service layer.
  - **`[feature-name].service.ts`:** Contains the business logic for the feature.
  - **`entities/`:** Database entities or models related to the feature.
  - **`dto/`:** Data Transfer Objects for request and response validation and typing.

### `shared/`

- **Purpose:** Shared utilities, configuration, and other code that is not specific to any single feature.
- **`config/`:** Application configuration (e.g., database, JWT, environment variables).
- **`constants/`:** Application-wide constants.
- **`decorators/`:** Custom decorators.
- **`utils/`:** Utility functions.

### `types/`

- **Purpose:** Global TypeScript types and interfaces.

### `test/`

- **Purpose:** Contains all end-to-end and integration tests. Unit tests should be co-located with the files they are testing.