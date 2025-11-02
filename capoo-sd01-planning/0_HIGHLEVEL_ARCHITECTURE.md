# High-Level Architecture

## 1. Overview

This document outlines the high-level architecture for the Roo Code Project Management Application. The design follows a service-oriented approach to ensure scalability, maintainability, and a clear separation of concerns. The architecture is composed of distinct services, each responsible for a specific business domain.

## 2. Architectural Style

A **Microservices Architecture** is proposed. This style decouples the core functionalities of the application—user management, project tracking, notifications, and tagging—into independently deployable services. Communication between the client and the services will be managed via an API Gateway for brief. (Recommended but not considered ultimately follow)

## 3. Core Components

The system is composed of the following key components:

*   **Web Client (Frontend):** A Single-Page Application (SPA) that provides the user interface. It communicates with the backend services via the API Gateway (using Nextjs 16 latest in Sep 2025).
*   **API Gateway:** The single entry point for all client requests. It routes traffic to the appropriate backend service, handling concerns like authentication and rate limiting (Honojs latest of Sep 2025).
*   **User Service:** Manages all user-related concerns, including registration, login, profile management, roles, and permissions. It is the authority on user identity.
*   **Project Service:** The core service for managing projects, tasks, and assignments. It handles all business logic related to project and task lifecycles. (This is the most complicated Service as Project management requires lots of tracking and relates to all entity in the database so this must be carefully plan / code / improve)
*   **Notification Service:** Responsible for generating and dispatching in-app and email notifications based on events occurring in other services (e.g., a new task assignment).
*   **Tagging Service:** Manages the creation, assignment, and filtering of tags for tasks and other resources. (includes comment)

## 4. Data Storage

Each service will have its own dedicated database to ensure loose coupling.

*   **User Service DB (PostgreSQL):** Stores user credentials, profiles, and role information.
*   **Project Service DB (PostgreSQL):** Stores project, task, and assignment data.
*   **Tagging Service DB (PostgreSQL):** Stores tag definitions and their associations with tasks.
*   **Notification Service DB (PostgreSQL):** Stores notification templates and logs.

Using a relational database like **PostgreSQL** is recommended for its reliability and support for structured data.

## 5. Technology Stack (Proposed)

| Layer     | Technology            | Notes                                          |
| :-------- | :-------------------- | :--------------------------------------------- |
| Frontend  | React.js / Next.js    | For building a dynamic and responsive UI.      |
| Backend   | Node.js (NestJS)      | For building efficient and scalable services.  |
| Database  | PostgreSQL            | For reliable and structured data storage.      |
| API Style | RESTful APIs          | For standardized client-server communication.  |
| Messaging | RabbitMQ / Kafka      | For asynchronous communication between services. |

## 6. System Architecture Diagram

```mermaid
graph TD
    subgraph "Client"
        A[Web Client / Browser]
    end

    subgraph "Backend Services"
        B(API Gateway)
        C[User Service]
        D[Project Service]
        E[Notification Service]
        F[Tagging Service]
    end

    subgraph "Data Stores"
        G[(User DB)]
        H[(Project DB)]
        I[(Notification DB)]
        J[(Tagging DB)]
    end

    subgraph "Message Bus"
        K{Event Bus}
    end

    A --> B

    B --> C
    B --> D
    B --> E
    B --> F

    C --- G
    D --- H
    E --- I
    F --- J

    D -- "Task Assigned Event" --> K
    K -- " " --> E
