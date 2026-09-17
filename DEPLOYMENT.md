# Deployment Guide

## Local Development with PostgreSQL

1. **Set up environment variables:**
   ```bash
   cp webapp/.env.example webapp/.env
   # Edit webapp/.env with your Neon DATABASE_URL
   ```

2. **Install dependencies:**
   ```bash
   cd webapp
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   # Access at http://localhost:8000
   ```

## Production Deployment

### Option 1: Render (Recommended for PostgreSQL)

1. **Create a Render account** at [render.com](https://render.com)

2. **Create a new Web Service:**
   - Connect your GitHub repository
   - Select the `webapp` folder as root directory
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

3. **Add Environment Variables:**
   - `DATABASE_URL`: Your Neon PostgreSQL connection string
   - `HOST`: `0.0.0.0`
   - `PORT`: `8000`
   - `MAX_ROWS`: `1000`
   - `ALLOWED_ORIGIN`: `*`

4. **Deploy** - Render will automatically deploy when you push to GitHub

### Option 2: Railway

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. **Initialize project:**
   ```bash
   cd webapp
   railway init
   ```

3. **Add PostgreSQL database:**
   ```bash
   railway add postgresql
   ```

4. **Set environment variables:**
   ```bash
   railway variables set PORT=8000
   railway variables set MAX_ROWS=1000
   railway variables set ALLOWED_ORIGIN=*
   ```

5. **Deploy:**
   ```bash
   railway up
   ```

### Option 3: Cloudflare Workers (Current - SQLite only)

The current Cloudflare Workers deployment uses D1 (SQLite) and has limited PL/SQL support. For full PostgreSQL functionality, use Render or Railway.

## Frontend Configuration

After deploying the backend, update `webapp/static/config.js`:

```javascript
window.API_BASE = "https://your-backend-url.onrender.com";
```

## SQL Features Supported

### With PostgreSQL (Render/Railway):
- ✅ Full DQL (SELECT with complex queries)
- ✅ Full DML (INSERT, UPDATE, DELETE)
- ✅ Full DDL (CREATE, ALTER, DROP)
- ✅ Stored Procedures and Functions
- ✅ Triggers
- ✅ Transactions (BEGIN, COMMIT, ROLLBACK)
- ✅ PL/SQL procedural blocks
- ✅ Window functions
- ✅ CTEs
- ✅ All PostgreSQL-specific features

### With Cloudflare D1 (Current):
- ✅ Basic DQL (SELECT)
- ✅ Basic DML (INSERT, UPDATE, DELETE)
- ✅ Basic DDL (CREATE, ALTER, DROP)
- ⚠️ Limited transaction support
- ❌ No stored procedures
- ❌ No triggers
- ❌ No PL/SQL

## Neon Database Setup

1. **Create a Neon account** at [neon.tech](https://neon.tech)

2. **Create a new project** and database

3. **Get connection string** from Neon dashboard

4. **Test connection:**
   ```bash
   psql "postgresql://user:password@host/database"
   ```

## Troubleshooting

### PostgreSQL Connection Issues
- Ensure SSL mode is enabled in connection string
- Check Neon database status
- Verify firewall rules allow connections

### Deployment Issues
- Check Render/Railway logs
- Verify environment variables are set correctly
- Ensure requirements.txt is up to date

### Frontend Not Connecting
- Update API_BASE in config.js
- Check CORS settings
- Verify backend is running