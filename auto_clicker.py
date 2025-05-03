import cv2
import numpy as np
import mss
import pyautogui
import time
import threading

template_path = "image.png"
template_color = cv2.imread(template_path, cv2.IMREAD_COLOR)

if template_color is None:
    raise FileNotFoundError(f"can't find the file: {template_path}")

template = cv2.cvtColor(template_color, cv2.COLOR_BGR2GRAY)
template_h, template_w = template.shape[:2]

region = {"top": 0, "left": 0, "width": 0, "height": 0}  # change this

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

def click_async(x, y):
    threading.Thread(target=pyautogui.click, args=(x, y), daemon=True).start()

def auto_click():
    last_click_time = 0
    debounce_interval = 0

    with mss.mss() as sct:
        while True:
            screen = np.array(sct.grab(region))
            gray_screen = cv2.cvtColor(screen[..., :3], cv2.COLOR_BGR2GRAY)

            result = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val >= 0.73:
                now = time.time()
                if now - last_click_time > debounce_interval:
                    x, y = max_loc
                    center_x = x + template_w // 2 + region['left']
                    center_y = y + template_h // 2 + region['top']
                    click_async(center_x, center_y)
                    last_click_time = now

if __name__ == "__main__":
    try:
        auto_click()
        
    except KeyboardInterrupt:
        print("Killed")
