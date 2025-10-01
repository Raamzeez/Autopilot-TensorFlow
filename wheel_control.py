# Test Tkinter
print("Testing Tkinter...")
try:
    import tkinter as tk
    root = tk.Tk()
    print("Tkinter initialized successfully!")
    print(f"Tkinter version: {tk.TkVersion}")
    root.withdraw()  # Hide the window
    root.update()    # Process events
    print("Tkinter window created and hidden")
    root.destroy()   # Clean up
    print("Tkinter cleanup successful")
except Exception as e:
    print(f"Tkinter error: {e}")

# Now try the wheel connection
print("\nTesting wheel connection...")
from logidrivepy import LogitechController
import os
from logidrivepy.constants import LogitechControllerConstants as LCC
import time

# Try to find G HUB's DLL
possible_dll_paths = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv', 'Lib', 'site-packages', 'logidrivepy', 'dll', 'LogitechSteeringWheelEnginesWrapper.dll'),
    r"C:\Program Files\LGHUB\sdk\LogitechSteeringWheelEnginesWrapper.dll",
    r"C:\Program Files\Logitech Gaming Software\sdk\LogitechSteeringWheelEnginesWrapper.dll",
]

for dll_path in possible_dll_paths:
    if os.path.exists(dll_path):
        print(f"Found DLL at: {dll_path}")
        try:
            controller = LogitechController(dll_path)
            print(f"steering_initialize: {controller.steering_initialize()}")
            print(f"logi_update: {controller.logi_update()}")
            print(f"is_connected: {controller.is_connected(0)}")
            controller.steering_shutdown()
            if controller.is_connected(0):
                print("Success! Wheel connected.")
                break
        except Exception as e:
            print(f"Failed with DLL {dll_path}: {e}")
    else:
        print(f"DLL not found at: {dll_path}")

# Initialize controller
controller = LogitechController()
print("Initializing wheel...")
if not controller.steering_initialize():
    print("Failed to initialize wheel!")
    exit()

print("Wheel initialized successfully!")

try:
    while True:
        # Must call update every frame
        controller.logi_update()
        
        # Get wheel state
        state = controller.get_state_engines(0)
        
        if state:
            # Steering axis (typically ranges from -32768 to 32767)
            steering = state.lX
            # Convert to degrees (assuming 900 degree rotation)
            steering_degrees = (steering / 32767.0) * 450  # 450 = half of 900 degrees
            
            # Pedals (typically 0 to 32767)
            throttle = state.lY
            brake = state.lRz
            clutch = state.rglSlider[0] if hasattr(state, 'rglSlider') else 0
            
            # Buttons (returns array of button states)
            buttons = state.rgbButtons if hasattr(state, 'rgbButtons') else []
            
            print(f"\rWheel: {steering_degrees:6.1f}° | Throttle: {throttle/327.67:3.0f}% | Brake: {brake/327.67:3.0f}% | Clutch: {clutch/327.67:3.0f}%", end='')
            
            # Print any pressed buttons
            pressed = [i for i, button in enumerate(buttons) if button]
            if pressed:
                print(f" | Buttons: {pressed}", end='')
        
        time.sleep(0.01)  # 100Hz update rate

except KeyboardInterrupt:
    print("\nStopping...")
finally:
    controller.steering_shutdown()
