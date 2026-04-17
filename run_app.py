import subprocess
import sys
import os

if __name__ == "__main__":
    # Avvia Streamlit in modalità desktop
    script_path = os.path.join(os.path.dirname(__file__), "app", "main.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", script_path, "--server.headless=true"])