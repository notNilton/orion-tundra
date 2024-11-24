import time
import random
from utils.check import check_brighter_shores, check_in_combat
from utils.act import move_mouse
from utils.mouse_utils import get_mouse_position
from pynput.keyboard import Controller as KeyboardController

# Controlador do teclado
mouse_keyboard = KeyboardController()

def simpleclick_mode(stop_event):
    """
    Movimenta o mouse da posição atual para a posição final especificada,
    com uma variação aleatória nos valores finais de x e y.
    Também pressiona a tecla '1' até entrar em combate.
    """
    base_position = (1300, 550)  # Posição base final do mouse

    while not stop_event.is_set():
        window = check_brighter_shores()
        if window:
            in_combat = check_in_combat(window)
            if in_combat:
                print("Status: Em combate. Parando cliques.")
                continue
            else:
                # Obtém a posição atual do mouse
                current_mouse_pos = get_mouse_position()

                # Adiciona aleatoriedade à posição final
                random_offset_x = random.randint(0, 100)
                random_offset_y = random.randint(-100, 100)
                final_position = (
                    base_position[0] + random_offset_x,
                    base_position[1] + random_offset_y,
                )

                print(f"Movendo o mouse de {current_mouse_pos} para {final_position} e pressionando '1'.")

                # Move o mouse da posição atual para a posição final com aleatoriedade
                move_mouse(current_mouse_pos, final_position, duration=0.5, click=True)

                # Pressiona e solta a tecla '1'
                mouse_keyboard.press('1')
                mouse_keyboard.release('1')
        else:
            print("Brighter Shores não está aberto.")
        time.sleep(1)  # Espera 1 segundo antes de repetir
    print("Modo simpleclick encerrado.")
