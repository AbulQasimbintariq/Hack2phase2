# Full-Stack Todo Application

A complete multi-user Todo application with FastAPI backend, Next.js frontend, PostgreSQL database, and background automation jobs.

## Features

- **Task Management**: Create, read, update, and delete tasks
- **User Authentication**: JWT-based secure signup and login
- **Task Organization**: Search, filter by priority/status/tags, and sort tasks
- **Task Automation**: Recurring tasks and reminder notifications
- **Responsive UI**: Modern Next.js frontend with Tailwind CSS

## Technology Stack

### Frontend
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Fetch API

### Backend
- Python FastAPI
- SQLModel ORM
- JWT Authentication
- RESTful API

### Database
- PostgreSQL (Neon Serverless recommended)
- UUID primary keys
- Async database operations

### Background Jobs
- APScheduler for job scheduling
- Recurring task processor
- Reminder dispatcher

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 12+ (or Neon Serverless account)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd todoapp
```

### 2. Backend Setup

```bash
cd server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your actual values
```

**Environment Variables (.env):**
```env
DATABASE_URL=postgresql://user:password@localhost/todoapp
SECRET_KEY=your-secret-key-here-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Note:** Generate a secure SECRET_KEY using:
```bash
openssl rand -hex 32
```

### 3. Database Setup

```bash
# Create database (PostgreSQL)
createdb todoapp

# Run database migrations (if using Alembic)
alembic upgrade head
```

### 4. Frontend Setup

```bash
cd client

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your backend URL
```

**Environment Variables (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5. Install All Dependencies (Alternative)

```bash
# This script installs Python and Node dependencies
./scripts/install-dependencies.sh
```

## Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
cd server
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

Backend API will be available at http://localhost:8000

**Terminal 2 - Frontend:**
```bash
cd client
npm run dev
```

Frontend will be available at http://localhost:3000

**Terminal 3 - Background Jobs:**
```bash
cd server
source venv/bin/activate
python manage.py
```

### Production Mode

**Backend:**
```bash
cd server
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Frontend:**
```bash
cd client
npm run build
npm start
```

## API Documentation

Once the backend is running, you can view interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

### Backend API Tests

```bash
cd server
pytest tests/ -v
```

### Frontend Tests

```bash
cd client
npm test
```

### Manual Testing

1. **Authentication:**
   - Sign up at http://localhost:3000/signup
   - Log in at http://localhost:3000/login
   - Access dashboard at http://localhost:3000/dashboard

2. **Task Management:**
   - Create tasks via POST /tasks
   - List tasks via GET /tasks
   - Update tasks via PUT /tasks/{id}
   - Delete tasks via DELETE /tasks/{id}

3. **Task Organization:**
   - Search: GET /tasks/search?q=keyword
   - Filter: GET /tasks/filter?completed=true&priority=high
   - Sort: GET /tasks/sort?by=due_date&order=asc

4. **Automation:**
   - Set due dates via POST /tasks/{id}/due-date
   - Configure recurrence via POST /tasks/{id}/recurrence
   - Create reminders via POST /tasks/{id}/reminders
   - View pending reminders via GET /reminders/pending

## Project Structure

```
.
├── server/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry
│   │   ├── models.py            # SQLModel database models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── auth.py              # JWT utilities
│   │   ├── dependencies.py      # FastAPI dependencies
│   │   ├── crud.py              # Database operations
│   │   └── routers/
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── tasks.py         # Tasks CRUD endpoints
│   │       └── reminders.py     # Reminders endpoints
│   ├── workers/
│   │   ├── scheduler.py         # APScheduler setup
│   │   └── jobs.py              # Job implementations
│   ├── requirements.txt         # Python dependencies
│   └── .env.example            # Backend env template
│
├── client/
│   ├── app/
│   │   ├── auth/login/          # Login page
│   │   ├── auth/signup/         # Signup page
│   │   └── dashboard/           # Dashboard with tasks
│   ├── components/              # React components
│   ├── lib/                     # API client and utilities
│   ├── hooks/                   # Custom React hooks
│   ├── package.json             # Node dependencies
│   └── .env.example            # Frontend env template
│
├── scripts/                     # Setup and utility scripts
├── specs/                       # Feature specifications
└── README.md                    # This file
```

## Database Schema

### User Table
- id (UUID, PK)
- email (String, Unique)
- name (String, Nullable)
- hashed_password (String)
- created_at (DateTime)
- updated_at (DateTime)

### Task Table
- id (UUID, PK)
- user_id (UUID, FK → User)
- title (String)
- description (String, Nullable)
- completed (Boolean, Default False)
- due_date (DateTime, Nullable)
- priority (Enum: low/medium/high)
- is_recurring (Boolean, Default False)
- recurrence_type (Enum: daily/weekly/monthly)
- recurrence_interval (Integer)
- created_at (DateTime)
- updated_at (DateTime)

### Reminder Table
- id (UUID, PK)
- task_id (UUID, FK → Task)
- remind_at (DateTime)
- sent (Boolean, Default False)
- created_at (DateTime)

### Tag Table
- id (UUID, PK)
- user_id (UUID, FK → User)
- name (String)
- color (String, Nullable)

### TaskTag Association Table
- task_id (UUID, FK → Task)
- tag_id (UUID, FK → Tag)

## Background Jobs

### Recurring Task Processor
- **Schedule:** Every 5 minutes
- **Purpose:** Generate new instances of completed recurring tasks

### Reminder Dispatcher
- **Schedule:** Every 1 minute
- **Purpose:** Send notifications for upcoming tasks

## Environment Configuration

### Production Considerations

1. **Security:**
   - Use strong, unique SECRET_KEY
   - Set ACCESS_TOKEN_EXPIRE_MINUTES appropriately
   - Configure CORS for your frontend domain
   - Use HTTPS in production

2. **Database:**
   - Use managed PostgreSQL (Neon, AWS RDS, etc.)
   - Enable connection pooling
   - Regular backups

3. **Background Jobs:**
   - Run as systemd service or in containers
   - Configure logging
   - Set up monitoring and alerts

4. **Frontend:**
   - Build for production: `npm run build`
   - Deploy to Vercel or similar platform
   - Configure environment variables

## Troubleshooting

### Backend Issues
- **Database connection failed:** Check DATABASE_URL in .env
- **JWT errors:** Verify SECRET_KEY and ALGORITHM match
- **Import errors:** Ensure virtual environment is activated and dependencies installed

### Frontend Issues
- **CORS errors:** Configure CORS policy on backend
- **API 401 errors:** Check token storage and Authorization header
- **Build errors:** Verify all dependencies installed and TypeScript compiles

### Background Jobs
- **Jobs not running:** Check APScheduler configuration
- **Duplicate tasks:** Verify job idempotency and database transactions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the full test suite
6. Submit a pull request

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
