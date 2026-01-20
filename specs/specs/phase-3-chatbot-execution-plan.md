# Phase III: AI Chatbot Execution Plan

## Objective
Extend the Todo system with an AI-powered chatbot that allows users to
manage tasks using natural language.

The chatbot must interact with the existing backend exclusively via APIs
and must not bypass authentication or business logic.

---

## Core Principles

- Chatbot is an interface, not a new backend
- All actions go through existing APIs
- No direct database access
- User context is mandatory

---

## Phase 3.1: Chatbot Architecture

### Task 3.1.1 – MCP Server Setup
- Initialize MCP server project
- Configure protocol handlers
- Enable tool invocation support

### Task 3.1.2 – Authentication Context
- Accept JWT token from frontend
- Validate user identity
- Inject user_id into all chatbot actions

---

## Phase 3.2: Intent & Command Mapping

### Task 3.2.1 – Intent Definitions
Define supported intents:
- create_task
- update_task
- delete_task
- complete_task
- list_tasks
- search_tasks
- set_due_date
- set_recurrence
- set_reminder

### Task 3.2.2 – Natural Language Examples

| User Input | Intent |
|-----------|-------|
| “Add buy milk” | create_task |
| “Mark task 3 done” | complete_task |
| “What’s due today?” | list_tasks |
| “Remind me tomorrow at 9am” | set_reminder |

---

## Phase 3.3: Tool Definitions (MCP)

### Task 3.3.1 – Task Tools

Each tool maps 1:1 to backend APIs.

Example:
- `create_task(title, description)`
- `update_task(task_id, fields)`
- `list_tasks(filters)`
- `delete_task(task_id)`

### Task 3.3.2 – Validation Rules
- Tool inputs must be validated
- Missing parameters must trigger clarification
- Invalid task IDs must return safe errors

---

## Phase 3.4: Conversation Flow

### Task 3.4.1 – Single-Step Commands
Execute immediately if intent is clear.

Example:
> “Add finish report”

### Task 3.4.2 – Multi-Step Clarification
If required info is missing:
- Ask a follow-up question
- Do not assume values

Example:
> “When should I remind you?”

---

## Phase 3.5: Context Handling

### Task 3.5.1 – Short-Term Context
- Track last referenced task
- Track last used filters

### Task 3.5.2 – Safety Boundaries
- Context expires after session
- No cross-user data access

---

## Phase 3.6: Chat UI Integration

### Task 3.6.1 – Frontend Chat UI
- Chat panel in dashboard
- Message history view
- Loading & error states

### Task 3.6.2 – API Gateway
- Chat UI sends messages to MCP server
- MCP server invokes backend APIs

---

## Phase 3.7: Error Handling

### Task 3.7.1 – User-Friendly Errors
- Convert API errors into natural language

Example:
> “I couldn’t find that task.”

### Task 3.7.2 – Fail-Safe Behavior
- Never execute partial actions
- Ask before destructive actions

---

## Phase 3.8: Security & Permissions

### Task 3.8.1 – Authorization Enforcement
- Validate JWT on every request
- Scope actions to user_id

### Task 3.8.2 – Rate Limiting
- Prevent abuse
- Throttle repeated actions

---

## Phase 3.9: Deployment

### Task 3.9.1 – MCP Server Deployment
- Deploy as separate service
- Secure environment variables

### Task 3.9.2 – Integration Testing
- Verify chatbot actions reflect in UI
- Verify API audit logs

---

## Phase 3.10: Verification

### Task 3.10.1 – Intent Accuracy
- Test common phrases
- Test ambiguous commands

### Task 3.10.2 – End-to-End Tests
- Chat → API → DB → UI

---

## Completion Criteria

Phase III is complete when:
- Users can manage tasks fully via chat
- No chatbot action bypasses APIs
- All security rules remain enforced
- System remains deterministic

---

## Non-Goals

- Free-form conversations
- Emotional companionship
- Unrestricted system access
