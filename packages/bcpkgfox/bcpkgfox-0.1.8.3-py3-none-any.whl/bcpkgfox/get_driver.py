from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import undetected_chromedriver as uc
import random
import sys
import os

# 1. Alterar o User-Agent
def set_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    ]
    return random.choice(user_agents)

def launch_browser(download_dir):
    # Configurações para o Chrome
    options = uc.ChromeOptions()

    # Alterar o User-Agent
    options.add_argument(f"user-agent={set_user_agent()}")

    # Default's
    profile = {
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'download.default_directory': download_dir,
    }
    options.add_experimental_option('prefs', profile)

    # Configurações para reduzir detecção
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-infobars')
    # options.add_argument('--disable-extensions') # Fix: Possibilita ter extensões ou não, nunca influenciou na detecção

    # Inicializar o navegador com undetected_chromedriver
    driver = uc.Chrome(options=options, use_subprocess=True)
    stealth(driver,
        user_agent=set_user_agent(),
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver