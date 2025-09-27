#!/usr/bin/env python3
"""
Test server to debug the IFC Monitoring System
"""

import sys
import traceback

try:
    print("Starting IFC Monitoring System...")
    
    # Import main components
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
    
    print("✓ FastAPI imported successfully")
    
    # Create a simple FastAPI app first
    app = FastAPI(title="IFC Monitoring System Test")
    
    print("✓ FastAPI app created successfully")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    print("✓ CORS middleware added successfully")
    
    @app.get("/")
    async def root():
        return {"message": "IFC Monitoring System API - Test Version", "status": "running"}
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    print("✓ Routes defined successfully")
    
    # Test database connection
    try:
        from backend.core.database import engine
        from backend.models import Base
        print("✓ Database components imported successfully")
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully")
        
    except Exception as e:
        print(f"⚠ Database warning: {e}")
    
    print("\n🚀 Starting server on http://localhost:45000")
    print("📖 API docs available at http://localhost:45000/docs")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Run the server
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=45000,
        log_level="info"
    )
    
except Exception as e:
    print(f"❌ Error starting server: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)
