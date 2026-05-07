import spidev
import RPi.GPIO as GPIO
import time

class ResistiveTouch:
    """
    A class for a 4-wire resistive touch screen using an MCP3008 ADC.
    Pins: X+, X-, Y+, Y-
    """
    def __init__(self, x_plus, x_minus, y_plus, y_minus, bus=0, device=0):
        self.pins = {'xp': x_plus, 'xm': x_minus, 'yp': y_plus, 'ym': y_minus}
        
        # SPI Setup for MCP3008
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1350000

        # GPIO Setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Calibration defaults (will vary by screen)
        self.x_min, self.x_max = 100, 900
        self.y_min, self.y_max = 100, 900

    def _read_adc(self, channel):
        """Reads raw data from the specified MCP3008 channel (0-7)."""
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def get_coords(self):
        """
        Calculates X and Y by toggling power between layers.
        Returns (x, y) tuple.
        """
        # --- Read X Position ---
        # Set X-layer as a voltage divider, Y+ as the probe
        GPIO.setup(self.pins['xp'], GPIO.OUT)
        GPIO.setup(self.pins['xm'], GPIO.OUT)
        GPIO.output(self.pins['xp'], GPIO.HIGH)
        GPIO.output(self.pins['xm'], GPIO.LOW)
        
        # Y+ must be high-impedance (Input) for the ADC to read it
        GPIO.setup(self.pins['yp'], GPIO.IN)
        time.sleep(0.01) # Settle time
        raw_x = self._read_adc(0) # Assuming Y+ is on ADC Channel 0

        # --- Read Y Position ---
        # Set Y-layer as a voltage divider, X+ as the probe
        GPIO.setup(self.pins['yp'], GPIO.OUT)
        GPIO.setup(self.pins['ym'], GPIO.OUT)
        GPIO.output(self.pins['yp'], GPIO.HIGH)
        GPIO.output(self.pins['ym'], GPIO.LOW)
        
        GPIO.setup(self.pins['xp'], GPIO.IN)
        time.sleep(0.01) 
        raw_y = self._read_adc(1) # Assuming X+ is on ADC Channel 1

        return raw_x, raw_y

    def is_pressed(self, threshold=100):
        """Checks if the screen is being touched based on ADC values."""
        x, y = self.get_coords()
        return x > threshold and y > threshold

    def cleanup(self):
        """Closes SPI and resets GPIO."""
        self.spi.close()
        GPIO.cleanup()
        print("Touchscreen interface de-initialized.")

# --- Terminal Execution Example ---
if __name__ == "__main__":
    # Example BCM Pin Mapping
    TS = ResistiveTouch(x_plus=17, x_minus=27, y_plus=22, y_minus=23)

    try:
        print("Waiting for touch... (Ctrl+C to stop)")
        while True:
            if TS.is_pressed():
                x, y = TS.get_coords()
                print(f"Touch Detected! Raw X: {x} | Raw Y: {y}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        TS.cleanup()
