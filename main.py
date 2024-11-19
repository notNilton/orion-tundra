import tkinter as tk
from tkinter import messagebox
from pynput import mouse, keyboard
import threading
import datetime
import os
from PIL import ImageGrab
import time
import pyautogui

# Configuração de caminhos
BASE_DIR = os.path.dirname(__file__)
LOG_FILE = os.path.join(BASE_DIR, "log.txt")
SCRIPT_FILE = os.path.join(BASE_DIR, "saved-script.txt")
TEMP_FOLDER = os.path.join(BASE_DIR, "temp-print")
os.makedirs(TEMP_FOLDER, exist_ok=True)

listener = None
hotkey_listener = None

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

def save_click(x, y, button, pressed):
    """Grava os cliques no arquivo de script."""
    if pressed:
        with open(SCRIPT_FILE, "a") as file:
            file.write(f"{x},{y},{button.name}\n")

def run_script():
    """Reproduz os cliques salvos no arquivo de script."""
    if not os.path.exists(SCRIPT_FILE):
        messagebox.showerror("Erro", "Nenhum script salvo encontrado!")
        return
    
    with open(SCRIPT_FILE, "r") as file:
        actions = file.readlines()
    
    for action in actions:
        try:
            x, y, button = action.strip().split(",")
            x, y = int(x), int(y)
            pyautogui.click(x=x, y=y, button=button)
            time.sleep(0.1)  # Pequeno delay entre os cliques
        except Exception as e:
            log_message(f"Erro ao executar clique: {e}", to_file=False)

    messagebox.showinfo("Informação", "Script executado com sucesso!")

def on_click(x, y, button, pressed):
    """Callback para capturar os cliques do mouse."""
    action = "Pressed" if pressed else "Released"
    log_message(f"{datetime.datetime.now()} - {action} {button} at ({x}, {y})")
    if pressed:
        capture_screen(button.name)
        save_click(x, y, button, pressed)

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

def listen_hotkey():
    """Escuta a combinação de teclas CTRL+F2 para rodar o script."""
    def on_press(key):
        try:
            if key == keyboard.Key.f2 and keyboard.Controller().ctrl_pressed:
                run_script()
        except AttributeError:
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def create_gui():
    """Cria a interface gráfica."""
    root = tk.Tk()
    root.title("Capturador de Cliques")
    root.geometry("300x200")

    tk.Label(root, text="Captura de Cliques do Mouse", font=("Arial", 12)).pack(pady=10)
    tk.Button(root, text="Iniciar Captura", command=lambda: toggle_capturing(True), width=20).pack(pady=5)
    tk.Button(root, text="Parar Captura", command=lambda: toggle_capturing(False), width=20).pack(pady=5)
    tk.Button(root, text="Rodar Script", command=run_script, width=20).pack(pady=5)

    # Iniciar a escuta da hotkey em outra thread
    threading.Thread(target=listen_hotkey, daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    create_gui()
