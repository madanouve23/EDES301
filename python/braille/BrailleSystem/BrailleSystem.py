import time
import os
import Adafruit_BBIO.GPIO as GPIO
# Assuming the previous classes are in the same directory or imported
# from solenoid import SolenoidValve
# from touchscreen import PocketBeagleTouch
# from audio import BrailleAudioFeedback

class BrailleSystem:
    def __init__(self):
        # Initialize Hardware
        self.touch = PocketBeagleTouch() # Pins P1.19, 1.21, 1.23, 1.25
        self.sol_left = SolenoidValve("P2_01")
        self.sol_right = SolenoidValve("P2_02")
        self.audio = BrailleAudioFeedback("P1_36")
        
        self.sequence = []
        self.last_char = None
        self.debounce_time = 0.5 # Seconds to wait before registering same char
        self.last_touch_time = 0

        # Grid Calibration (PocketBeagle ADC is 0-4095)
        self.mid_x = 2048
        self.mid_y = 2048

    def process_touch(self, x, y):
        """Maps (x, y) to a character and triggers haptics/audio."""
        current_char = ""
        
        if x < self.mid_x and y > self.mid_y:
            current_char = "w"
            self.sol_left.pulse(0.1)
            self.play_audio("w_sound.wav")
        elif x >= self.mid_x and y > self.mid_y:
            current_char = "a"
            self.sol_right.pulse(0.1)
            self.play_audio("a_sound.wav")
        elif x < self.mid_x and y <= self.mid_y:
            current_char = "s"
            # Actuate both for 'S'
            self.sol_left.open_valve()
            self.sol_right.open_valve()
            time.sleep(0.1)
            self.sol_left.close_valve()
            self.sol_right.close_valve()
            self.play_audio("s_sound.wav")
        elif x >= self.mid_x and y <= self.mid_y:
            current_char = "d"
            self.audio.beep(0.1, 440) # Simple beep for D
            self.play_audio("d_sound.wav")

        # Append to sequence if it's a new interaction
        now = time.time()
        if current_char != self.last_char or (now - self.last_touch_time > self.debounce_time):
            self.sequence.append(current_char)
            self.last_char = current_char
            self.last_touch_time = now
            print(f"Current Sequence: {''.join(self.sequence)}")

    def play_audio(self, filename):
        """
        Placeholder for playing a specific audio file. 
        On Linux, you'd typically use 'aplay' or a library like pygame.
        """
        # os.system(f"aplay /home/debian/sounds/{filename} &")
        print(f"Playing audio: {filename}")

    def run(self):
        print("Braille System Active. Touch the screen grid...")
        try:
            while True:
                if self.touch.is_pressed():
                    x, y = self.touch.get_coords()
                    self.process_touch(x, y)
                    # Small sleep to prevent high CPU usage and double-triggering
                    time.sleep(0.3) 
                time.sleep(0.05)
        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        self.sol_left.cleanup()
        self.sol_right.cleanup()
        self.audio.cleanup()
        self.touch.cleanup()
        print("\nFinal Sequence Recorded:", "".join(self.sequence))

if __name__ == "__main__":
    system = BrailleSystem()
    system.run()
