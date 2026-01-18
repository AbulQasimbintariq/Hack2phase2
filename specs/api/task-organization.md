# Task Organization API

## Overview
This API provides advanced querying and organization features.

Authorization:
- All endpoints require authentication

## Endpoints

### GET /tasks/search
Search tasks by keyword.

Query Params:
- q (search term)

Response:
- list of matching tasks

---

### GET /tasks/filter
Filter tasks by attributes.

Query Params:
- completed
- priority (low, medium, high)
- tag
- due_before
- due_after

Response:
- filtered task list

---

### GET /tasks/sort
Sort tasks.

Query Params:
- by (due_date | priority | title)
- order (asc | desc)

Response:
- sorted task list
