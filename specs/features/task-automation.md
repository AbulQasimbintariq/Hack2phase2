# Task Automation

## Overview
This feature defines time-based and recurring task automation.

## Fields
Task includes:
- is_recurring
- recurrence_type (daily, weekly, monthly)
- recurrence_interval
- due_date

Reminder includes:
- remind_at
- sent

## Capabilities

### Set Due Dates
Users must be able to assign a due date and time to tasks.

### Recurring Tasks
The system must allow tasks to repeat on a defined schedule.

When a recurring task is completed:
A new task must be automatically created using the recurrence rules.

### Reminders
The system must trigger reminders before a task is due.

The reminder must be delivered via:
- Web notifications
- Chatbot alerts
