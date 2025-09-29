import pygame
import time

# Initialize steering wheel (Logitech G920)
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Detected controller: {joystick.get_name()}")

MAX_ROTATION = 450  # Logitech G920 is ±450 degrees

print("Steering angle reader started... press CTRL+C to stop.")

try:
    while True:
        # Get steering angle
        pygame.event.pump()
        axis_val = joystick.get_axis(0)  # steering axis [-1, 1]
        degrees = axis_val * MAX_ROTATION  # scale to degrees
        
        print(f"Steering angle: {degrees:.2f}°")
        time.sleep(0.1)  # Update 10 times per second

except KeyboardInterrupt:
    print("Stopping steering reader...")

finally:
    pygame.quit()
