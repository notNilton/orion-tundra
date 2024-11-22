import pygetwindow as gw
import time
import argparse
import threading
import keyboard

def monitor_stop_event(stop_event):
    print("Pressione Ctrl+F10 para encerrar o programa.")
    keyboard.add_hotkey("ctrl+f10", stop_event.set)

def check_brighter_shores():
    while True:
        for window in gw.getAllWindows():
            if "Brighter Shores" in window.title.strip():
                if window.isMinimized:
                    print("Brighter Shores minimizado.")
                else:
                    print("Brighter Shores visível.")
                break
        else:
            print("Brighter Shores não aberto.")
        time.sleep(1)

def main():
    parser = argparse.ArgumentParser(description="Verifica se 'Brighter Shores' está aberto.")
    parser.add_argument("--interface", action="store_true", help="Monitorar 'Brighter Shores'.")
    args = parser.parse_args()
    stop_event = threading.Event()
    threading.Thread(target=monitor_stop_event, args=(stop_event,), daemon=True).start()
    if args.interface:
        print("Monitorando 'Brighter Shores'.")
        threading.Thread(target=check_brighter_shores, daemon=True).start()
    stop_event.wait()

if __name__ == "__main__":
    main()
