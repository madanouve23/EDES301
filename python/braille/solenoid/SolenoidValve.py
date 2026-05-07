import RPi.GPIO as GPIO
import time

class SolenoidValve:
    """
    A class to control a miniature solenoid valve via GPIO.
    """
    def __init__(self, pin, board_mode=GPIO.BCM):
        self.pin = pin
        self.board_mode = board_mode
        self.is_open = False

        # Setup GPIO
        GPIO.setmode(self.board_mode)
        GPIO.setup(self.pin, GPIO.OUT)
        
        # Ensure the valve starts in the CLOSED (Low) state
        GPIO.output(self.pin, GPIO.LOW)
        print(f"Valve initialized on Pin {self.pin}.")

    def open_valve(self):
        """Actuates the solenoid to open the valve."""
        if not self.is_open:
            GPIO.output(self.pin, GPIO.HIGH)
            self.is_open = True
            print("Valve: OPEN")
        else:
            print("Valve is already open.")

    def close_valve(self):
        """De-energizes the solenoid to close the valve."""
        if self.is_open:
            GPIO.output(self.pin, GPIO.LOW)
            self.is_open = False
            print("Valve: CLOSED")
        else:
            print("Valve is already closed.")

    def pulse(self, duration):
        """Opens the valve for a specific number of seconds, then closes it."""
        self.open_valve()
        time.sleep(duration)
        self.close_valve()

    def cleanup(self):
        """Resets the GPIO pin state safely."""
        self.close_valve()
        GPIO.cleanup(self.pin)
        print("GPIO cleaned up and valve shut down.")

# --- Terminal Execution Example ---
if __name__ == "__main__":
    # Use GPIO Pin 18 (BCM numbering)
    VALVE_PIN = 18
    valve = SolenoidValve(VALVE_PIN)

    try:
        while True:
            cmd = input("Enter command (open/close/pulse/quit): ").lower()
            if cmd == "open":
                valve.open_valve()
            elif cmd == "close":
                valve.close_valve()
            elif cmd == "pulse":
                sec = float(input("Duration in seconds: "))
                valve.pulse(sec)
            elif cmd == "quit":
                break
            else:
                print("Unknown command.")
    except KeyboardInterrupt:
        print("\nManual override detected.")
    finally:
        valve.cleanup()
