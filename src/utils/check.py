import os
import cv2
import numpy as np
from PIL import ImageGrab

def check_images_in_window(window_rect, template_dir, threshold=0.8):
    """
    Verifica se alguma imagem do diretório de templates aparece dentro da janela.

    Args:
        window_rect (tuple): Coordenadas da janela (left, top, right, bottom).
        template_dir (str): Caminho para o diretório de imagens.
        threshold (float): Limiar de similaridade para considerar uma correspondência.

    Returns:
        tuple: (bool, float, str). True se uma imagem for encontrada, porcentagem de similaridade, e o nome do arquivo correspondente.
    """
    try:
        screen_gray = cv2.cvtColor(np.array(ImageGrab.grab(bbox=window_rect)), cv2.COLOR_BGR2GRAY)
        for filename in os.listdir(template_dir):
            if filename.endswith(".png"):
                template_path = os.path.join(template_dir, filename)
                template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
                if template is not None:
                    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(result)
               
                    if max_val >= threshold:
                        print(f"Imagem correspondente encontrada: {filename} (similaridade: {max_val:.2f})")
                        return True, max_val, filename

        return False, 0, None
    except Exception as e:
        print(f"Erro ao verificar imagens: {e}")
        return False, 0, None
