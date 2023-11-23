import time
import pyautogui
import os

def KeepSearchingImageAndClickWhenFound(image):
    # Localize o caminho da imagem
    image_path = os.path.join("Images", image)

    while True:
        try:
            # Tente localizar a posição da imagem
            image_position = pyautogui.locateOnScreen(image_path, confidence=0.8)

            # Se a imagem for encontrada, clique nela
            if image_position:
                image_center = pyautogui.center(image_position)
                pyautogui.click(image_center.x, image_center.y)
                if image == "Aceitar.png":
                    time.sleep(5)
                break  # Saia do loop após clicar na imagem
        except Exception as e:
            None

        # Aguarde um curto período antes de tentar novamente
        time.sleep(0.5)

KeepSearchingImageAndClickWhenFound("Aceitar.png")