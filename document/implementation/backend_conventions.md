# Backend Coding Conventions

## 1. Folder and File Naming

- **Modules:** kebab-case (e.g., `user-management`).
- **Controllers, Services, Resolvers:** Use NestJS CLI conventions (`.controller.ts`, `.service.ts`, `.resolver.ts`).
- **Entities & DTOs:** PascalCase (e.g., `User.entity.ts`, `CreateUser.dto.ts`).
- **Interfaces:** PascalCase, prefixed with `I` (e.g., `IUserService.ts`).
- **Configuration:** camelCase (e.g., `database.config.ts`).
- **Folders:** kebab-case.

## 2. Module and Service Structure

- **Props & DTOs:** Use TypeScript classes for DTOs to leverage decorators for validation. Use interfaces for internal-only type definitions.
- **Dependency Injection:** Use NestJS's built-in DI container. Services should be injected into controllers/resolvers.
- **Error Handling:** All business logic errors must be raised using custom exceptions derived from `APIException` (defined in `app.core.exceptions`). These exceptions are automatically handled and formatted by the global exception handlers.
- **Imports:** Order imports as follows: Python built-ins, external libraries, internal modules, services, entities, DTOs, types.

## 3. Database and Entities

- **Entities:** Use a repository pattern for data access. Define entities with appropriate decorators if using an ORM like TypeORM or Prisma.
- **Migrations:** Use a migration tool to manage database schema changes. Each migration should be atomic and reversible.
- **Transactions:** Use transactions for operations that involve multiple database writes to ensure data integrity.

## 4. API Design

- **RESTful Principles:** Adhere to RESTful principles for API design. Use appropriate HTTP verbs (GET, POST, PUT, DELETE) and status codes.
- **Response Standardization:** All successful API responses must use the `GeneralResponse` schema (or `SuccessResponse` derived from it) defined in `app.domain.general_schema`. The response should include `status: "success"`, a descriptive `message`, and the actual payload in the `data` field.
- **Error Documentation:** All API endpoints must explicitly document potential error responses (e.g., 401, 404, 409) using the `responses` parameter in the FastAPI route decorator, referencing the `ErrorResponse` schema.
- **Versioning:** Version APIs to avoid breaking changes for clients (e.g., `/api/v1/...`).
- **Validation:** Use Pydantic models (DTOs/Schemas) for request and response bodies, leveraging FastAPI's automatic validation and serialization.

## 5. TypeScript

- **Strict Mode:** Enable `strict` mode in `tsconfig.json`.
- **Typings:** Provide explicit types for all function arguments, return values, and variables. Avoid `any`.
- **Interfaces vs. Classes:** Use interfaces for defining contracts and public APIs. Use classes for DTOs and entities.

## 6. Linting and Formatting

- **ESLint & Prettier:** Adhere to the rules defined in the project's ESLint and Prettier configurations.
- **CI/CD:** Integrate linting, formatting, and testing checks into the CI/CD pipeline.