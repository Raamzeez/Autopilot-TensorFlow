import threading
import time
from logidrivepy import LogitechController

class WheelController:
    def __init__(self, wheel_id=0, kp=50, kd=5):
        self.lc = LogitechController()
        if not self.lc.steering_initialize():
            raise RuntimeError("Failed to initialize Logitech wheel")

        self.wheel_id = wheel_id
        self.target_angle = 0.0
        self.kp = kp
        self.kd = kd

        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def set_angle(self, angle_deg: float):
        """Set desired steering angle in degrees (approx)."""
        self.target_angle = angle_deg

    def _loop(self):
        prev_error = 0.0
        prev_time = time.time()

        while self._running:
            self.lc.logi_update()
            state = self.lc.get_state(self.wheel_id)

            # Depending on wrapper, adjust this line:
            current_angle = state.lX  # common axis field (check your wrapper!)
            
            # Scale raw axis to degrees (-450..+450 typical for G920)
            # Some SDKs already give degrees; adjust if needed
            wheel_range = 900  
            current_deg = (current_angle / 32767.0) * (wheel_range / 2)

            # Error
            error = self.target_angle - current_deg
            now = time.time()
            dt = now - prev_time if now - prev_time > 0 else 1e-3
            d_error = (error - prev_error) / dt

            # PD control
            torque = self.kp * error + self.kd * d_error

            # Clamp torque (SDK expects -10000..10000 usually)
            torque = max(-10000, min(10000, int(torque)))

            self.lc.play_constant_force(self.wheel_id, torque)

            prev_error = error
            prev_time = now
            time.sleep(0.01)  # ~100 Hz

    def stop(self):
        self._running = False
        self._thread.join()
        self.lc.steering_shutdown()

