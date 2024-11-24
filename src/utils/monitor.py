import keyboard

def monitor_stop_event(stop_event):
    """
    Monitora o atalho Ctrl+F10 para encerrar o programa.
    """
    print("Pressione Ctrl+F10 para encerrar o programa.")
    keyboard.add_hotkey("f3", lambda: stop_event.set())
