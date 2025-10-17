# === IMPORT DELLE LIBRERIE ===
import pyautogui               # Per muovere il mouse e cliccare
import time                    # Per gestire i tempi di attesa
import json                    # Per leggere file di configurazione (config.json)
import keyboard                # Per rilevare tasti premuti (es. "q" per fermare il bot)
import os                      # Per operazioni su file/cartelle
import cv2                     # OpenCV: per il riconoscimento immagini veloce
import numpy as np             # Per gestire array di pixel
from PIL import ImageGrab      # Per fare screenshot veloci

# === CONFIGURAZIONE ===
CONFIDENCE = 0.65               # Soglia di riconoscimento immagini
DROP_DELAY = 0.15               # Ritardo tra un click e l’altro
IMG_DIR = "img"                 # Cartella immagini di riferimento

HERO_IMAGES = ["king.png", "queen.png", "warden.png", "champion.png"]  # Eroi in ordine di abilità
HERO_POS = {}                   # Posizioni eroi salvate
IMAGES_CACHE = {}               # Cache immagini caricate

# === CARICAMENTO IMMAGINI IN CACHE ===
print("[INFO] Caricamento immagini in memoria...")
for filename in os.listdir(IMG_DIR):
    if filename.endswith(".png"):
        path = os.path.join(IMG_DIR, filename)
        IMAGES_CACHE[filename] = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
print(f"[INFO] Immagini caricate: {list(IMAGES_CACHE.keys())}")

# === CARICA CONFIGURAZIONE DAL FILE JSON ===
with open("config.json") as f:
    CONFIG = json.load(f)
print("[INFO] Configurazione caricata.")

# === FUNZIONI BASE ===
def click(x, y, delay=DROP_DELAY):
    """Muove il mouse alla posizione (x, y) e clicca."""
    print(f"[ACTION] Click su ({x}, {y})")
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(delay)

def drop_at(pos, times=1, delay=DROP_DELAY):
    """Clicca più volte in una determinata posizione."""
    print(f"[ACTION] Drop su {pos}, {times} volte")
    pyautogui.moveTo(pos)
    for _ in range(times):
        pyautogui.click()
        time.sleep(delay)

def screenshot(region=None):
    """Cattura screenshot in scala di grigi di tutta la schermata o di una regione."""
    if region:
        x, y, w, h = region
        bbox = (x, y, x + w, y + h)
    else:
        bbox = None
    img = ImageGrab.grab(bbox=bbox)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    return img

def locate_and_click(image_name, confidence=CONFIDENCE, region=None):
    """Cerca un'immagine sullo schermo e clicca se trovata."""
    template = IMAGES_CACHE.get(image_name)
    if template is None:
        print(f"[WARN] Immagine {image_name} non trovata in cache!")
        return False

    screen = screenshot(region)
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= confidence)

    if len(loc[0]) > 0:
        y, x = loc[0][0], loc[1][0]
        h, w = template.shape
        cx, cy = x + w // 2, y + h // 2
        if region:
            cx += region[0]
            cy += region[1]
        click(cx, cy)
        if image_name in HERO_IMAGES and image_name not in HERO_POS:
            HERO_POS[image_name] = (cx, cy)
            print(f"[INFO] Posizione salvata per {image_name}: {HERO_POS[image_name]}")
        return True
    else:
        print(f"[MISS] {image_name} non trovato.")
    return False

def click_saved_hero(image_name):
    """Clicca un eroe usando le coordinate salvate."""
    pos = HERO_POS.get(image_name)
    if pos:
        print(f"[ACTION] Click eroe salvato: {image_name} a {pos}")
        click(*pos)
        return True
    return False

def activate_hero_abilities():
    """Attiva le abilità degli eroi in ordine."""
    for hero in HERO_IMAGES:
        if not click_saved_hero(hero):
            locate_and_click(hero)

# === FUNZIONI DI ATTESA ===
def wait_until_image(image_name, timeout=180, region=None):
    """Aspetta finché un'immagine appare sullo schermo (senza cliccarla)."""
    print(f"[WAIT] Aspettando {image_name}...")
    start = time.time()
    while time.time() - start < timeout:
        template = IMAGES_CACHE.get(image_name)
        if template is None:
            return False
        screen = screenshot(region)
        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= CONFIDENCE)
        if len(loc[0]) > 0:
            print(f"[FOUND] {image_name} trovato.")
            return True
        time.sleep(0.3)
    print(f"[TIMEOUT] {image_name} non trovato entro {timeout} secondi.")
    return False

def wait_for_return_home_image(timeout=180):
    """Aspetta la comparsa del tasto 'Return Home'."""
    start = time.time()
    while time.time() - start < timeout:
        if locate_and_click("return_home.png"):
            return True
        time.sleep(1)
    return False

# === DEPLOY TRUPPE ===
def deploy_troops():
    coords = CONFIG["troop_coords"]

    if locate_and_click("balloon.png", region=(0, 800, 1920, 250)):
        drop_at(coords["balloon_drop"], times=2)

    if locate_and_click("electro_dragon.png", region=(0, 800, 1920, 250)):
        for i in range(1, 10):
            drop_at(coords[f"dragon_{i}"])

    if locate_and_click("slammer.png", region=(0, 800, 1920, 250)):
        drop_at(coords["slammer_drop"])

    if locate_and_click("king.png", region=(0, 800, 1920, 250)):
        drop_at(coords["king_drop"])

    if locate_and_click("queen.png", region=(0, 800, 1920, 250)):
        drop_at(coords["king_drop"])

    if locate_and_click("warden.png", region=(0, 800, 1920, 250)):
        drop_at(coords["warden_drop"])

    if locate_and_click("champion.png", region=(0, 800, 1920, 250)):
        drop_at(coords["warden_drop"])

    if locate_and_click("rage_spell.png", region=(0, 800, 1920, 250)):
        for i in range(1, 6):
            drop_at(coords[f"rage_{i}"])
            if i in [2, 4]:
                time.sleep(7)

    if locate_and_click("freeze_spell.png", region=(0, 800, 1920, 250)):
        drop_at(coords["freeze_drop"])
        time.sleep(5)
        activate_hero_abilities()

# === MAIN LOOP ===
def main():
    time.sleep(2)  # Pausa iniziale

    locate_and_click("attack.png")
    time.sleep(1)
    locate_and_click("find.png")

    # Attesa dinamica: aspetta che compaiano le mongolfiere
    wait_until_image("balloon.png", timeout=60, region=(0, 800, 1920, 250))

    deploy_troops()

    wait_for_return_home_image()

    # Attesa dinamica: aspetta di rivedere il tasto attack
    wait_until_image("attack.png", timeout=60)

if __name__ == "__main__":
    print("[INFO] Avvio bot. Premi 'q' per fermarlo.")
    while not keyboard.is_pressed("q"):
        main()
    print("[INFO] Bot fermato.")
