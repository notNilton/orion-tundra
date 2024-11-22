import os
import time
import datetime
from PIL import ImageGrab
from pynput import mouse
from tkinter import messagebox
import pyautogui
from utils.logger import log_message
from utils.config import LOG_FILE, SCRIPT_FILE, TEMP_FOLDER, BASE_DIR
from utils.screen_checker import check_screen

listener = None

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
        listener.start()
        log_message("Captura iniciada!")
    elif listener:
        listener.stop()
        listener = None
        log_message("Captura encerrada!")


def run_screen_checker():
    """Executa o verificador de tela."""
    # Caminho para a imagem do item a ser localizado
    template_path = os.path.join(BASE_DIR, "data", "example-data", "image-backpack.png")

    try:
        # Chama a função de verificação de tela
        check_screen(template_path)
    except Exception as e:
        log_message(f"Erro ao executar o verificador de tela: {e}")
        print(f"Erro ao executar o verificador de tela: {e}")
