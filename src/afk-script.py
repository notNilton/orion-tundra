import argparse
import threading
import time
import keyboard
import pygetwindow as gw
import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract
import os
from pynput.mouse import Controller, Button
import random

mouse = Controller()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def monitor_stop_event(stop_event):
    print("Pressione Ctrl+F10 para encerrar o programa.")
    keyboard.add_hotkey("ctrl+f10", stop_event.set)

def find_text_in_window(window_rect, target_text):
    try:
        screen = cv2.cvtColor(np.array(ImageGrab.grab(bbox=window_rect)), cv2.COLOR_BGR2GRAY)
        _, processed = cv2.threshold(screen, 150, 255, cv2.THRESH_BINARY)
        data = pytesseract.image_to_data(processed, output_type=pytesseract.Output.DICT, config='--oem 3 --psm 6')
        for i, word in enumerate(data["text"]):
            if target_text.lower() in word.lower():
                x = data["left"][i] + data["width"][i] // 2
                y = data["top"][i] + data["height"][i] // 2
                return True, (x, y)
        return False, None
    except Exception as e:
        print(f"Erro ao verificar texto: {e}")
        return False, None

def smooth_move_mouse(start, end, duration=0.5):
    x1, y1, x2, y2 = *start, *end
    steps = max(10, int(duration * 100))
    for i in range(steps + 1):
        t = (i / steps) ** 2 * (3 - 2 * (i / steps))
        x = int(x1 + (x2 - x1) * t + random.uniform(-1, 1))
        y = int(y1 + (y2 - y1) * t + random.uniform(-1, 1))
        mouse.position = (x, y)
        time.sleep(duration / steps)

def click_in_window(window, position, text=None):
    try:
        window.activate()
        time.sleep(0.1)
        start = mouse.position
        x, y = position
        if text and text.lower() == "ragged":
            x += 50
            y += 50
        smooth_move_mouse(start, (x, y))
        mouse.click(Button.left, 1)
        print(f"Clique realizado em: {(x, y)}")
        keyboard.send('1')
    except Exception as e:
        print(f"Erro ao clicar: {e}")

def press_space_in_window(window):
    try:
        window.activate()
        time.sleep(0.1)
        keyboard.send("space")
    except Exception as e:
        print(f"Erro ao pressionar espaço: {e}")

def monitor_space_and_combat_cycle():
    while True:
        for window in gw.getAllWindows():
            if "Brighter Shores" in window.title.strip():
                if window.isMinimized:
                    print("Brighter Shores minimizado.")
                else:
                    print("Brighter Shores visível.")
                    window_rect = (window.left, window.top, window.right, window.bottom)
                    while find_text_in_window(window_rect, "Combat")[0]:
                        print("Em combate. Aguardando...")
                        time.sleep(2)
                    press_space_in_window(window)
                    found, position = find_text_in_window(window_rect, "Ragged")
                    if found:
                        click_in_window(window, position, text="Ragged")
                    else:
                        print("Ragged não encontrado.")
                break
        else:
            print("Brighter Shores não aberto.")
        time.sleep(1)

def main():
    parser = argparse.ArgumentParser(description="Monitor interações com 'Brighter Shores'.")
    parser.add_argument("--interface", action="store_true", help="Monitorar programa.")
    args = parser.parse_args()
    stop_event = threading.Event()
    threading.Thread(target=monitor_stop_event, args=(stop_event,), daemon=True).start()
    if args.interface:
        print("Monitorando 'Brighter Shores'.")
        threading.Thread(target=monitor_space_and_combat_cycle, daemon=True).start()
    else:
        print("Interface gráfica iniciando.")
    stop_event.wait()

if __name__ == "__main__":
    main()
