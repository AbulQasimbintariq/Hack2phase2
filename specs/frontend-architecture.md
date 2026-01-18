# Frontend Architecture

## Overview
The frontend is a responsive web application built with Next.js using the App Router.
It communicates with the backend exclusively via REST APIs and handles authentication,
state management, and UI rendering.

---

## Technology Stack

- Next.js (App Router)
- TypeScript
- Tailwind CSS
- Better Auth (client SDK)
- Fetch API / Server Actions

---

## Folder Structure

app/
├── layout.tsx              # Root layout
├── page.tsx                # Landing page
├── auth/
│   ├── login/
│   │   └── page.tsx
│   ├── signup/
│   │   └── page.tsx
│
├── dashboard/
│   ├── layout.tsx          # Protected layout
│   ├── page.tsx            # Task list
│   ├── loading.tsx
│   ├── error.tsx
│
├── tasks/
│   └── [id]/
│       └── page.tsx        # Task details
│
├── api/                    # Next.js route handlers (optional)
│   └── auth/
│
components/
├── ui/                     # Reusable UI primitives
├── TaskCard.tsx
├── TaskList.tsx
├── TaskForm.tsx
├── FilterBar.tsx
├── SortMenu.tsx
│
lib/
├── api.ts                  # API client wrapper
├── auth.ts                 # Auth helpers
├── types.ts                # Shared types
│
hooks/
├── useTasks.ts
├── useAuth.ts
│
styles/
└── globals.css
