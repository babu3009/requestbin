# Testing the New Split-Panel Inspect View

## Quick Start

### 1. Start the Application
```powershell
.\run-postgres.bat
```

### 2. Open Your Browser
Navigate to: http://localhost:4000

### 3. Login
- Email: `admin@requestbin.cfapps.eu10-004.hana.ondemand.com`
- Password: `ChangeMe123!`

### 4. Create a Bin or Use Existing One
- Click "Create a RequestBin"
- Note the bin ID (e.g., `6b4crirj`)

## Manual Testing (Browser)

### Option 1: Use Browser Developer Tools

1. Open Developer Tools (F12)
2. Go to Console tab
3. Run these commands:

```javascript
// Test 1: JSON POST
fetch('http://localhost:4000/YOUR_BIN_ID', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({test: 'json_data', timestamp: new Date().toISOString()})
});

// Test 2: Form URL-Encoded
fetch('http://localhost:4000/YOUR_BIN_ID', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: 'username=testuser&password=secret&remember=true'
});

// Test 3: GET with Query Params
fetch('http://localhost:4000/YOUR_BIN_ID?search=test&page=1&limit=10');

// Test 4: PUT Request
fetch('http://localhost:4000/YOUR_BIN_ID', {
    method: 'PUT',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({id: 123, status: 'updated'})
});

// Test 5: DELETE Request
fetch('http://localhost:4000/YOUR_BIN_ID?id=456', {method: 'DELETE'});
```

## Automated Testing (Python Script)

### Run the Test Script

1. **Start the app first:**
```powershell
.\run-postgres.bat
```

2. **In a NEW terminal, run:**
```powershell
.\test-inspect-view.bat
```

This will send 10 different types of requests:
- JSON POST
- Form URL-Encoded POST
- GET with query parameters
- XML POST
- Plain text POST
- PUT with JSON
- DELETE request
- PATCH request
- Form data POST
- GET with custom headers

## What to Verify

### ✅ Left Panel (Request List)

Check that you see:
- **Column Headers**: #, Date & Time, Method, Type, Size, IP
- **Record ID**: Sequential numbers (1, 2, 3...)
- **Date Format**: `YYYY-MM-DD HH:mm:ss` with timezone below
- **HTTP Method Badges**: Color-coded
  - GET = Green
  - POST = Blue
  - PUT = Orange
  - PATCH = Purple
  - DELETE = Red
- **Content Type Classification**:
  - `json` for application/json
  - `form-urlencoded` for application/x-www-form-urlencoded
  - `form-data` for multipart/form-data
  - `xml` for application/xml
  - `text` for text/*
  - `binary` for images or octet-stream
  - `raw` for other types
- **Size**: Shows in bytes or kB
- **IP Address**: Shows source IP (likely 127.0.0.1)

### ✅ Interactions

1. **Click a Request Row**
   - Row should highlight with blue background
   - Blue left border should appear on selected row
   - Right panel should update to show that request's details

2. **Hover Over Rows**
   - Row should show light gray background on hover

3. **View Request Details** (Right Panel)
   - Should see request number and "Details" header
   - HTTP method badge and full path
   - Metadata icons (time, IP, size)
   - Complete headers in table format
   - Query parameters (if present)
   - Form/POST parameters (if present)
   - Raw body with syntax highlighting
   - cURL command at the bottom

4. **Copy to Clipboard**
   - Click the "Copy to clipboard" button
   - Button should change to show "✓ Copied!"
   - Button should turn green briefly
   - Should return to normal after 2 seconds

### ✅ Responsive Design

1. **Desktop View** (>1200px)
   - Left panel: ~45% width
   - Right panel: ~55% width

2. **Tablet View** (768px - 1200px)
   - Left panel: ~40% width
   - Right panel: ~60% width

3. **Mobile View** (<768px)
   - Panels should stack vertically
   - List panel on top (max 400px height)
   - Detail panel below (full width)

## Visual Comparison

### Before (Old View)
- Single column layout
- All details expanded for all requests
- Lots of scrolling required
- Hard to see overview

### After (New Split-Panel View)
- Split-panel Outlook-style layout
- Tabular list showing many requests at once
- Click to view details on the right
- Professional, efficient interface
- Clear visual hierarchy

## Common Issues

### App Not Running
```powershell
# Check if port 4000 is in use
netstat -ano | findstr :4000

# If needed, kill the process
taskkill /PID <PID> /F

# Restart
.\run-postgres.bat
```

### Test Script Fails
- Make sure the app is running first
- Check the bin ID in test_inspect_view.py matches your bin
- Ensure conda environment is activated

### No Requests Showing
- Make sure you're viewing the correct bin
- Add `?inspect` to the URL
- Try refreshing the page

## Screenshots Checklist

Take screenshots showing:
1. ✅ Empty bin view
2. ✅ List with multiple requests (left panel)
3. ✅ Selected request with details (right panel)
4. ✅ Different HTTP method badges
5. ✅ Different content type classifications
6. ✅ Copy button before and after clicking
7. ✅ Mobile responsive view

## Success Criteria

- [ ] Left panel shows tabular list with all columns
- [ ] Requests are numbered sequentially
- [ ] Date/time format is correct (YYYY-MM-DD HH:mm:ss)
- [ ] HTTP methods have color-coded badges
- [ ] Content types are correctly classified
- [ ] Clicking a request shows details on the right
- [ ] Active request is highlighted in blue
- [ ] Copy to clipboard works with visual feedback
- [ ] Layout is responsive on different screen sizes
- [ ] All headers, query params, and form data display correctly
- [ ] Raw body is shown with proper formatting
- [ ] cURL command is accurate and copyable

## Next Steps

After verifying everything works:
1. Commit changes to git
2. Deploy to SAP BTP production
3. Test in production environment
4. Update user documentation

## Need Help?

See `INSPECT_VIEW_UPDATE.md` for complete technical documentation.
