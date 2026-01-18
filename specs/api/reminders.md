# Reminder & Automation API

## Overview
This API handles due dates, recurring tasks, and reminders.

Authorization:
- All endpoints require authentication

## Endpoints

### POST /tasks/{task_id}/due-date
Assign a due date to a task.

Request:
- due_date (ISO timestamp)

Response:
- updated task

---

### POST /tasks/{task_id}/recurrence
Configure task recurrence.

Request:
- recurrence_type (daily, weekly, monthly)
- recurrence_interval

Response:
- updated task

---

### POST /tasks/{task_id}/reminders
Create a reminder for a task.

Request:
- remind_at (ISO timestamp)

Response:
- reminder object

---

### GET /reminders/pending
Return all pending reminders for the user.

Response:
- list of reminders
