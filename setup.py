(cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF'
diff --git a/setup.py b/setup.py
--- a/setup.py
+++ b/setup.py
@@ -0,0 +1,287 @@
+#!/usr/bin/env python3
+"""
+Setup Script for MRU Voice Chatbot
+==================================
+
+This script helps set up the MRU Voice Chatbot system with all dependencies.
+"""
+
+import subprocess
+import sys
+import os
+import platform
+
+def print_header(title):
+    print("\n" + "="*60)
+    print(f"🎯 {title}")
+    print("="*60)
+
+def run_command(command, description):
+    """Run a system command with error handling"""
+    print(f"\n🔄 {description}...")
+    try:
+        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
+        print(f"✅ {description} completed successfully!")
+        return True
+    except subprocess.CalledProcessError as e:
+        print(f"❌ Error: {description} failed!")
+        print(f"Error message: {e.stderr}")
+        return False
+
+def check_python_version():
+    """Check if Python version is compatible"""
+    version = sys.version_info
+    if version.major == 3 and version.minor >= 8:
+        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
+        return True
+    else:
+        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
+        print("Please install Python 3.8 or higher")
+        return False
+
+def install_system_dependencies():
+    """Install system-level dependencies based on OS"""
+    system = platform.system().lower()
+    
+    print(f"\n🖥️ Detected OS: {platform.system()}")
+    
+    if system == "windows":
+        print("Windows detected - most dependencies should work out of the box")
+        return True
+    elif system == "darwin":  # macOS
+        print("macOS detected - checking for brew...")
+        # Install portaudio for PyAudio
+        commands = [
+            "brew install portaudio",
+            "brew install espeak"  # For TTS alternatives
+        ]
+        for cmd in commands:
+            run_command(cmd, f"Installing {cmd.split()[-1]}")
+        return True
+    elif system == "linux":
+        print("Linux detected - installing audio dependencies...")
+        # Common Linux audio dependencies
+        commands = [
+            "sudo apt-get update",
+            "sudo apt-get install -y python3-pyaudio",
+            "sudo apt-get install -y portaudio19-dev",
+            "sudo apt-get install -y espeak espeak-data",
+            "sudo apt-get install -y pulseaudio"
+        ]
+        for cmd in commands:
+            run_command(cmd, f"Installing {cmd.split()[-1]}")
+        return True
+    else:
+        print(f"⚠️ Unknown OS: {system}")
+        print("You may need to install audio dependencies manually")
+        return True
+
+def install_python_dependencies():
+    """Install Python packages"""
+    print_header("Installing Python Dependencies")
+    
+    # Core dependencies
+    core_packages = [
+        "speechrecognition==3.10.0",
+        "pyttsx3==2.90",
+        "scikit-learn==1.3.2",
+        "numpy==1.24.3",
+        "spacy==3.7.2",
+        "requests==2.31.0"
+    ]
+    
+    for package in core_packages:
+        if not run_command(f"pip install {package}", f"Installing {package}"):
+            print(f"⚠️ Failed to install {package}, but continuing...")
+    
+    # Try to install PyAudio (can be tricky)
+    print("\n🎤 Installing PyAudio (audio processing)...")
+    if not run_command("pip install pyaudio", "Installing PyAudio"):
+        print("⚠️ PyAudio installation failed. Trying alternative method...")
+        if platform.system().lower() == "windows":
+            print("For Windows, try: pip install pipwin && pipwin install pyaudio")
+        else:
+            print("You may need to install portaudio19-dev system package first")
+    
+    # Download spaCy model
+    print("\n🧠 Downloading spaCy language model...")
+    run_command("python -m spacy download en_core_web_sm", "Downloading English language model")
+
+def test_installation():
+    """Test if the installation works"""
+    print_header("Testing Installation")
+    
+    test_code = '''
+import sys
+print("Testing core imports...")
+
+try:
+    import speech_recognition as sr
+    print("✅ speech_recognition imported successfully")
+except ImportError as e:
+    print(f"❌ speech_recognition import failed: {e}")
+
+try:
+    import pyttsx3
+    print("✅ pyttsx3 imported successfully")
+except ImportError as e:
+    print(f"❌ pyttsx3 import failed: {e}")
+
+try:
+    import spacy
+    nlp = spacy.load("en_core_web_sm")
+    print("✅ spaCy and language model loaded successfully")
+except ImportError as e:
+    print(f"❌ spaCy import failed: {e}")
+except OSError as e:
+    print(f"❌ spaCy language model not found: {e}")
+
+try:
+    import sklearn
+    print("✅ scikit-learn imported successfully")
+except ImportError as e:
+    print(f"❌ scikit-learn import failed: {e}")
+
+try:
+    import numpy
+    print("✅ numpy imported successfully")
+except ImportError as e:
+    print(f"❌ numpy import failed: {e}")
+
+print("\\n🎯 Testing audio devices...")
+try:
+    import speech_recognition as sr
+    r = sr.Recognizer()
+    mic = sr.Microphone()
+    print("✅ Microphone detected")
+except Exception as e:
+    print(f"❌ Microphone test failed: {e}")
+
+try:
+    import pyttsx3
+    engine = pyttsx3.init()
+    print("✅ Text-to-speech engine initialized")
+except Exception as e:
+    print(f"❌ TTS test failed: {e}")
+'''
+    
+    # Write test file
+    with open("test_installation.py", "w") as f:
+        f.write(test_code)
+    
+    # Run test
+    result = run_command("python test_installation.py", "Running installation test")
+    
+    # Clean up
+    if os.path.exists("test_installation.py"):
+        os.remove("test_installation.py")
+    
+    return result
+
+def create_launch_script():
+    """Create easy launch scripts"""
+    print_header("Creating Launch Scripts")
+    
+    # Create batch file for Windows
+    if platform.system().lower() == "windows":
+        batch_content = '''@echo off
+echo Starting MRU Voice Chatbot...
+python mru_chatbot_system.py
+pause
+'''
+        with open("start_chatbot.bat", "w") as f:
+            f.write(batch_content)
+        print("✅ Created start_chatbot.bat for Windows")
+    
+    # Create shell script for Unix-like systems
+    shell_content = '''#!/bin/bash
+echo "Starting MRU Voice Chatbot..."
+python3 mru_chatbot_system.py
+'''
+    with open("start_chatbot.sh", "w") as f:
+        f.write(shell_content)
+    
+    # Make shell script executable
+    if platform.system().lower() != "windows":
+        os.chmod("start_chatbot.sh", 0o755)
+        print("✅ Created start_chatbot.sh for Unix/Linux/macOS")
+
+def show_usage_instructions():
+    """Show how to use the chatbot"""
+    print_header("Usage Instructions")
+    
+    print("""
+🚀 How to Run the Chatbot:
+
+Method 1: Direct Python execution
+    python mru_chatbot_system.py
+
+Method 2: Using launch scripts
+    Windows: Double-click start_chatbot.bat
+    Linux/macOS: ./start_chatbot.sh
+
+Method 3: Run the demo
+    python demo.py
+
+🎤 Voice Commands:
+    • Speak naturally or type your questions
+    • Say "text" to switch to text mode
+    • Say "voice" to enable voice mode
+    • Say "help" for available commands
+    • Say "quit" to exit
+
+💡 Tips:
+    • Ensure your microphone is working
+    • Speak clearly for better recognition
+    • Internet connection required for speech recognition
+    • The system will fallback to text mode if voice fails
+
+📞 For Help:
+    • Check README.md for detailed instructions
+    • Run demo.py to see all features
+    • Contact: admissions@manavrachna.edu.in
+    """)
+
+def main():
+    """Main setup function"""
+    print_header("MRU Voice Chatbot Setup")
+    print("🎓 Welcome to Manav Rachna University Voice Chatbot Setup!")
+    print("This script will help you install and configure the chatbot system.")
+    
+    # Check Python version
+    if not check_python_version():
+        return False
+    
+    # Install system dependencies
+    install_system_dependencies()
+    
+    # Install Python dependencies
+    install_python_dependencies()
+    
+    # Test installation
+    if test_installation():
+        print("\n✅ Installation completed successfully!")
+    else:
+        print("\n⚠️ Installation completed with some issues.")
+        print("The chatbot may still work, but some features might be limited.")
+    
+    # Create launch scripts
+    create_launch_script()
+    
+    # Show usage instructions
+    show_usage_instructions()
+    
+    print_header("Setup Complete")
+    print("🎉 MRU Voice Chatbot is ready to use!")
+    print("Run 'python mru_chatbot_system.py' to start the chatbot.")
+    
+    return True
+
+if __name__ == "__main__":
+    try:
+        main()
+    except KeyboardInterrupt:
+        print("\n\n👋 Setup interrupted by user. Goodbye!")
+    except Exception as e:
+        print(f"\n❌ Setup failed with error: {e}")
+        print("Please check the error and try again, or install dependencies manually.")
EOF
)
