# Task API

## Overview
This API manages core task operations.

Authorization:
- All endpoints require authentication

## Endpoints

### POST /tasks
Create a new task.

Request:
- title
- description (optional)

Response:
- task object

---

### GET /tasks
Retrieve all tasks for the authenticated user.

Query Params (optional):
- completed (true/false)

Response:
- list of tasks

---

### GET /tasks/{task_id}
Retrieve a single task.

Response:
- task object

---

### PUT /tasks/{task_id}
Update an existing task.

Request:
- title (optional)
- description (optional)
- completed (optional)

Response:
- updated task

---

### DELETE /tasks/{task_id}
Delete a task.

Response:
- success message
