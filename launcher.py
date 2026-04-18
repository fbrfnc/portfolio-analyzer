import os
import sys
import subprocess
import logging

def main():
    print("Avvio Portfolio Analyzer...")

    # Aggiungi il percorso corrente
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)

    # Avvia Streamlit in modo esplicito
    try:
        subprocess.Popen([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app/main.py",
            "--server.headless=true",
            "--server.port=8501",
            "--server.address=127.0.0.1",
            "--logger.level=error"
        ], creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        print("Applicazione avviata. Si dovrebbe aprire nel browser.")
    except Exception as e:
        print(f"Errore durante l'avvio: {e}")
        logging.error(str(e))
        input("Premi Invio per chiudere...")

if __name__ == "__main__":
    main()