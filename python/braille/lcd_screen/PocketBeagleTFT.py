import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import ili9341 # Change based on your driver (e.g., st7735)

class PocketBeagleTFT:
    """
    A class to manage a TFT LCD screen using SPI on a PocketBeagle.
    Default configuration is for an ILI9341 240x320 display.
    """
    def __init__(self, rotation=90):
        # Configuration for Pins
        cs_pin = digitalio.DigitalInOut(board.P1_06)
        dc_pin = digitalio.DigitalInOut(board.P1_02)
        reset_pin = digitalio.DigitalInOut(board.P1_04)

        # Config for SPI
        spi = board.SPI()

        # Initialize Display
        self.display = ili9341.ILI9341(
            spi,
            rotation=rotation,
            cs=cs_pin,
            dc=dc_pin,
            rst=reset_pin,
            baudrate=24000000, # 24MHz for smooth updates
        )

        # Create blank image for drawing
        if rotation % 180 == 90:
            self.width = self.display.height
            self.height = self.display.width
        else:
            self.width = self.display.width
            self.height = self.display.height

        self.image = Image.new("RGB", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        
        self.clear_screen()
        print("TFT LCD Initialized.")

    def clear_screen(self, color=(0, 0, 0)):
        """Wipes the screen with a solid color."""
        self.draw.rectangle((0, 0, self.width, self.height), fill=color)
        self.display.image(self.image)

    def draw_text(self, text, x, y, size=20, color=(255, 255, 255)):
        """Draws text to the internal buffer and updates screen."""
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except IOError:
            font = ImageFont.load_default()
            
        self.draw.text((x, y), text, font=font, fill=color)
        self.display.image(self.image)

    def draw_braille_cell(self, x, y, dots=[0,0,0,0,0,0]):
        """
        Specialized helper for your Braille project.
        'dots' is a list of 6 booleans representing the Braille cell.
        """
        radius = 10
        padding = 15
        for i, active in enumerate(dots):
            # Calculate 2x3 grid positions
            col = i // 3
            row = i % 3
            dot_x = x + (col * (radius * 2 + padding))
            dot_y = y + (row * (radius * 2 + padding))
            
            fill = (255, 255, 0) if active else (50, 50, 50)
            self.draw.ellipse([dot_x, dot_y, dot_x+radius*2, dot_y+radius*2], fill=fill)
        
        self.display.image(self.image)

    def cleanup(self):
        """Clears screen and shuts down."""
        self.clear_screen()
        print("Display buffer cleared.")

# --- Terminal Execution ---
if __name__ == "__main__":
    tft = PocketBeagleTFT()

    try:
        tft.draw_text("Braille System", 10, 10, size=24)
        # Draw a 'Letter B' in Braille (Dots 1 and 2)
        tft.draw_braille_cell(100, 80, dots=[1, 1, 0, 0, 0, 0])
        
        print("Displaying demo... Press Ctrl+C to exit.")
        while True:
            pass
    except KeyboardInterrupt:
        tft.cleanup()
