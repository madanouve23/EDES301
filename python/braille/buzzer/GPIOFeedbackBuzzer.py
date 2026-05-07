import Adafruit_BBIO.GPIO as GPIO
import time

class GPIOFeedbackBuzzer:
    """
    A class to control an active buzzer via GPIO on the PocketBeagle.
    """
    def __init__(self, pin="P2_03"):
        self.pin = pin
        self.is_sounding = False
        
        # Initialize GPIO
        GPIO.setup(self.pin, GPIO.OUT)
        # Ensure it starts OFF
        GPIO.output(self.pin, GPIO.LOW)
        print(f"Buzzer initialized on {self.pin}.")

    def on(self):
        """Turns the buzzer on indefinitely."""
        if not self.is_sounding:
            GPIO.output(self.pin, GPIO.HIGH)
            self.is_sounding = True

    def off(self):
        """Turns the buzzer off."""
        if self.is_sounding:
            GPIO.output(self.pin, GPIO.LOW)
            self.is_sounding = False

    def buzz(self, duration):
        """
        Sounds the buzzer for a specific duration.
        :param duration: Time in seconds
        """
        self.on()
        time.sleep(duration)
        self.off()

    def alert_pattern(self, count=3, speed=0.1):
        """Creates a series of rapid beeps."""
        for _ in range(count):
            self.on()
            time.sleep(speed)
            self.off()
            time.sleep(speed)

    def cleanup(self):
        """Safety cleanup to ensure the buzzer isn't left screaming."""
        self.off()
        GPIO.cleanup()
        print("Buzzer GPIO cleaned up.")

# --- Terminal Execution ---
if __name__ == "__main__":
    # Initialize on P2_03
    alarm = GPIOFeedbackBuzzer("P2_03")

    try:
        while True:
            cmd = input("Buzzer Cmd (on/off/buzz/pattern/quit): ").lower()
            if cmd == "on":
                alarm.on()
            elif cmd == "off":
                alarm.off()
            elif cmd == "buzz":
                sec = float(input("Duration (sec): "))
                alarm.buzz(sec)
            elif cmd == "pattern":
                alarm.alert_pattern()
            elif cmd == "quit":
                break
    except KeyboardInterrupt:
        pass
    finally:
        alarm.cleanup()
