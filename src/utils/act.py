import time
import keyboard
import time
import math
import random
from pynput.mouse import Controller, Button

mouse = Controller()  # Inicializa o controlador do mouse


def press_spacebar(window):
    """
    Ativa a janela do Brighter Shores e simula o pressionamento da barra de espaço.

    Args:
        window: Objeto da janela do Brighter Shores.
    """
    try:
        # Ativa a janela
        window.activate()
        time.sleep(0.1)  # Pequeno delay para garantir o foco

        # Pressiona a barra de espaço
        keyboard.send("space")
        print("Barra de espaço pressionada na janela do Brighter Shores.")
    except Exception as e:
        print(f"Erro ao pressionar a barra de espaço: {e}")

def move_mouse(start, end, duration=0.2, click=True):
    """
    Move o mouse suavemente de uma posição inicial para uma posição final com aceleração,
    curvamento, aleatoriedade e realiza um clique opcional.

    Args:
        start (tuple): Posição inicial (x, y).
        end (tuple): Posição final (x, y).
        duration (float): Duração do movimento em segundos.
        click (bool): Se True, realiza um clique ao final do movimento.
    """
    x1, y1 = start
    x2, y2 = end
    x2 += 0  # Ajuste de +50 pixels no eixo X
    y2 += 0  # Ajuste de +50 pixels no eixo Y
    steps = max(10, int(duration * 100))  # Divide o movimento em passos para suavidade
    curve_offset = random.uniform(0, 0)  # Adiciona um desvio para curvatura

    for i in range(steps + 1):
        t = i / steps  # Proporção atual do movimento (0 a 1)
        t = t * t * (3 - 2 * t)  # Suavização (ease in-out)

        # Calcular a posição intermediária com curvamento
        xt = int(x1 + (x2 - x1) * t + curve_offset * math.sin(math.pi * t))
        yt = int(y1 + (y2 - y1) * t + curve_offset * math.sin(math.pi * t))

        # Adiciona leve aleatoriedade
        xt += random.randint(-1, 1)
        yt += random.randint(-1, 1)

        mouse.position = (xt, yt)  # Move o mouse para a posição calculada
        time.sleep(duration / steps)  # Pequeno atraso entre os passos

    if click:
        mouse.position = (x2, y2)  # Certifique-se de que o mouse está na posição final ajustada
        mouse.click(Button.left)  # Realiza um clique com o botão esquerdo
        print(f"Mouse clicado em: ({x2}, {y2})")