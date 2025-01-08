from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import pyautogui
import time

def find_element_with_wait_backcode(driver, by, value, timeout, parent):
    if "css" in by:
        by = By.CSS_SELECTOR

    if parent is None:
        parent = driver  # Usa o driver principal se nenhum elemento pai for passado
    return WebDriverWait(parent, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def find_elements_with_wait_backcode(driver, by, value, timeout, parent):
    if "css" in by:
        by = By.CSS_SELECTOR

    if parent is None:
        parent = driver  # Usa o driver principal se nenhum elemento pai for passado
    return WebDriverWait(parent, timeout).until(
        EC.presence_of_all_elements_located((by, value))
    )

def move_to_image(imagens, click_on_final=False, tolerancia=1, timeout=10, repeat=False):
    """
    Move o mouse até o centro de uma imagem na tela e clica, se necessário.

    Args:
        imagens (list) : Caminho da imagem a ser localizada.
        click_on_final (bool): Se True, realiza um clique ao final.
        tolerancia (float): Tolerância para a comparação da imagem (opcional, valor padrão: 1).
        timeout (int): Tempo máximo (em segundos) para procurar a imagem antes de desistir (opcional, valor padrão: 10).

    Exemplo:
        caminho_imagem = 'C:\\User\\Caminho\\exemplo.png'
        move_to_image(caminho_imagem, click_on_final=True, tolerancia=0.9, timeout=30)

    Nota:
        Recomenda-se colocar a imagem na mesma pasta do arquivo MAIN para evitar problemas ao gerar o executável com pyinstaller e rodar em outras máquinas.
    """

    if isinstance(imagens, str):
        imagens = [imagens]

    attempts = 0
    def funcao():
        try:
            # Os for's abaixo servem para caso seja mais de uma imagem
            for imagem in imagens:
                try:
                    localizacao = pyautogui.locateOnScreen(imagem, confidence=tolerancia)
                    break
                except:
                    localizacao = None
                    continue

            if localizacao is not None:
                x = localizacao.left + round(localizacao.width / 2)
                y = localizacao.top + round(localizacao.height / 2)
                pyautogui.moveTo(x, y)

                if click_on_final:
                    pyautogui.click()
                return 1

            else: raise FileNotFoundError()

        except Exception as e:
            attempts += 1
            ultima_excecao = e
            time.sleep(1)

    if repeat == True:
        while True:
            if funcao() == 1:
                return
    else:
        while attempts < timeout:
            if funcao() == 1:
                return

    # Se todas as tentativas falharem, levanta erro
    raise ValueError(f"Erro ao procurar a imagem '{imagens}' após 10 tentativas.") from ultima_excecao