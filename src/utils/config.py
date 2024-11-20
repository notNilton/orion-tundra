import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOG_FILE = os.path.join(BASE_DIR, "log.txt")
SCRIPT_FILE = os.path.join(BASE_DIR, "data", "saved-script.txt")
TEMP_FOLDER = os.path.join(BASE_DIR, "data", "temp-print")

# Criar pasta de capturas se não existir
os.makedirs(TEMP_FOLDER, exist_ok=True)

