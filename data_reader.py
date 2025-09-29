import pygame
import mss
import cv2
import numpy as np
import time
from datetime import datetime
import os

# ===============================
# CONFIG
# ===============================
SAVE_DIR = "driving_dataset_2"
FPS = 10  # frames per second to capture (10 = every 100ms)
MAX_ROTATION = 450  # Logitech G920 is ±450 degrees
# ===============================

# Make dataset directory
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# Initialize steering wheel (Logitech G920)
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Detected controller: {joystick.get_name()}")

# Initialize screen capture
sct = mss.mss()
# Print available monitors to debug
print("Available monitors:")
for i, monitor in enumerate(sct.monitors):
    print(f"Monitor {i}: {monitor}")

# Try to capture the primary monitor (usually index 1)
monitorIndex = 0
monitor = sct.monitors[monitorIndex]  # capture primary monitor
print(f"Using monitor {monitorIndex}: {monitor}")

# Data log file
data_file = open(os.path.join(SAVE_DIR, "data.txt"), "a")

frame_id = 0
interval = 1.0 / FPS
print("Starting data collection... press CTRL+C to stop.")

try:
    while True:
        start_time = time.time()

        # ---- 1. Capture steering angle ----
        pygame.event.pump()
        axis_val = joystick.get_axis(0)  # steering axis [-1, 1]
        degrees = axis_val * MAX_ROTATION  # scale to degrees

        # ---- 2. Capture screen ----
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)  # BGRA
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Save image
        filename = f"{frame_id}.jpg"
        filepath = os.path.join(SAVE_DIR, filename)
        cv2.imwrite(filepath, img)

        # ---- 3. Log to data.txt ----
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]
        data_file.write(f"{filename} {degrees:.6f},{timestamp}\n")
        data_file.flush()

        print(f"[{frame_id}] Steering={degrees:.2f}°  Saved={filename}")

        frame_id += 1

        # ---- 4. Keep steady FPS ----
        elapsed = time.time() - start_time
        sleep_time = max(0, interval - elapsed)
        time.sleep(sleep_time)

except KeyboardInterrupt:
    print("Stopping data collection...")

finally:
    data_file.close()
    pygame.quit()
