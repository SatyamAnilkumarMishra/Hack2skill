#!/usr/bin/env python3
"""
Simple runner script for the Agentic RAG project.
Provides easy commands to run different interfaces.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        import google.generativeai
        import langchain
        return True
    except ImportError as e:
        print(f"❌ Missing required packages: {str(e)}")
        print("📦 Please install requirements: pip install -r requirements.txt")
        return False

def check_env():
    """Check if environment is properly configured"""
    if not os.path.exists(".env"):
        print("❌ .env file not found")
        print("🔧 Please create a .env file with your Google API key:")
        print("   GOOGLE_API_KEY=your_api_key_here")
        return False
    
    # Load .env file to check API key
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ GOOGLE_API_KEY not found in .env file")
        print("🔧 Please add your Google API key to the .env file:")
        print("   GOOGLE_API_KEY=your_api_key_here")
        return False
    
    print("✅ Environment configured correctly")
    return True

def run_streamlit():
    """Run the Streamlit web interface"""
    print("🚀 Starting Streamlit web interface...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Streamlit: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Streamlit stopped")

def run_cli():
    """Run the command-line interface"""
    print("🚀 Starting CLI interface...")
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start CLI: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 CLI stopped")

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        sys.exit(1)

def create_sample_env():
    """Create a sample .env file"""
    env_content = """# Agentic RAG Configuration
# Add your Google API key below:
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Other configuration
# LOG_LEVEL=INFO
"""
    
    if os.path.exists(".env"):
        print("⚠️  .env file already exists")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("❌ Operation cancelled")
            return
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ Sample .env file created")
    print("🔧 Please edit the .env file and add your Google API key")

def show_status():
    """Show project status"""
    print("📊 Agentic RAG Project Status")
    print("=" * 40)
    
    # Check files
    required_files = ["requirements.txt", "app.py", "main.py", "crew_config.py", "rag_pipeline.py"]
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
    
    # Check .env
    if os.path.exists(".env"):
        print("✅ .env")
        from dotenv import load_dotenv
        load_dotenv()
        if os.getenv("GOOGLE_API_KEY"):
            print("✅ Google API Key configured")
        else:
            print("❌ Google API Key not configured")
    else:
        print("❌ .env")
    
    # Check packages
    print("\n📦 Package Status:")
    packages = ["streamlit", "google-generativeai", "langchain", "chromadb", "python-dotenv"]
    for pkg in packages:
        try:
            __import__(pkg.replace("-", "_"))
            print(f"✅ {pkg}")
        except ImportError:
            print(f"❌ {pkg}")

def main():
    parser = argparse.ArgumentParser(description="Agentic RAG Project Runner")
    parser.add_argument("command", nargs="?", choices=["web", "cli", "install", "setup", "status"], 
                       help="Command to run")
    
    args = parser.parse_args()
    
    if not args.command:
        print("🤖 Agentic RAG Assistant")
        print("=" * 30)
        print("Available commands:")
        print("  web     - Start Streamlit web interface")
        print("  cli     - Start command-line interface")
        print("  install - Install requirements")
        print("  setup   - Create sample .env file")
        print("  status  - Show project status")
        print("\nUsage: python run.py [command]")
        return
    
    if args.command == "install":
        install_requirements()
    elif args.command == "setup":
        create_sample_env()
    elif args.command == "status":
        show_status()
    elif args.command == "web":
        if not check_requirements() or not check_env():
            sys.exit(1)
        run_streamlit()
    elif args.command == "cli":
        if not check_requirements() or not check_env():
            sys.exit(1)
        run_cli()

if __name__ == "__main__":
    main()