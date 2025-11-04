# Frontend Coding Conventions

## 1. Folder and File Naming

- **Components:** PascalCase (e.g., `UserProfile.tsx`).
- **Pages & Layouts:** kebab-case (e.g., `user-profile.tsx`).
- **Hooks:** camelCase with `use` prefix (e.g., `useUserData.ts`).
- **Services & Utilities:** camelCase (e.g., `apiClient.ts`, `dateUtils.ts`).
- **Styles:** kebab-case (e.g., `user-profile.module.css`).
- **Folders:** kebab-case (e.g., `user-profile`).

## 2. Component Structure

- **Props:** Use TypeScript interfaces for prop types, prefixed with `I` (e.g., `IUserProfileProps`).
- **State Management:** Prefer React Hooks (`useState`, `useReducer`). For complex global state, use Zustand or a similar lightweight library.
- **Styling:** Use CSS Modules for component-scoped styles. Global styles should be minimal and reside in `app/globals.css`.
- **Imports:** Order imports as follows: React, external libraries, internal components, hooks, services, types, styles.

## 3. State Management

- **Local State:** Use `useState` for simple component state.
- **Complex Local State:** Use `useReducer` for components with complex state logic.
- **Global State:** Use Zustand for minimal, hook-based global state management. Avoid Redux unless the application's complexity justifies it.

## 4. Data Fetching

- **API Client:** Use a centralized API client (e.g., using `fetch` or `axios`) for all HTTP requests.
- **Hooks:** Create custom hooks for data fetching logic (e.g., `useFetchProjects`).
- **State:** Use a library like React Query (TanStack Query) to manage caching, refetching, and server state.

## 5. TypeScript

- **Strict Mode:** Enable `strict` mode in `tsconfig.json`.
- **Typings:** Provide explicit types for all function arguments, return values, and variables. Avoid `any` where possible.
- **Interfaces vs. Types:** Use interfaces for object shapes and types for unions, intersections, or primitives.

## 6. Linting and Formatting

- **ESLint:** Adhere to the rules defined in `.eslintrc.mjs`.
- **Prettier:** Use a code formatter to ensure consistent styling across the codebase.
- **CI/CD:** Integrate linting and formatting checks into the CI/CD pipeline.