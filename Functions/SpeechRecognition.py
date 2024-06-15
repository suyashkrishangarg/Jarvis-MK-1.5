from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import time as t
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import colorama
from os import getcwd
from playaudio import playaudio
from mtranslate import translate
import sys
import io

colorama.init(autoreset=True)

class FilteredStream(io.TextIOWrapper):
    def write(self, data):
        if "ERROR:ssl_client_socket_impl.cc" in data or "DevTools listening on" in data:
            return
        super().write(data)
sys.stdout = FilteredStream(sys.stdout.buffer, encoding='utf-8')

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.page_load_strategy = 'eager'
chrome_options.add_argument("--enable-tcp-caching")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--log-level=3')

# Initialize Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Website URL
# website = "https://663381dffa96bfc03108fa69--genuine-duckanoo-f5df47.netlify.app/"
website = f"{getcwd()}\\Functions\\Listen.html"

driver.get(website)
L = 0

# Function for speech recognition
def speechrecognition(Print=True, Translate=False):
    global L
    driver.get(website)
    driver.find_element(by=By.ID, value='start').click()
    if Print:
        print(colorama.Fore.MAGENTA + "Listening...")
        playaudio('Resources\\notification1.mp3')
    final_text = ""
    previous_text = ""
    if Print:
        print(colorama.Fore.GREEN + "==> You Said: ", end="")
    text = ""

    while True:
        text = driver.find_element(by=By.ID, value='output').text
        length = len(previous_text)
        if "<ended>" in text:
            print('\n')
            break

        if Print:
            print(colorama.Fore.LIGHTGREEN_EX + text[length:], end="", flush=True)
            
        final_text += text[length:]
        previous_text = text
        L = t()

    if Translate:
        L = t()
        final_text = translate(final_text, "en", "hi")
        if Print:
            print(colorama.Fore.CYAN + "==> Translated: " + final_text, end="")
            time_taken = str(t() - L)[:4]
            print(f"\nTranslating Time: {time_taken}s\n")

    return final_text.lower()

print("==> Speech Recognition Loaded!")

if __name__ == "__main__":
    while True:
        speechrecognition(Translate=False)
