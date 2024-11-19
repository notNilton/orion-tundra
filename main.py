import tkinter as tk
from tkinter import messagebox
from pynput import mouse
import threading
import datetime
import os
from PIL import ImageGrab

# Configuração de caminhos
BASE_DIR = os.path.dirname(__file__)
LOG_FILE = os.path.join(BASE_DIR, "log.txt")
TEMP_FOLDER = os.path.join(BASE_DIR, "temp-print")
os.makedirs(TEMP_FOLDER, exist_ok=True)

listener = None

def log_message(message, to_file=True):
    """Escreve log no terminal e opcionalmente em arquivo."""
    print(message)
    if to_file:
        with open(LOG_FILE, "a") as file:
            file.write(f"{message}\n")

def capture_screen(click_id):
    """Captura a tela e salva no diretório 'temp-print'."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(TEMP_FOLDER, f"click_{click_id}_{timestamp}.png")
    ImageGrab.grab().save(path)
    log_message(f"Print salvo: {path}", to_file=False)

def on_click(x, y, button, pressed):
    """Callback para cliques do mouse."""
    action = "Pressed" if pressed else "Released"
    log_message(f"{datetime.datetime.now()} - {action} {button} at ({x}, {y})")
    if pressed:
        capture_screen(button.name)

def toggle_capturing(start=True):
    """Controla o estado do listener."""
    global listener
    if start:
        if listener and listener.running:
            return messagebox.showinfo("Informação", "A captura já está em execução!")
        listener = mouse.Listener(on_click=on_click)
        threading.Thread(target=listener.start, daemon=True).start()
        messagebox.showinfo("Informação", "Captura iniciada!")
    elif listener:
        listener.stop()
        listener = None
        messagebox.showinfo("Informação", "Captura encerrada!")

def create_gui():
    """Cria a interface gráfica."""
    root = tk.Tk()
    root.title("Capturador de Cliques")
    root.geometry("300x150")

    tk.Label(root, text="Captura de Cliques do Mouse", font=("Arial", 12)).pack(pady=10)
    tk.Button(root, text="Iniciar Captura", command=lambda: toggle_capturing(True), width=20).pack(pady=5)
    tk.Button(root, text="Parar Captura", command=lambda: toggle_capturing(False), width=20).pack(pady=5)
    root.mainloop()

if __name__ == "__main__":
    create_gui()
