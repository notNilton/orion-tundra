import tkinter as tk
from tkinter import messagebox
from pynput import mouse
import threading
import datetime
import os

# Caminho do arquivo de log
log_file = os.path.join(os.path.dirname(__file__), "log.txt")
listener = None  # Variável global para o Listener do mouse

def write_log(message):
    """Escreve uma mensagem no arquivo de log."""
    with open(log_file, "a") as file:
        file.write(f"{message}\n")

def on_click(x, y, button, pressed):
    """Callback para capturar os cliques do mouse."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    action = "Pressed" if pressed else "Released"
    log_message = f"{timestamp} - {action} {button} at ({x}, {y})"
    print(log_message)  # Exibe no terminal
    write_log(log_message)  # Escreve no arquivo de log

def start_capturing():
    """Inicia a captura dos cliques."""
    global listener
    if listener and listener.running:
        messagebox.showinfo("Informação", "A captura já está em execução!")
        return

    # Iniciar o listener em uma nova thread
    listener = mouse.Listener(on_click=on_click)
    thread = threading.Thread(target=listener.start)
    thread.daemon = True  # Finaliza a thread ao fechar o programa
    thread.start()

    messagebox.showinfo("Informação", "Captura iniciada! Os cliques serão salvos em log.txt")

def stop_capturing():
    """Para a captura dos cliques."""
    global listener
    if listener and listener.running:
        listener.stop()
        listener = None
        messagebox.showinfo("Informação", "Captura encerrada!")
    else:
        messagebox.showinfo("Informação", "Nenhuma captura está em execução.")

# Configuração da interface gráfica
def create_gui():
    root = tk.Tk()
    root.title("Capturador de Cliques")
    root.geometry("300x150")

    label = tk.Label(root, text="Captura de Cliques do Mouse", font=("Arial", 12))
    label.pack(pady=10)

    start_button = tk.Button(root, text="Iniciar Captura", command=start_capturing, width=20)
    start_button.pack(pady=5)

    stop_button = tk.Button(root, text="Parar Captura", command=stop_capturing, width=20)
    stop_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
