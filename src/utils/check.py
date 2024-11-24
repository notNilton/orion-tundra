import pygetwindow as gw
import cv2
import numpy as np
from PIL import ImageGrab
import os
import pytesseract

# Configura o caminho para o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def check_brighter_shores():
    """
    Verifica se a janela 'Brighter Shores' está aberta, minimizada ou visível.
    """
    for window in gw.getAllWindows():
        if "Brighter Shores" in window.title.strip():
            if window.isMinimized:
                print("Brighter Shores minimizado.")
            return window  # Retorna o objeto da janela encontrada
    print("Brighter Shores não aberto.")
    return None


def check_in_combat(window, template_dir="./data/combat-image", threshold=0.5):
    """
    Verifica se há uma imagem de combate presente na janela do 'Brighter Shores' e imprime todas as imagens na pasta.

    Args:
        window: Objeto da janela do Brighter Shores.
        template_dir (str): Diretório contendo as imagens de combate.
        threshold (float): Limiar de similaridade para considerar uma correspondência.

    Returns:
        bool: True se uma imagem foi encontrada, False caso contrário.
    """
    try:
        # Verifica se alguma imagem corresponde na tela
        window_rect = (window.left, window.top, window.right, window.bottom)
        screen_gray = cv2.cvtColor(np.array(ImageGrab.grab(bbox=window_rect)), cv2.COLOR_BGR2GRAY)

        for filename in os.listdir(template_dir):
            if filename.endswith(".png"):
                template_path = os.path.join(template_dir, filename)
                template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

                if template is not None:
                    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(result)

                    if max_val >= threshold:
                        return True
        return False
    except Exception as e:
        print(f"Erro ao verificar combate: {e}")
        return False

def find_word_in_window(window, target_word):
    """
    Procura pela palavra especificada na janela do Brighter Shores usando OCR.

    Args:
        window: Objeto da janela do Brighter Shores.
        target_word (str): Palavra a ser buscada na tela.

    Returns:
        tuple: (bool, position). Retorna True e a posição central da palavra encontrada (x, y),
               ou False e None caso contrário.
    """
    try:
        # Captura a região da janela
        window_rect = (window.left, window.top, window.right, window.bottom)
        screenshot = ImageGrab.grab(bbox=window_rect)
        screen_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)

        # Preprocessa a imagem
        _, processed_image = cv2.threshold(screen_gray, 150, 255, cv2.THRESH_BINARY)

        # Realiza OCR na imagem processada
        data = pytesseract.image_to_data(processed_image, output_type=pytesseract.Output.DICT, config='--oem 3 --psm 6')

        # Itera pelos textos reconhecidos
        for i, word in enumerate(data["text"]):
            if target_word.lower() in word.lower():
                x = data["left"][i] + data["width"][i] // 2 + window.left
                y = data["top"][i] + data["height"][i] // 2 + window.top
                print(f"Palavra '{target_word}' encontrada na posição ({x}, {y})")
                return True, (x, y)

        print(f"Palavra '{target_word}' não encontrada.")
        return False, None
    except Exception as e:
        print(f"Erro ao buscar a palavra '{target_word}': {e}")
        return False, None