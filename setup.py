"""
Setup Script for Copilot Localization Translator
Automates the initial setup process.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is adequate."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"[OK] Python version {sys.version_info.major}.{sys.version_info.minor} is adequate")
    return True

def create_virtual_environment():
    """Create a virtual environment."""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("[OK] Virtual environment already exists")
        return True
    
    try:
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("[OK] Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return False

def install_dependencies():
    """Install required dependencies."""
    venv_python = "venv\\Scripts\\python.exe" if os.name == 'nt' else "venv/bin/python"
    
    if not Path(venv_python).exists():
        print("Error: Virtual environment Python not found")
        return False
    
    try:
        print("Installing dependencies...")
        subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("[OK] Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def create_env_file():
    """Create .env file from template."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("[OK] .env file already exists")
        return True
    
    if not env_example.exists():
        print("Warning: .env.example not found")
        return False
    
    try:
        env_file.write_text(env_example.read_text())
        print("[OK] .env file created from template")
        print("  Please edit .env and add your OpenAI API key")
        return True
    except Exception as e:
        print(f"Error creating .env file: {e}")
        return False

def run_tests():
    """Run the test suite."""
    venv_python = "venv\\Scripts\\python.exe" if os.name == 'nt' else "venv/bin/python"
    
    try:
        print("Running tests...")
        result = subprocess.run([venv_python, "test_app.py"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("[OK] All tests passed")
            return True
        else:
            print("[FAIL] Some tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def main():
    """Main setup function."""
    print("=" * 60)
    print("Copilot Localization Translator - Setup")
    print("=" * 60)
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Creating virtual environment", create_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Creating environment file", create_env_file),
        ("Running tests", run_tests)
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"\n[FAIL] Setup failed at: {step_name}")
            print("Please fix the error and run setup again.")
            return False
    
    print("\n" + "=" * 60)
    print("[SUCCESS] Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run the application:")
    print("   - python run_app.py")
    print("   - or double-click run_app.bat on Windows")
    print("\nFor help, see README.md")
    
    return True

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)