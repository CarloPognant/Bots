import pyautogui
import keyboard
from pynput.keyboard import Key, Controller
import time

print("Comandi:")
print("    - Premi 'e' per cominciare combo con strike")
print("    - Premi 'q'per iniziare con le arts")
print("ESC - Esci dal programma")

while True:
    if keyboard.is_pressed('e'):
        print("Inizio combo con strike...")
        keyboard.press('w')
        time.sleep(0.15)
        keyboard.release('w')
        time.sleep(0.35)
        keyboard.press('a')
        time.sleep(0.1)
        keyboard.release('a')
    else:
        if keyboard.is_pressed('q'):
            print("Inizio combo con arts...")
            keyboard.press('g')
            keyboard.release('g')
            time.sleep(1.5)
            keyboard.press('w')
            time.sleep(0.15)
            keyboard.release('w')
            time.sleep(0.1)
            keyboard.press('space')
            time.sleep(0.5)
            keyboard.release('space')
            keyboard.press('h')
            keyboard.release('h')
        elif keyboard.is_pressed('esc'):
            print("Uscita dal programma...")
            break
    