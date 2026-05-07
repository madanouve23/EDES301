import Adafruit_BBIO.PWM as PWM
import time

class BrailleAudioFeedback:
    """
    Controls an LM386 Amplifier module via PWM to provide 
    audio feedback for a Braille system.
    """
    def __init__(self, pin="P1_36"):
        self.pin = pin
        self.is_playing = False
        # Initialize PWM at 0% duty cycle (silent)
        PWM.start(self.pin, 0, 1000) 
        print(f"Audio Module initialized on {self.pin}.")

    def play_tone(self, frequency, volume=50):
        """
        Plays a continuous tone.
        :param frequency: Pitch in Hz (e.g., 440 for A4)
        :param volume: Duty cycle 0-100 (keep low to avoid clipping)
        """
        PWM.set_frequency(self.pin, frequency)
        PWM.set_duty_cycle(self.pin, volume)
        self.is_playing = True

    def stop_tone(self):
        """Silences the amplifier."""
        PWM.set_duty_cycle(self.pin, 0)
        self.is_playing = False

    def beep(self, duration=0.1, frequency=1000):
        """Plays a short 'blip' for tactile confirmation."""
        self.play_tone(frequency)
        time.sleep(duration)
        self.stop_tone()

    def play_alert(self, pattern="error"):
        """Pre-defined audio patterns for user feedback."""
        if pattern == "success":
            for freq in [880, 1109, 1318]: # A major chord
                self.beep(0.1, freq)
        elif pattern == "error":
            for _ in range(3):
                self.beep(0.05, 200)
                time.sleep(0.05)

    def cleanup(self):
        """Stops PWM and cleans up the pin."""
        PWM.stop(self.pin)
        PWM.cleanup()
        print("Audio GPIO cleaned up.")

# --- Terminal Execution ---
if __name__ == "__main__":
    audio = BrailleAudioFeedback()

    try:
        while True:
            cmd = input("Command (beep/success/error/quit): ").lower()
            if cmd == "beep":
                audio.beep(0.2, 800)
            elif cmd == "success":
                audio.play_alert("success")
            elif cmd == "error":
                audio.play_alert("error")
            elif cmd == "quit":
                break
    except KeyboardInterrupt:
        pass
    finally:
        audio.cleanup()
