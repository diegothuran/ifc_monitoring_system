#!/usr/bin/env python3
"""
Startup script for the IFC Monitoring System
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("✓ Backend dependencies are installed")
    except ImportError as e:
        print(f"✗ Missing backend dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    return True

def check_frontend_dependencies():
    """Check if frontend dependencies are installed"""
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print("✗ Frontend directory not found")
        return False
    
    node_modules = frontend_path / "node_modules"
    if not node_modules.exists():
        print("✗ Frontend dependencies not installed")
        print("Please run: cd frontend && npm install")
        return False
    
    print("✓ Frontend dependencies are installed")
    return True

def start_backend():
    """Start the backend server"""
    print("Starting backend server...")
    try:
        # Start the backend server
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Check if the server is running
        if process.poll() is None:
            print("✓ Backend server started successfully")
            print("  API available at: https://ifc-backend-ph0n.onrender.com")
            print("  API docs at: https://ifc-backend-ph0n.onrender.com/docs")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"✗ Backend server failed to start:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"✗ Error starting backend server: {e}")
        return None

def start_frontend():
    """Start the frontend development server"""
    print("Starting frontend server...")
    try:
        # Change to frontend directory and start the development server
        process = subprocess.Popen([
            "npm", "start"
        ], cwd="frontend", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        time.sleep(5)
        
        # Check if the server is running
        if process.poll() is None:
            print("✓ Frontend server started successfully")
            print("  Frontend available at: http://localhost:3000")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"✗ Frontend server failed to start:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"✗ Error starting frontend server: {e}")
        return None

def main():
    """Main startup function"""
    print("="*60)
    print("IFC MONITORING SYSTEM STARTUP")
    print("="*60)
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    if not check_frontend_dependencies():
        return 1
    
    # Check if sample data exists
    from backend.core.database import SessionLocal
    from backend.models import User
    
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        if user_count == 0:
            print("\nNo users found. Creating sample data...")
            import create_sample_data
            create_sample_data.create_sample_data()
            print("✓ Sample data created successfully")
        else:
            print(f"✓ Found {user_count} users in database")
    except Exception as e:
        print(f"✗ Error checking database: {e}")
        return 1
    finally:
        db.close()
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        return 1
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        return 1
    
    print("\n" + "="*60)
    print("SYSTEM STARTED SUCCESSFULLY!")
    print("="*60)
    print("\nAccess points:")
    print("  Frontend: http://localhost:3000")
    print("  Backend API: https://ifc-backend-ph0n.onrender.com")
    print("  API Documentation: https://ifc-backend-ph0n.onrender.com/docs")
    print("\nDefault login credentials:")
    print("  Admin: admin / admin123")
    print("  Operator: operator / operator123")
    print("  Viewer: viewer / viewer123")
    print("\nPress Ctrl+C to stop both servers")
    
    try:
        # Open browser to frontend
        time.sleep(2)
        webbrowser.open("http://localhost:3000")
        
        # Wait for user to stop the servers
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\nStopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        
        # Wait for processes to terminate
        backend_process.wait()
        frontend_process.wait()
        
        print("✓ Servers stopped successfully")
        return 0

if __name__ == "__main__":
    sys.exit(main())
