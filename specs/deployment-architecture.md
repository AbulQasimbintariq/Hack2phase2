# Deployment Architecture

## Overview
The system is deployed as a cloud-native application using managed services.
The frontend, backend API, database, and background workers are deployed as
independent but coordinated components.

---

## Deployment Stack

### Frontend
- Platform: Vercel
- Framework: Next.js (App Router)
- Deployment Type: Serverless + Edge

### Backend API
- Platform: Vercel Serverless Functions
- Framework: FastAPI (ASGI)
- Runtime: Python

### Database
- Platform: Neon
- Type: Serverless PostgreSQL
- Connection: Pooled + non-pooled modes

### Background Workers
- Platform: Vercel Cron + Serverless Functions
- Execution: Scheduled HTTP triggers

---

## High-Level Deployment Diagram

User Browser
   ↓
Vercel Edge (Next.js)
   ↓
Vercel Serverless API (FastAPI)
   ↓
Neon PostgreSQL
   ↑
Vercel Cron Jobs (Workers)

---

## Environment Configuration

### Required Environment Variables

Frontend (Vercel):
- NEXT_PUBLIC_API_URL
- NEXT_PUBLIC_AUTH_PROVIDER

Backend (Vercel):
- DATABASE_URL
- JWT_SECRET
- AUTH_SECRET

Workers:
- DATABASE_URL
- WORKER_SECRET
- CRON_SIGNATURE

---

## Frontend Deployment

- Deployed via GitHub → Vercel integration
- Automatic preview deployments for PRs
- Production build uses server components by default
- Auth redirects handled at edge level

---

## Backend API Deployment

- Each FastAPI route runs as a serverless function
- Stateless execution model
- Cold-start tolerant
- Auth middleware executes per request

---

## Database Deployment (Neon)

- Separate branches for:
  - development
  - staging
  - production
- Migrations executed per environment
- Connection pooling enabled for serverless
- SSL enforced

---

## Background Workers Deployment

### Worker Model
- Implemented as FastAPI routes or standalone functions
- Triggered by Vercel Cron schedules

### Example Jobs
- `/cron/recurring-tasks`
- `/cron/reminder-dispatcher`

### Security
- Cron endpoints protected via secret headers
- Requests rejected if signature is invalid

---

## Scheduling Strategy

| Job | Frequency |
|----|-----------|
| Recurring task processor | Every 5 minutes |
| Reminder dispatcher | Every 1 minute |
| Overdue scanner | Every 15 minutes |

Schedules configured via `vercel.json`.

---

## Deployment Configuration (`vercel.json`)

```json
{
  "crons": [
    {
      "path": "/api/cron/recurring-tasks",
      "schedule": "*/5 * * * *"
    },
    {
      "path": "/api/cron/reminder-dispatcher",
      "schedule": "* * * * *"
    }
  ]
}