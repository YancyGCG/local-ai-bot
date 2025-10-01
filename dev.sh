#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🚀 Starting Local AI Bot Development Environment${NC}"
echo "================================================================"

# Check if we're in the right directory
if [[ ! -f "src/web_api.py" ]]; then
    echo -e "${RED}❌ Please run this script from the local-ai-bot directory${NC}"
    exit 1
fi

if [[ ! -f "frontend/package.json" ]]; then
    echo -e "${RED}❌ Frontend directory not found. Please ensure frontend is set up.${NC}"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Stopping all servers...${NC}"
    
    # Kill backend
    if [[ ! -z "$BACKEND_PID" ]]; then
        echo -e "   ${BLUE}Stopping backend...${NC}"
        kill $BACKEND_PID 2>/dev/null
    fi
    
    # Kill frontend
    if [[ ! -z "$FRONTEND_PID" ]]; then
        echo -e "   ${BLUE}Stopping frontend...${NC}"
        kill $FRONTEND_PID 2>/dev/null
    fi
    
    # Wait a moment then force kill if needed
    sleep 2
    pkill -f "uvicorn.*web_api" 2>/dev/null
    pkill -f "vite.*dev" 2>/dev/null
    pkill -f "local-ai-bot.*src.web_api" 2>/dev/null
    
    echo -e "${GREEN}✅ All servers stopped${NC}"
    exit 0
}

# Set up trap for cleanup
trap cleanup SIGINT SIGTERM

# Start backend with hot reload
echo -e "${BLUE}🐍 Starting backend server with hot reload...${NC}"
cd "$(dirname "$0")"

# Activate virtual environment and start backend
source ../.venv/bin/activate
PYTHONPATH=$(pwd) python -m uvicorn src.web_api:app \
    --host 0.0.0.0 \
    --port 8899 \
    --reload \
    --reload-dir src \
    --reload-dir templates &
BACKEND_PID=$!

# Give backend a moment to start
sleep 3

# Start frontend dev server
echo -e "${YELLOW}⚡ Starting frontend dev server...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!

# Go back to root
cd ..

echo ""
echo -e "${GREEN}✅ Development servers started!${NC}"
echo -e "${CYAN}📱 Frontend: http://localhost:3000 (with hot reload)${NC}"
echo -e "${CYAN}🔧 Backend:  http://localhost:8899 (with auto-reload)${NC}"
echo -e "${YELLOW}💡 Make changes to your code and see them instantly!${NC}"
echo ""
echo -e "${BLUE}Press Ctrl+C to stop all servers${NC}"
echo "================================================================"

# Wait for processes
wait