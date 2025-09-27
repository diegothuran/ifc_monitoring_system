"""
Script to run the Streamlit IFC Monitoring App
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def run_streamlit():
    """Run the Streamlit app"""
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "main.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped!")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

if __name__ == "__main__":
    print("🚀 Starting IFC Monitoring System - Streamlit Frontend")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found. Please run this script from the streamlit_app directory.")
        sys.exit(1)
    
    # Install requirements
    print("📦 Installing requirements...")
    if not install_requirements():
        sys.exit(1)
    
    print("\n🌐 Starting Streamlit app...")
    print("📍 App will be available at: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the app")
    print("=" * 60)
    
    # Run Streamlit
    run_streamlit()
