# Troubleshooting Guide

## ❌ "Failed to create negotiation session" Error

### **Solution 1: Reset Database (Most Common Fix)**

The database schema was updated with new fields. If you have an old database, it needs to be reset.

**Option A: Delete and recreate (Windows PowerShell)**
```powershell
cd "C:\Users\Pratham Ahuja\HackathonE\equi-exchange\backend"
# Stop the backend server first (Ctrl+C)
Remove-Item data.db -ErrorAction SilentlyContinue
# Restart backend - it will recreate the database
```

**Option B: Use reset script**
```powershell
cd "C:\Users\Pratham Ahuja\HackathonE\equi-exchange\backend"
.\.venv\Scripts\activate
python reset_database.py
# Type "yes" when prompted
```

**Option C: Manual reset**
1. Stop backend server
2. Delete `backend/data.db` file
3. Restart backend server
4. Database will be recreated automatically

---

### **Solution 2: Check Backend Logs**

Look at the terminal where backend is running. You should see the actual error message.

**Common errors:**
- `no such column: concession_rate` → Database needs reset (Solution 1)
- `ModuleNotFoundError` → Missing imports, check if all files exist
- `Connection error` → Database file locked, stop and restart

---

### **Solution 3: Verify All Files Exist**

Make sure these files exist:
- `backend/app/explainer.py`
- `backend/app/market_service.py`
- `backend/app/chat_service.py`
- `backend/app/theory_of_mind_agent.py`

If missing, they were created during implementation. Check the file structure.

---

### **Solution 4: Check Backend is Running**

1. Open http://localhost:8000 in browser
2. Should see: `{"message":"EquiExchange API is running 🚀"}`
3. If not, backend is not running or crashed

---

### **Solution 5: Check API Endpoint**

Test the endpoint directly:
```powershell
curl -X POST http://localhost:8000/sessions -H "Content-Type: application/json" -d '{\"role\":\"buyer\",\"target_price\":75,\"min_price\":50,\"max_price\":100,\"quantity\":1}'
```

This will show the exact error message.

---

### **Solution 6: Check Frontend Console**

1. Open browser DevTools (F12)
2. Go to Console tab
3. Try creating session
4. Look for error messages

---

## 🔍 Debugging Steps

### **Step 1: Check Backend Terminal**
- Look for Python errors or tracebacks
- Check if server started successfully
- Look for import errors

### **Step 2: Check Database File**
```powershell
cd backend
dir data.db
```
If file exists but is old, delete it and restart.

### **Step 3: Test API Directly**
Use Postman or curl to test the endpoint:
```bash
POST http://localhost:8000/sessions
Content-Type: application/json

{
  "role": "buyer",
  "buyer_address": "0x123...",
  "target_price": 75,
  "min_price": 50,
  "max_price": 100,
  "quantity": 1
}
```

### **Step 4: Check Network Tab**
In browser DevTools → Network tab:
- See if request is being sent
- Check response status code
- Read error message in response

---

## 🐛 Common Issues

### **Issue: "no such column: concession_rate"**
**Fix:** Database schema mismatch. Use Solution 1.

### **Issue: "ModuleNotFoundError: No module named 'app.explainer'"**
**Fix:** Make sure you're in the backend directory and all files exist.

### **Issue: "Database is locked"**
**Fix:** 
1. Stop backend server
2. Delete `data.db`
3. Restart backend

### **Issue: "Connection refused"**
**Fix:** Backend is not running. Start it in Terminal 1.

### **Issue: CORS errors**
**Fix:** Backend CORS is already configured. Check if backend is running on port 8000.

---

## ✅ Quick Fix Checklist

- [ ] Backend server is running (Terminal 1)
- [ ] Frontend server is running (Terminal 2)
- [ ] Database file exists or was recreated
- [ ] All new Python files exist (explainer.py, market_service.py, etc.)
- [ ] No errors in backend terminal
- [ ] Check browser console for errors
- [ ] Try resetting database (Solution 1)

---

## 📞 Still Not Working?

1. **Check backend terminal** - Copy the full error message
2. **Check browser console** - Look for JavaScript errors
3. **Check network tab** - See the actual API response
4. **Try resetting database** - Most common fix

Share the error message from backend terminal for more specific help!

