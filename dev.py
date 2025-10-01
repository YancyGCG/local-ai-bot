#!/usr/bin/env python3
"""
Development server with hot reload for both frontend and backend
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path
from threading import Thread

class DevServer:
    def __init__(self):
        self.processes = []
        self.running = True
        
    def start_backend(self):
        """Start backend with auto-reload"""
        print("🐍 Starting backend server with hot reload...")
        env = os.environ.copy()
        env['PYTHONPATH'] = str(Path.cwd())
        
        # Use uvicorn with reload for the backend
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "src.web_api:app",
            "--host", "0.0.0.0",
            "--port", "8899",
            "--reload",
            "--reload-dir", "src",
            "--reload-dir", "templates"
        ]
        
        process = subprocess.Popen(cmd, env=env)
        self.processes.append(('backend', process))
        return process
        
    def start_frontend(self):
        """Start frontend dev server"""
        print("⚡ Starting frontend dev server...")
        os.chdir("frontend")
        
        # Start Vite dev server
        cmd = ["npm", "run", "dev", "--", "--port", "3000", "--host"]
        process = subprocess.Popen(cmd)
        self.processes.append(('frontend', process))
        
        # Go back to root directory
        os.chdir("..")
        return process
        
    def stop_all(self):
        """Stop all processes"""
        self.running = False
        print("\n🛑 Stopping all servers...")
        
        for name, process in self.processes:
            if process.poll() is None:  # Process is still running
                print(f"   Stopping {name}...")
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print(f"   Force killing {name}...")
                    process.kill()
                    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        self.stop_all()
        sys.exit(0)
        
    def run(self):
        """Run both servers"""
        # Set up signal handling
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("🚀 Starting Local AI Bot Development Environment")
        print("=" * 50)
        
        # Start both servers
        backend_process = self.start_backend()
        time.sleep(2)  # Give backend a moment to start
        frontend_process = self.start_frontend()
        
        print("\n✅ Development servers started!")
        print("📱 Frontend: http://localhost:3000 (with hot reload)")
        print("🔧 Backend:  http://localhost:8899 (with auto-reload)")
        print("💡 Make changes to your code and see them instantly!")
        print("\nPress Ctrl+C to stop all servers")
        print("=" * 50)
        
        # Monitor processes
        try:
            while self.running:
                # Check if any process died
                for name, process in self.processes:
                    if process.poll() is not None:
                        print(f"❌ {name} server stopped unexpectedly")
                        self.stop_all()
                        return
                        
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.stop_all()

if __name__ == "__main__":
    # Check if we're in the right directory
    if not Path("src/web_api.py").exists():
        print("❌ Please run this script from the local-ai-bot directory")
        sys.exit(1)
        
    if not Path("frontend/package.json").exists():
        print("❌ Frontend directory not found. Please ensure frontend is set up.")
        sys.exit(1)
        
    server = DevServer()
    server.run()