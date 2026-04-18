import os
import sys
import subprocess

if __name__ == "__main__":
    # Aggiungi la cartella corrente al path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Avvia Streamlit
    subprocess.call([
        sys.executable, 
        "-m", 
        "streamlit", 
        "run", 
        "app/main.py",
        "--server.headless=true",
        "--server.port=8501",
        "--server.address=127.0.0.1"
    ])