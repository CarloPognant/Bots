# color_combat.py
import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
import time

# Riconoscimento HSV
COLOR_RANGES = {
    "red": [
        (np.array([0, 100, 100]), np.array([10, 255, 255])),
        (np.array([160, 100, 100]), np.array([180, 255, 255]))
    ],
    "yellow": [
        (np.array([20, 100, 100]), np.array([30, 255, 255]))
    ],
    "blue": [
        (np.array([90, 100, 100]), np.array([120, 255, 255]))
    ],
    "green": [
        (np.array([40, 100, 100]), np.array([70, 255, 255]))
    ]
}

# Ordine da seguire (modificabile)
COLOR_ORDER = ["red", "yellow", "blue", "green"]


def take_screenshot(region=None):
    if region:
        x, y, w, h = region
        bbox = (x, y, x + w, y + h)
        img = ImageGrab.grab(bbox=bbox)
    else:
        img = ImageGrab.grab()
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def detect_color_cards(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    detected = {}

    for color, ranges in COLOR_RANGES.items():
        mask_total = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for lower, upper in ranges:
            mask = cv2.inRange(hsv, lower, upper)
            mask_total = cv2.bitwise_or(mask_total, mask)

        contours, _ = cv2.findContours(mask_total, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        centers = []
        for cnt in contours:
            if cv2.contourArea(cnt) > 100:
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    centers.append((cx, cy))

        detected[color] = centers

    return detected

def click_color_cards(region=None):
    print("🎯 Riconoscimento carte in corso...")
    screenshot = take_screenshot(region)
    detected = detect_color_cards(screenshot)

    for color in COLOR_ORDER:
        if color in detected:
            for pos in detected[color]:
                print(f"🖱️ Clic su carta {color.upper()} → {pos}")
                pyautogui.moveTo(pos)
                pyautogui.click()
                time.sleep(0.2)
