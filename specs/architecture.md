# System Architecture

## Overview
The system is a multi-user, full-stack Todo application with authentication,
persistent storage, and automation features.

The architecture follows a service-oriented design with a clear separation
between frontend, backend API, database, and background workers.

---

## High-Level Architecture

Frontend (Next.js)
    ↓ HTTPS (REST)
Backend API (FastAPI)
    ↓ ORM
Database (PostgreSQL)
    ↓ Events / Jobs
Background Workers (Scheduler / Automation)

---

## Technology Stack

### Frontend
- Next.js (App Router)
- TypeScript
- Tailwind CSS
- Authentication via Better Auth

### Backend
- Python FastAPI
- SQLModel ORM
- JWT-based authentication
- RESTful API

### Database
- PostgreSQL (Neon Serverless)
- UUID primary keys
- Indexed foreign keys

### Authentication
- Better Auth for user signup/signin
- JWT access tokens
- Auth middleware on protected routes

### Automation
- Background worker for:
  - recurring tasks
  - due date reminders
- Time-based scheduler (cron-style or async loop)

---

## Data Flow

### User Request Flow
1. User interacts with the frontend UI.
2. Frontend sends authenticated HTTP requests.
3. Backend validates JWT token.
4. Backend performs business logic.
5. Database persists data.
6. Backend returns response to frontend.

---

## Authentication Flow

1. User signs up or logs in.
2. Backend issues JWT access token.
3. Token is stored securely on the frontend.
4. Token is sent in `Authorization: Bearer` header.
5. Backend middleware validates the token.
6. Request proceeds to protected endpoints.

---

## Backend Responsibilities

- Validate user authentication
- Enforce user-level data isolation
- Expose REST APIs for tasks, tags, reminders
- Execute business rules:
  - completion logic
  - recurrence generation
  - reminder scheduling

---

## Database Design Principles

- Each task belongs to exactly one user
- Tags use a many-to-many relationship
- Reminders are separate entities
- Soft constraints enforced at the application layer

---

## Background Jobs

### Recurring Task Processor
- Runs at scheduled intervals
- Detects completed recurring tasks
- Generates the next task instance

### Reminder Dispatcher
- Checks for upcoming reminders
- Marks reminders as sent
- Triggers notifications

---

## Frontend Responsibilities

- User authentication UI
- Task management interface
- Search, filter, and sort controls
- Notification permissions handling

---

## Error Handling Strategy

- Validation errors return 400
- Authentication errors return 401
- Authorization errors return 403
- Not-found errors return 404
- Server errors return 500

---

## Scalability Considerations

- Stateless backend services
- Database indexes on:
  - user_id
  - due_date
  - completed
- Background jobs isolated from request lifecycle

---

## Security Considerations

- Passwords are never stored in plaintext
- JWT tokens have expiration times
- All task operations are user-scoped
- HTTPS enforced in production

---

## Non-Goals

- Real-time collaboration
- Offline-first support
- External calendar integrations

---

## Future Extensions

- AI chatbot interface (MCP server)
- Push notifications
- Shared task lists
- Role-based access control

