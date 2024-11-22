import tkinter as tk
from tkinter import messagebox
import threading
from core.script import toggle_capturing, run_script
from core.hotkey import listen_hotkey
from core.script import run_screen_checker

def create_gui():
    """Cria a interface gráfica."""
    root = tk.Tk()
    root.title("Capturador de Cliques")
    root.geometry("300x250")

    tk.Label(root, text="Captura de Cliques do Mouse", font=("Arial", 12)).pack(pady=10)
    tk.Button(root, text="Iniciar Captura", command=lambda: toggle_capturing(True), width=20).pack(pady=5)
    tk.Button(root, text="Parar Captura", command=lambda: toggle_capturing(False), width=20).pack(pady=5)
    tk.Button(root, text="Rodar Script", command=run_script, width=20).pack(pady=5)
    tk.Button(root, text="Verificar Tela", command=run_screen_checker, width=20).pack(pady=5)  # Novo botão

    # Iniciar a escuta da hotkey em outra thread
    threading.Thread(target=listen_hotkey, daemon=True).start()
    root.mainloop()
