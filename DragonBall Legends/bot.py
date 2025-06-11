import pyautogui
import pytesseract
import time
import json
import cv2
import numpy as np
from PIL import ImageGrab
import os

# === CONFIG ===
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

with open("config.json") as f:
    CONFIG = json.load(f)

with open("cutscenes.json") as f:
    CUTSCENES = json.load(f)["cutscenes"]

with open("progress.json") as f:
    PROGRESS = json.load(f)

with open("structure.json") as f:
    STRUCTURE = json.load(f)["structure"]


def is_cutscene(part, book, chapter):
    return any(
        c["part_number"] == part and
        c["book_number"] == book and
        c["chapter_number"] == chapter
        for c in CUTSCENES
    )

def click(x, y, delay=0.5):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(delay)

# ✅ OCR integrato nel file
def wait_for_ok_text(area, timeout=180):
    start_time = time.time()
    while time.time() - start_time < timeout:
        x, y, w, h = area
        screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        screenshot_np = np.array(screenshot)

        # Salva immagine originale per confronto
        cv2.imwrite("ocr_original.png", screenshot_np)

        gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # cv2.imwrite("ocr_thresh_debug.png", thresh)  # opzionale
        cv2.imwrite("ocr_debug.png", thresh)

        custom_config = r'--psm 8'
        text = pytesseract.image_to_string(thresh, config=custom_config).strip().lower()
        print(f"[OCR RAW] '{text}'")

        if "ok" in text:
            return True
        time.sleep(1)
    return False




def handle_cutscene():
    print("🎬 Cutscene detected. Trying to skip...")
    time.sleep(5)
    click(*CONFIG["skip_button"])
    time.sleep(2)
    click(*CONFIG["post_battle_clicks"][2])
    # Se vuoi, puoi espandere qui con controlli OCR in futuro

def advance_progress():
    part = PROGRESS["part_number"]
    book = PROGRESS["book_number"]
    chapter = PROGRESS["chapter_number"]

    current_book_chapters = STRUCTURE[str(part)][book - 1]

    if chapter < current_book_chapters:
        PROGRESS["chapter_number"] += 1
    else:
        total_books = len(STRUCTURE[str(part)])
        if book < total_books:
            PROGRESS["book_number"] += 1
            PROGRESS["chapter_number"] = 1
        else:
            # Fine della parte attuale
            if str(part + 1) in STRUCTURE:
                PROGRESS["part_number"] += 1
                PROGRESS["book_number"] = 1
                PROGRESS["chapter_number"] = 1
            else:
                print("✅ Fine di tutte le parti. Bot terminato.")
                exit()

    with open("progress.json", "w") as f:
        json.dump(PROGRESS, f, indent=2)

    print("✅ Avanzato a -> Part {part} Book {book} Chapter {chapter}")


def run_battle_cycle():
    part = PROGRESS["part_number"]
    book = PROGRESS["book_number"]
    chapter = PROGRESS["chapter_number"]

    print(f"\n➡️ Part {part} - Book {book} - Chapter {chapter}")

    if is_cutscene(part, book, chapter):
        handle_cutscene()
    else:
        print("▶️ Battle phase starting...")

        time.sleep(5)
        print("🖱️ Removing demo...")
        click(*CONFIG["demo_button"], delay=0.2)

        print("🖱️ Clicking Start Battle...")
        click(*CONFIG["start_battle"], delay=5)

        print("🧙 Selecting characters...")
        click(*CONFIG["character_slots"][0], delay=0.2)
        click(*CONFIG["character_slots"][1], delay=0.2)
        click(*CONFIG["character_slots"][2], delay=0.2)
        click(*CONFIG["character_slots"][3], delay=0.2)

        print("🟢 Clicking Ready...")
        click(*CONFIG["ready_button"])

        print("⏳ Waiting for battle to finish and 'OK' to appear...")
        if not wait_for_ok_text(CONFIG["ok_area"]):
            print("❌ Timeout waiting for OK.")
        else:
            print("✅ 'OK' detected.")
            click(*CONFIG["post_battle_clicks"][0])

        time.sleep(3)
        click(*CONFIG["post_battle_clicks"][0])
        time.sleep(0.2)
        click(*CONFIG["post_battle_clicks"][1])
        time.sleep(0.2)
        click(*CONFIG["post_battle_clicks"][2])

    advance_progress()

if __name__ == "__main__":
    while True:
        run_battle_cycle()
        print("\n⏱️ Attesa 5 secondi prima del prossimo ciclo...")
        time.sleep(5)

