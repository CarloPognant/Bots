import pyautogui
import json
import time
import os
import keyboard  # Assicurati di avere installato il modulo `keyboard`

CONFIG_PATH = "config.json"

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    print(f"✅ Config salvato in '{CONFIG_PATH}'.")

def wait_for_keypress(key='s'):
    print(f"👉 Premi '{key.upper()}' per salvare la posizione...")
    while True:
        if keyboard.is_pressed(key):
            time.sleep(0.3)  # previene doppio input
            return

def get_area_coordinates():
    print("🖱️ Posiziona il mouse sul punto IN ALTO A SINISTRA dell’area e premi 'S'...")
    wait_for_keypress('s')
    x1, y1 = pyautogui.position()
    print(f"🔹 Primo punto: ({x1}, {y1})")

    print("🖱️ Ora posiziona il mouse sul punto IN BASSO A DESTRA dell’area e premi 'S'...")
    wait_for_keypress('s')
    x2, y2 = pyautogui.position()
    print(f"🔸 Secondo punto: ({x2}, {y2})")

    x = min(x1, x2)
    y = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    return x, y, width, height

def main():
    config = load_config()

    name = input("✏️ Inserisci il nome dell’area (es: card_area, rematch_button, ok_area): ").strip()
    x, y, w, h = get_area_coordinates()
    config[name] = [x, y, w, h]

    print(f"📍 Area '{name}' salvata: ({x}, {y}, {w}, {h})")
    save_config(config)

if __name__ == "__main__":
    main()
