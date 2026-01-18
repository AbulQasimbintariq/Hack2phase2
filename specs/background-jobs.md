# Background Jobs & Workers

## Overview
This specification defines background processes responsible for automation,
time-based execution, and non-blocking system tasks.

Background jobs must run independently of HTTP request/response cycles.

---

## Responsibilities

- Process recurring tasks
- Dispatch reminders
- Maintain task automation integrity
- Avoid duplicate executions

---

## Execution Model

- Jobs run on a fixed schedule (cron-style)
- Jobs execute asynchronously
- Jobs are idempotent
- Jobs are isolated from user-facing APIs

---

## Job 1: Recurring Task Processor

### Purpose
Automatically generate new task instances for recurring tasks.

### Schedule
- Runs every 5 minutes

### Input Data
- Tasks where:
  - is_recurring = true
  - completed = true
  - due_date IS NOT NULL

### Logic
1. Fetch eligible recurring tasks
2. Calculate next due date based on:
   - recurrence_type
   - recurrence_interval
3. Create a new task instance
4. Reset completed status
5. Preserve metadata:
   - title
   - description
   - priority
   - tags

### Safety Rules
- A task must not be regenerated more than once
- Store last_processed_at timestamp
- Skip tasks already processed

---

## Job 2: Reminder Dispatcher

### Purpose
Send notifications for upcoming task deadlines.

### Schedule
- Runs every 1 minute

### Input Data
- Reminders where:
  - sent = false
  - remind_at <= NOW()

### Logic
1. Fetch pending reminders
2. Send notification
3. Mark reminder as sent
4. Log delivery timestamp

### Delivery Channels
- Web notifications
- Chatbot alerts

---

## Job 3: Overdue Task Scanner (Optional)

### Purpose
Detect overdue tasks for UX highlighting.

### Schedule
- Runs every 15 minutes

### Input Data
- Tasks where:
  - completed = false
  - due_date < NOW()

### Output
- Update task status to overdue
- Trigger optional notifications

---

## Concurrency Rules

- Jobs must use database-level locking
- Prevent parallel execution conflicts
- Use transaction boundaries

---

## Failure Handling

- Jobs must retry safely
- Partial failures must not corrupt data
- Errors must be logged with context

---

## Observability

- Log job start/end times
- Log affected entity IDs
- Record failures and retries

---

## Configuration

- Job schedules configurable via environment variables
- Enable/disable jobs independently

---

## Non-Goals

- Real-time scheduling per user
- External message queues
- Heavy workflow orchestration

---

## Future Extensions

- Distributed workers
- Retry backoff strategies
- External notification providers
