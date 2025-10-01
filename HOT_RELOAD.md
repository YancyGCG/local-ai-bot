# Hot Reload Development Setup

This setup enables instant hot reload for both frontend and backend development.

## Quick Start

### Option 1: VS Code Task (Recommended)
1. Open VS Code
2. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
3. Type "Tasks: Run Task"
4. Select "🔥 Start Local AI Bot (Hot Reload)"

### Option 2: Shell Script
```bash
cd local-ai-bot
./dev.sh
```

### Option 3: Python Script
```bash
cd local-ai-bot
python dev.py
```

## What You Get

### 🔥 **Hot Reload Magic**
- **Frontend**: Changes to React/TypeScript files are instantly reflected in the browser
- **Backend**: Changes to Python files automatically restart the FastAPI server
- **No manual restarts needed!**

### 🌐 **Two Development URLs**
- **Frontend Dev Server**: http://localhost:3000 
  - Vite dev server with instant hot reload
  - All API calls proxied to backend
- **Backend API**: http://localhost:8899
  - FastAPI server with auto-reload
  - Direct API access for testing

## How It Works

### Frontend (Vite)
- Runs on port 3000 with hot module replacement (HMR)
- Proxies API calls to backend on port 8899
- Instant updates when you save React/CSS/TypeScript files

### Backend (FastAPI + Uvicorn)
- Runs on port 8899 with `--reload` flag
- Watches `src/` and `templates/` directories
- Auto-restarts when Python files change

## Development Workflow

1. **Start the development servers** using any method above
2. **Open http://localhost:3000** in your browser
3. **Make changes** to your code:
   - Frontend changes (React/CSS/TS) → Instant browser update
   - Backend changes (Python) → Automatic server restart
4. **See changes immediately** without manual refreshes or restarts

## File Watching

### Frontend Files (Hot Reload)
- `src/**/*.tsx` - React components
- `src/**/*.ts` - TypeScript files  
- `src/**/*.css` - Stylesheets
- `public/**/*` - Static assets

### Backend Files (Auto-restart)
- `src/**/*.py` - Python source code
- `templates/**/*` - Template files

## Stopping the Servers

Simply press `Ctrl+C` in the terminal running the development script. Both servers will be stopped gracefully.

## Troubleshooting

### Port Already in Use
If ports 3000 or 8899 are in use:
```bash
# Kill any existing processes
pkill -f "uvicorn.*web_api"
pkill -f "vite.*dev"
```

### Frontend Won't Start
Make sure dependencies are installed:
```bash
cd frontend
npm install
```

### Backend Won't Start
Make sure you're in the virtual environment:
```bash
source ../.venv/bin/activate  # From local-ai-bot directory
```

## Benefits Over Production Mode

- **No build step** required for frontend changes
- **Source maps** available for debugging
- **Hot module replacement** preserves component state
- **Instant feedback** loop for development
- **Better error messages** with full stack traces