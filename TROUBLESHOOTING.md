# Troubleshooting Guide - Academic Grievance DSS

## Common Issues and Solutions

---

## Backend Issues

### Issue 1: Backend won't start

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
cd backend
pip3 install -r requirements.txt
```

---

### Issue 2: PostgreSQL connection refused

**Error:**
```
connection to server at "localhost", port 5432 failed: Connection refused
```

**Solution:**
This is expected! The system automatically falls back to mock database.

**To verify:**
```bash
curl http://localhost:8000/health
# Should show: "database": "mock (in-memory)"
```

**To use real PostgreSQL (optional):**
```bash
# Start PostgreSQL
docker run -d -p 5432:5432 \
  -e POSTGRES_DB=grievance_db \
  -e POSTGRES_USER=grievance_user \
  -e POSTGRES_PASSWORD=grievance_password \
  postgres:15

# Initialize schema
psql -h localhost -U grievance_user -d grievance_db -f database/init.sql
```

---

### Issue 3: JPype/Drools not found

**Error:**
```
No module named 'jpype'
```

**Solution:**
This is expected! The system automatically uses mock rule engine.

**To verify:**
```bash
curl http://localhost:8000/health
# Should show: "drools": "mock"
```

**To use real Drools (optional):**
```bash
# Install Java and Maven
brew install openjdk@11 maven

# Build Drools JAR
cd java-bridge
mvn clean package

# Install JPype1
pip3 install JPype1
```

---

### Issue 4: OpenAI API error

**Error:**
```
OpenAI API key not configured
```

**Solution:**
The system works without OpenAI! LLM service is configured but optional.

**To add OpenAI (optional):**
```bash
# Edit backend/.env
OPENAI_API_KEY=sk-your-actual-key-here
```

---

### Issue 5: CORS errors

**Error:**
```
Access-Control-Allow-Origin error
```

**Solution:**
```bash
# Edit backend/.env
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000","http://your-frontend-url"]
```

---

## Frontend Issues

### Issue 1: npm not found

**Error:**
```
zsh: command not found: npm
```

**Solution:**
```bash
# Install Node.js
brew install node

# Verify installation
node --version
npm --version
```

---

### Issue 2: Dependencies installation fails

**Error:**
```
npm ERR! code ERESOLVE
```

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

---

### Issue 3: Frontend can't connect to backend

**Error:**
```
Network Error
```

**Solution:**
1. Check backend is running:
```bash
curl http://localhost:8000/health
```

2. Check frontend .env:
```bash
# frontend/.env
REACT_APP_API_URL=http://localhost:8000
```

3. Restart frontend:
```bash
npm start
```

---

### Issue 4: Port 3000 already in use

**Error:**
```
Port 3000 is already in use
```

**Solution:**
```bash
# Option 1: Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Option 2: Use different port
PORT=3001 npm start
```

---

## API Issues

### Issue 1: 422 Unprocessable Entity

**Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "parameters"],
      "msg": "field required"
    }
  ]
}
```

**Solution:**
Ensure all required fields are included in request:
```json
{
  "student_id": "STU2024001",
  "grievance_type": "ATTENDANCE_SHORTAGE",
  "narrative": "Description",
  "parameters": {}  // Required, even if empty
}
```

---

### Issue 2: 500 Internal Server Error

**Error:**
```json
{
  "success": false,
  "error": "Internal server error"
}
```

**Solution:**
1. Check backend logs:
```bash
# Terminal running uvicorn will show detailed error
```

2. Enable debug mode in backend/.env:
```bash
DEBUG_MODE=True
```

3. Check health endpoint:
```bash
curl http://localhost:8000/health
```

---

### Issue 3: Empty response

**Error:**
No response from API

**Solution:**
1. Verify backend is running:
```bash
curl http://localhost:8000/
```

2. Check firewall settings

3. Verify correct URL:
```bash
# Correct
http://localhost:8000/api/grievances

# Incorrect
http://localhost:8000/grievances
```

---

## Testing Issues

### Issue 1: Test script not executable

