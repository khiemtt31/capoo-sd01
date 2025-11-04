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
- **Error Handling:** Use standard NestJS exceptions (`HttpException`, `NotFoundException`, etc.). Create custom exceptions for specific business logic errors.
- **Imports:** Order imports as follows: Node.js built-ins, external libraries, internal modules, services, entities, DTOs, types.

## 3. Database and Entities

- **Entities:** Use a repository pattern for data access. Define entities with appropriate decorators if using an ORM like TypeORM or Prisma.
- **Migrations:** Use a migration tool to manage database schema changes. Each migration should be atomic and reversible.
- **Transactions:** Use transactions for operations that involve multiple database writes to ensure data integrity.

## 4. API Design

- **RESTful Principles:** Adhere to RESTful principles for API design. Use appropriate HTTP verbs (GET, POST, PUT, DELETE) and status codes.
- **Versioning:** Version APIs to avoid breaking changes for clients (e.g., `/api/v1/...`).
- **Validation:** Use validation pipes with DTOs to validate incoming request bodies.

## 5. TypeScript

- **Strict Mode:** Enable `strict` mode in `tsconfig.json`.
- **Typings:** Provide explicit types for all function arguments, return values, and variables. Avoid `any`.
- **Interfaces vs. Classes:** Use interfaces for defining contracts and public APIs. Use classes for DTOs and entities.

## 6. Linting and Formatting

- **ESLint & Prettier:** Adhere to the rules defined in the project's ESLint and Prettier configurations.
- **CI/CD:** Integrate linting, formatting, and testing checks into the CI/CD pipeline.