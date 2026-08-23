#!/usr/bin/env python3
"""
Deployment and Installation Utility Script
Helps with various setup and deployment tasks
"""

import os
import sys
import subprocess
from pathlib import Path

class Setup:
    def __init__(self):
        self.repo_root = Path(__file__).parent
        self.venv_path = self.repo_root / 'venv'
        
    def check_python(self):
        """Check if Python 3.8+ is installed"""
        print("🔍 Checking Python version...")
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Python 3.8+ required")
            sys.exit(1)
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    
    def create_venv(self):
        """Create virtual environment"""
        print("\n📦 Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_path)], check=True)
            print("✓ Virtual environment created")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create venv: {e}")
            return False
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("\n📥 Installing dependencies...")
        try:
            # Get pip path based on OS
            if sys.platform == "win32":
                pip_path = self.venv_path / "Scripts" / "pip.exe"
            else:
                pip_path = self.venv_path / "bin" / "pip"
            
            # Upgrade pip
            subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
            
            # Install requirements
            subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
            print("✓ Dependencies installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def setup_env(self):
        """Setup environment file"""
        print("\n⚙️ Setting up environment...")
        env_file = self.repo_root / ".env"
        env_example = self.repo_root / ".env.example"
        
        if env_file.exists():
            print("✓ .env file already exists")
            return True
        
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            print("✓ Created .env from template")
            print("  ⚠️  Please edit .env with your credentials")
            return True
        
        print("❌ .env.example not found")
        return False
    
    def run_full_setup(self):
        """Run complete setup"""
        print("\n" + "="*50)
        print("🚀 LuxuryShoppers Bot - Full Setup")
        print("="*50)
        
        steps = [
            ("Python Check", self.check_python),
            ("Virtual Environment", self.create_venv),
            ("Dependencies", self.install_dependencies),
            ("Environment", self.setup_env),
        ]
        
        for step_name, step_func in steps:
            try:
                if not step_func():
                    print(f"\n❌ Setup failed at: {step_name}")
                    return False
            except Exception as e:
                print(f"\n❌ Error during {step_name}: {e}")
                return False
        
        print("\n" + "="*50)
        print("✅ Setup Complete!")
        print("="*50)
        print("\nNext steps:")
        print("1. Edit .env with your credentials")
        print("2. Activate venv:")
        if sys.platform == "win32":
            print("   venv\\Scripts\\activate.bat")
        else:
            print("   source venv/bin/activate")
        print("3. Run: python run.py")
        print("\n🎉 Good luck!")
        return True

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        setup = Setup()
        
        if command == "venv":
            setup.create_venv()
        elif command == "install":
            setup.install_dependencies()
        elif command == "env":
            setup.setup_env()
        else:
            print(f"Unknown command: {command}")
            print("Available: venv, install, env")
    else:
        setup = Setup()
        setup.run_full_setup()

if __name__ == "__main__":
    main()
