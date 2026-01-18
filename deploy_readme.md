# Deployment Guide

## Overview
This guide provides instructions for deploying the Task Management System to Vercel.

## Prerequisites

1. **GitHub Account** - Repository connected to GitHub
2. **Vercel Account** - Connected to GitHub
3. **Neon Account** - For PostgreSQL database (optional for local dev)

## Environment Setup

### 1. Local Development Setup

```bash
# Install dependencies
cd client && npm install
cd ../server && pip install -r requirements.txt

# Set up environment variables
cp server/.env.example server/.env
# Edit server/.env with your local database credentials

# Start backend server
cd server && uvicorn main:app --reload

# Start frontend server
cd client && npm run dev
```

### 2. Vercel Environment Variables

Set these in your Vercel project dashboard:

```bash
# Database (Production)
DATABASE_URL=neon_database_connection_string
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Authentication
JWT_SECRET=your-jwt-secret-key-here-minimum-32-characters
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Cron Security
CRON_SECRET=your-cron-secret-here
WORKER_SECRET=your-worker-secret-here

# Application
APP_ENVIRONMENT=production

# CORS (Production)
CORS_ORIGINS=https://your-vercel-app.vercel.app
```

## Deployment Steps

### Option A: Vercel CLI (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Link project
vercel link

# Deploy
vercel

# Production deploy
vercel --prod
```

### Option B: GitHub Integration

1. Push code to GitHub
2. Connect repository in Vercel dashboard
3. Configure environment variables in Vercel
4. Deploy automatically on push

## Cron Job Configuration

The following cron jobs are configured in `vercel.json`:

| Job | Endpoint | Schedule | Purpose |
|-----|----------|----------|---------|
| Reminder Dispatcher | `/api/cron/reminder-dispatcher` | Every minute | Send reminder notifications |
| Overdue Scanner | `/api/cron/overdue-scanner` | Every 15 minutes | Mark overdue tasks |

**Security:** Cron endpoints are protected with the `CRON_SECRET` header.

## Testing Deployment

### 1. Test Cron Endpoints Locally

```bash
# Edit test script with your secret
export CRON_SECRET=your-secret-here
python test_cron.py
```

### 2. Test Production Endpoints

```bash
# Health check (public endpoint)
curl https://your-vercel-app.vercel.app/api/health

# Cron test (requires secret header)
curl -X POST https://your-vercel-app.vercel.app/api/cron/reminder-dispatcher \
  -H "X-Cron-Secret: your-cron-secret-here"
```

## Monitoring

### Health Checks

```bash
# Application health
GET /api/health

# Cron job status
Check Vercel Cron logs in dashboard
```

### Logs

- **Vercel Dashboard** → Logs tab
- **Server logs**: Application logs in Vercel Functions
- **Cron logs**: Execution history in Vercel Cron

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Verify `DATABASE_URL` is correct
   - Check Neon database is running
   - Ensure SSL is configured properly

2. **Cron Jobs Not Running**
   - Verify `CRON_SECRET` matches in Vercel env and cron headers
   - Check Vercel Cron dashboard for schedule
   - Verify endpoint returns 200 status

3. **CORS Issues**
   - Update `CORS_ORIGINS` to include your production domains
   - Check frontend is calling correct API URL

### Testing Cron Locally

Update the test script with your actual secrets:

```python
# In test_cron.py
BASE_URL = "http://localhost:8000"
CRON_SECRET = "your-actual-secret-from-env"
```

## Database Migration

For production database updates:

1. Connect to Neon database
2. Run SQL migrations
3. Test with existing data
4. Update `DATABASE_URL` if database changes

## Rollback Procedure

If deployment fails:

1. **Vercel Dashboard** → Deployments → Revert to previous
2. **Database**: Restore from Neon backup if needed
3. **Environment Variables**: Revert changes in Vercel dashboard

## Post-Deployment Checklist

- [ ] All environment variables set
Z
- [ ] Database connected and responding
- [ ] Frontend loading correctly
- [ ] API endpoints responding
- [ ] Cron jobs scheduled and running
- [ ] Monitoring and logging configured
- [ ] Backup procedures in place

## Support

For issues with deployment:

1. Check Vercel documentation
2. Review logs in Vercel dashboard
3. Test locally with same environment variables
4. Contact support if persistent issues

---

*Last Updated: 2026-01-18*
*Version: 1.0.0*