**Error:**
```
Permission denied: ./test_api.sh
```

**Solution:**
```bash
chmod +x test_api.sh
./test_api.sh
```

---

### Issue 2: Tests failing

**Error:**
```
✗ FAILED: Expected REJECT outcome
```

**Solution:**
1. Check backend is running:
```bash
curl http://localhost:8000/health
```

2. Run individual test:
```bash
curl -X POST http://localhost:8000/api/grievances \
  -H "Content-Type: application/json" \
  -d @test_grievance.json | python3 -m json.tool
```

3. Check response manually

---

## Docker Issues

### Issue 1: Docker daemon not running

**Error:**
```
Cannot connect to the Docker daemon
```

**Solution:**
```bash
# Start Docker Desktop
open -a Docker

# Or use system without Docker (mock services work!)
```

---

### Issue 2: Container build fails

**Error:**
```
Error building image
```

**Solution:**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild
docker-compose build --no-cache
```

---

## Performance Issues

### Issue 1: Slow API responses

**Symptoms:**
API takes >5 seconds to respond

**Solution:**
1. Check if using real PostgreSQL (slower than mock)
2. Check if using real Drools (slower than mock)
3. Reduce log level in backend/.env:
```bash
LOG_LEVEL=WARNING
```

---

### Issue 2: High memory usage

**Symptoms:**
System using >2GB RAM

**Solution:**
Mock services use in-memory storage. For production:
1. Use real PostgreSQL
2. Implement data cleanup
3. Add pagination to API responses

---

## Data Issues

### Issue 1: Data not persisting

**Symptoms:**
Submitted grievances disappear after restart

**Solution:**
This is expected with mock database (in-memory).

**To persist data:**
1. Use real PostgreSQL
2. Or export data before shutdown:
```bash
curl http://localhost:8000/api/grievances/student/STU2024001 > backup.json
```

---

### Issue 2: Inconsistent decisions

**Symptoms:**
Same grievance gets different decisions

**Solution:**
This is expected with mock rule engine (randomized for testing).

**To get consistent decisions:**
1. Use real Drools engine
2. Or check mock_rule_engine_service.py logic

---

## Debugging Tips

### Enable Verbose Logging
```bash
# backend/.env
LOG_LEVEL=DEBUG
DEBUG_MODE=True
```

### Check Service Status
```bash
curl http://localhost:8000/health | python3 -m json.tool
```

### View Backend Logs
```bash
# Terminal running uvicorn shows all logs
```

### Test Individual Endpoints
```bash
# Health
curl http://localhost:8000/health

# Root
curl http://localhost:8000/

# Submit grievance
curl -X POST http://localhost:8000/api/grievances \
  -H "Content-Type: application/json" \
  -d @test_grievance.json
```

### Interactive API Testing
```bash
# Open Swagger UI
open http://localhost:8000/docs
```

---

## Getting Help

### Check Documentation
- README.md - Project overview
- QUICKSTART.md - Quick start guide
- API_DOCUMENTATION.md - API reference
- SYSTEM_SUMMARY.md - System details

### Check Logs
```bash
# Backend logs in terminal running uvicorn
# Frontend logs in browser console (F12)
```

### Verify System Status
```bash
# Run test suite
./test_api.sh

# Check health
curl http://localhost:8000/health
```

---

## Quick Fixes

### Reset Everything
```bash
# Stop backend (Ctrl+C in terminal)
# Stop frontend (Ctrl+C in terminal)

# Restart backend
cd backend
python3 -m uvicorn main:app --reload

# Restart frontend (if using)
cd frontend
npm start
```

### Clean Start
```bash
# Backend
cd backend
rm -rf __pycache__ .pytest_cache
python3 -m uvicorn main:app --reload

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

---

**Remember:** The system is designed to work WITHOUT external dependencies!
- ✅ No PostgreSQL needed (mock database)
- ✅ No Java/Maven needed (mock rule engine)
- ✅ No OpenAI API needed (mock LLM)

If something isn't working, check if mock services are active:
```bash
curl http://localhost:8000/health
```
