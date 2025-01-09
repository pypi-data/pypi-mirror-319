from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from .find_elements import *
from .invoke_api import *
from .get_driver import *

import os

download_dir = "C:\\TMPIMGGI\\LAST_IMG\\"
download_kit = "C:\\TMPIMGKIT\\"
download_ggi = "C:\\TMPIMGGI\\"
driver = None
By = By


def create_dirs():
    """Cria os diretórios 'download_dir', 'download_kit' e 'download_ggi' se não existirem."""
    global download_dir, download_kit, download_ggi
    for directory in [download_dir, download_kit, download_ggi]:

        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f" - Diretório criado: {directory}")

def initialize_driver():
    global driver
    if driver is None:
        driver = get_driver.backcode__dont_use__launch_browser(download_dir)
        return driver

def get(link):
    global driver
    if driver != None:
        get_driver.backcode__dont_use__get(driver, link)

def find_element_with_wait(by, value, timeout=10, parent=None):
    global driver
    if driver != None:
        return find_elements.find_element_with_wait_backcode(driver, by.lower(), value, timeout, parent)

    else: raise ValueError("Error: Driver is None")

def find_elements_with_wait(by, value, timeout=10, parent=None):
    global driver
    if driver != None:
        return find_elements.find_elements_with_wait_backcode(driver, by.lower(), value, timeout, parent)

    else: raise ValueError("Error: Driver is None")

def wait_for(object, type, timeout=10):
    """
    Aguarda até que um objeto (texto, elemento ou imagem) seja encontrado na tela.

    Args:
        object (str|list): O objeto a ser procurado. Pode ser um caminho de imagem, texto ou elemento XPATH.
        type (str): O tipo de objeto a ser procurado. Pode ser 'imagem', 'texto' ou 'elemento'.
        timeout (int): limite de tempo que vai procurar o objeto, coloque 0 para não ter limite

    Exemplo:
        wait_for('C:\\Caminho\\da\\imagem.png', 'imagem')
        wait_for('Texto a ser encontrado', 'texto')
        wait_for( XPATH_AQUI, 'elemento')
    """
    global driver
    tempo = timeout

    text_type = ['texto', 'string', 'palavra', 'mensagem', 'frase', 'conteúdo', 'texto_visível', 'texto_encontrado', 'texto_display', 'label']
    element_type = [ "element", "elemento", "botao", 'element', 'web_element', 'html_element', 'ui_element', 'interface_element', 'objeto', 'widget', 'campo', 'componente']
    imagem_type = [ 'imagem', 'imagem_png', 'imagem_jpeg', 'image', 'imagem_exata', 'padrão_imagem', 'foto', 'captura_tela', 'screenshot', 'imagem_visual']

    for escrita in text_type:
        if escrita in type.lower():
            type = "text"

    for escrita in element_type:
        if escrita in type.lower():
            type = "element"

    for escrita in imagem_type:
        if escrita in type.lower():
            type = "image"

    return find_elements.backcode__dont_use__wait_for(driver, object, type, timeout=tempo)

