import json
import time
from PIL import ImageGrab
import numpy as np
import cv2
import pytesseract
import pyautogui

# === CONFIG ===
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

with open("config.json") as f:
    CONFIG = json.load(f)

def click(x, y, delay=0.5):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(delay)

def wait_for_ok_text(area, timeout=240):
    start_time = time.time()
    while time.time() - start_time < timeout:
        x, y, w, h = area
        screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        screenshot_np = np.array(screenshot)
        gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        custom_config = r'--psm 8'
        text = pytesseract.image_to_string(thresh, config=custom_config).strip().lower()
        print(f"[OCR RAW] '{text}'")

        if "rematch" in text:
            return True
        time.sleep(1)
    return False

def repeat_mission(n=5):
    for i in range(n):
        print(f"\n🔁 Ciclo {i+1}/{n}")
        print("⏳ Aspetto 'OK'...")
        if wait_for_ok_text(CONFIG["rematch_area"]):
            print("✅ Rematch trovato. Clicco...")
            click(*CONFIG["rematch_button"])
        else:
            print("❌ Timeout senza trovare OK.")
        print("⏱️ Aspetto 5 secondi prima della ripetizione.")
        time.sleep(5)

if __name__ == "__main__":
    n = int(input("Quante volte vuoi ripetere la missione? "))
    repeat_mission(n)
