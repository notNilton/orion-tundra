from pynput import keyboard
from core.script import run_script

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
