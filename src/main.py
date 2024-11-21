import argparse
import threading
import time
import keyboard  # Para detectar teclas globalmente
from ui.gui import create_gui
import pygetwindow as gw  # Para listar janelas abertas
import cv2
import numpy as np
from PIL import ImageGrab


def monitor_stop_event(stop_event):
    """
    Monitora teclas globais para acionar o evento de parada.
    """
    print("Pressione Ctrl+F10 para encerrar o programa.")
    keyboard.add_hotkey("ctrl+f10", lambda: [print("Ctrl+F10 pressionado. Encerrando..."), stop_event.set()])


def check_image_in_window(window_rect, template_path):
    """
    Verifica se a imagem especificada está visível dentro da janela.

    Args:
        window_rect (tuple): Coordenadas da janela (left, top, right, bottom).
        template_path (str): Caminho para a imagem do template a ser localizado.

    Returns:
        bool: True se a imagem for encontrada, False caso contrário.
    """
    try:
        # Captura a região da janela
        screen = ImageGrab.grab(bbox=window_rect)
        screen_np = np.array(screen)
        screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)

        # Carrega a imagem do template
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print("Erro: Template não encontrado ou inválido.")
            return False

        # Realiza a correspondência de padrões
        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        # Define o limiar de correspondência
        threshold = 0.8
        return max_val >= threshold
    except Exception as e:
        print(f"Erro ao verificar imagem: {e}")
        return False


def check_window_visibility():
    """
    Verifica se o programa 'Brighter Shores' está visível ou minimizado na tela.
    """
    template_path = "./data/example-data/image-backpack.png"  # Atualize com o caminho correto da imagem

    while True:
        windows = gw.getAllWindows()  # Obtém todas as janelas
        found = False
        for window in windows:
            if window.title.strip() and "Brighter Shores" in window.title:
                found = True
                if window.isMinimized:
                    print("Brighter Shores está minimizado.")
                else:
                    print("Brighter Shores está visível na tela.")
                    # Verifica se a imagem está presente na janela
                    window_rect = (window.left, window.top, window.right, window.bottom)
                    if check_image_in_window(window_rect, template_path):
                        print("Mochila disponível.")
                    else:
                        print("Mochila não encontrada.")
                break
        if not found:
            print("Brighter Shores não está aberto.")
        time.sleep(5)  # Aguarda 5 segundos antes de verificar novamente


def main():
    """
    Função principal que gerencia os modos de execução do programa.
    """
    parser = argparse.ArgumentParser(description="Programa para monitorar a visibilidade de 'Brighter Shores'.")
    parser.add_argument(
        "--interface",
        action="store_true",
        help="Monitora se o programa 'Brighter Shores' está visível ou minimizado."
    )
    args = parser.parse_args()

    # Evento para parar o programa
    stop_event = threading.Event()

    # Inicia o monitoramento do atalho de teclado em um thread separado
    threading.Thread(target=monitor_stop_event, args=(stop_event,), daemon=True).start()

    if args.interface:
        print("Modo CLI: Monitorando a visibilidade de 'Brighter Shores'.")
        threading.Thread(target=check_window_visibility, daemon=True).start()
    else:
        print("Modo GUI: Iniciando a interface gráfica.")
        create_gui()

    # Aguarda a sinalização do evento de parada
    stop_event.wait()
    print("Programa encerrado.")


if __name__ == "__main__":
    main()
