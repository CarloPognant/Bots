import pyautogui
import keyboard
import time

print("Posiziona il mouse e premi 's' per salvare la posizione, ESC per uscire.")

coords = []

while True:
    if keyboard.is_pressed('s'):
        x, y = pyautogui.position()
        print(f"Salvato: ({x}, {y})")
        coords.append((x, y))
        time.sleep(0.3)  # evita lettura multipla
    elif keyboard.is_pressed('esc'):
        break

print("Coordinate salvate:")
for c in coords:
    print(c)
