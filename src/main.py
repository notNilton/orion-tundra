import argparse
import threading
import time
import keyboard  # Para detectar teclas globalmente
from ui.gui import create_gui
import pygetwindow as gw  # Para listar janelas abertas


def monitor_stop_event(stop_event):
    """
    Monitora teclas globais para acionar o evento de parada.
    """
    print("Pressione Ctrl+F10 para encerrar o programa.")
    keyboard.add_hotkey("ctrl+f10", lambda: [print("Ctrl+F10 pressionado. Encerrando..."), stop_event.set()])


def check_window_visibility():
    """
    Verifica se o programa 'Brighter Shores' está visível ou minimizado na tela.
    """
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
