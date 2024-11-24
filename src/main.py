import ctypes
import threading
import time
import keyboard
from pynput.keyboard import Controller as KeyboardController
from utils.check import check_brighter_shores, check_in_combat
from utils.act import move_mouse
from utils.mouse_utils import get_mouse_position
from utils.monitor import monitor_stop_event
from modes.simpleclick import simpleclick_mode
from prototype import prototype_mode

mouse_keyboard = KeyboardController()

# Define a estrutura POINT usada pelo Windows para representar coordenadas (x, y)
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def print_mouse_position_mode(stop_event):
    """
    Imprime a posição do mouse a cada segundo.
    """
    print("Pressione Ctrl+F10 para encerrar o modo de impressão da posição do mouse.")
    while not stop_event.is_set():
        x, y = get_mouse_position()
        print(f"Posição atual do mouse: x={x}, y={y}")
        time.sleep(1)
    print("Modo de impressão da posição do mouse encerrado.")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Gerencia modos de execução.")
    parser.add_argument("--prototype", action="store_true", help="Executa o modo prototype.")
    parser.add_argument("--simpleclick", action="store_true", help="Executa o modo simpleclick.")
    parser.add_argument("--mouseposition", action="store_true", help="Imprime a posição do mouse a cada segundo.")
    args = parser.parse_args()

    stop_event = threading.Event()
    threading.Thread(target=monitor_stop_event, args=(stop_event,), daemon=True).start()

    if args.prototype:
        print("Modo CLI: Prototype iniciado.")
        prototype_mode(stop_event)
    elif args.simpleclick:
        print("Modo CLI: Simpleclick iniciado.")
        simpleclick_mode(stop_event)
    elif args.mouseposition:
        print("Modo CLI: Impressão da posição do mouse iniciado.")
        print_mouse_position_mode(stop_event)
    else:
        print("Nenhum modo selecionado. Use --prototype, --simpleclick ou --print-mouse-position.")

    print("Programa encerrado.")

if __name__ == "__main__":
    main()