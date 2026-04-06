# ⚙️ PhoenixPME Technical Setup Guide

**Last Updated:** February 24, 2026
**Purpose:** For developers who want to run the PhoenixPME platform locally
**Current Status:** ✅ Local development working with mock wallet (until March 6)

---

## 📋 Prerequisites

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Node.js | v20+ | `node --version` |
| PostgreSQL | v14+ | `postgres --version` |
| Git | latest | `git --version` |
| npm | v10+ | `npm --version` |

---

## 🚀 Quick Start (3 Terminals)

### Terminal 1: Start Database
```bash
# Start PostgreSQL
sudo systemctl start postgresql

# Verify it's running
sudo systemctl status postgresql

# Create database (if not exists)
createdb phoenix

Terminal 2: Start Backend

cd ~/dev/TX/apps/backend

# Install dependencies
npm install

# Set up environment
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations
npx prisma migrate dev

# Start development server
npm run dev
# Runs on http://localhost:3001

Terminal 3: Start Frontend

cd ~/dev/TX/apps/frontend

# Install dependencies
npm install

# Set up environment
cp .env.local.example .env.local
# Edit .env.local if needed

# Start development server
npm run dev
# Runs on http://localhost:3000

🔧 Configuration Files
Backend .env example:
env
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/phoenix"
PORT=3001
NODE_ENV=development
ADMIN_PASSWORD=your-secure-password
Frontend .env.local example:
env
NEXT_PUBLIC_API_URL=http://localhost:3001
NEXT_PUBLIC_CHAIN_ID=coreum-testnet-1
NEXT_PUBLIC_CONTRACT_ADDRESS= # Will be added after March 6 deployment
🐳 Docker Setup (Optional)
If you prefer using Docker for the database:

bash
# Run PostgreSQL via Docker
docker run --name phoenix-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=phoenix \
  -p 5432:5432 \
  -d postgres:14

# Connection string for .env:
# DATABASE_URL="postgresql://postgres:postgres@localhost:5432/phoenix"
✅ Verification
After starting all services, verify they're working:

bash
# Check backend API
curl http://localhost:3001/api/health
# Expected: {"status":"healthy",...}

# Check backend prices endpoint
curl http://localhost:3001/api/prices
# Expected: {"success":true,"data":{...}}

# Check frontend is running
curl -I http://localhost:3000
# Expected: HTTP/1.1 200 OK

# When running, you should see:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:3001
# - Mock wallet available for testing (until March 6)
🔧 Troubleshooting
Common Issues
Mock Wallet Not Showing
If the wallet selector doesn't appear, check that:

✅ You're running the latest code (git pull)

✅ Dependencies are installed (npm install)

✅ No errors in browser console (F12)

✅ You're on the sandbox page (/sandbox)

Backend Won't Start
bash
# Check if port 3001 is already in use
sudo lsof -i :3001

# Check database connection
psql -d phoenix -c "SELECT 1"

# Check for TypeScript errors
npm run build
Database Connection Issues
bash
# Verify PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U postgres -d phoenix -h localhost

# Reset database if needed
npx prisma migrate reset --force
Frontend Build Fails
bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Check TypeScript errors
npx tsc --noEmit
CORS Errors in Development
If you see CORS errors when the frontend tries to fetch from backend:

✅ Backend CORS is configured for http://localhost:3000

✅ Check that NEXT_PUBLIC_API_URL is set to http://localhost:3001

✅ Restart both servers after configuration changes

📦 Dependencies Overview
Backend Dependencies
Express - Web framework

Prisma - Database ORM

PostgreSQL - Database

TypeScript - Language

CORS - Cross-origin resource sharing

Frontend Dependencies
Next.js 14 - React framework

TypeScript - Language

Tailwind CSS - Styling

Lucide React - Icons

@cosmjs/ - CosmWasm client libraries

🧪 Testing the Setup
1. Create a Test Auction (UI)
Visit http://localhost:3000/auctions/create

Fill in metal details (type, weight, purity)

Set starting and reserve prices

Submit form (uses mock data until March 6)

2. Check Database
bash
# Connect to database
psql -d phoenix

# View price history
SELECT * FROM "PriceHistory" ORDER BY "createdAt" DESC LIMIT 5;
3. Admin Panel
Visit http://localhost:3000/admin

Login with your ADMIN_PASSWORD from .env

Update metal prices

Verify prices update in the price banner

🔄 Git Workflow
bash
# Get latest changes
git pull origin main

# Create a branch for your changes
git checkout -b feature/your-feature

# Commit changes
git add .
git commit -m "Description of changes"

# Push and create PR
git push origin feature/your-feature
📝 Important Notes
Until March 6, 2026
✅ Smart contracts are ready but not deployed

✅ UI uses mock data for auction creation

✅ Wallet connection works (mock wallet available)

✅ Price banner shows live data from backend

✅ Admin panel works for price updates

After March 6, 2026
🔜 Contracts deploy to TX Testnet 6.0

🔜 Real TESTUSD tokens will be used

🔜 Actual auction creation and bidding

🔜 Community testing begins

📚 Related Documentation
Document	Purpose
Quick Start Guide	For users using the platform
Architecture Overview	System design
Coreum Reference	Official Coreum documentation
Contributing Guide	How to contribute
CURRENT-FOCUS.md	What we're building now
🚀 Quick Commands Reference
bash
# Start everything
sudo systemctl start postgresql
cd ~/dev/TX/apps/backend && npm run dev
cd ~/dev/TX/apps/frontend && npm run dev

# Stop everything
pkill -f node
sudo systemctl stop postgresql

# Update everything
git pull origin main
cd apps/backend && npm install
cd ../frontend && npm install

# Build for production
cd apps/frontend && npm run build
🆘 Getting Help
GitHub Issues: https://github.com/greg-gzillion/TX/issues

Email: gjf20842@gmail.com

Discussions: GitHub Discussions tab

Last Updated: February 24, 2026
*Next Milestone: March 6, 2026 - TX Testnet Launch* 🚀
