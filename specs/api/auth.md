# Authentication API

## Overview
This API handles user authentication and identity.

## Endpoints

### POST /auth/signup
Create a new user account.

Request:
- email
- password
- name (optional)

Response:
- user_id
- access_token

---

### POST /auth/login
Authenticate an existing user.

Request:
- email
- password

Response:
- access_token

---

### GET /auth/me
Return the authenticated user's profile.

Authorization:
- Bearer token required

Response:
- id
- email
- name
