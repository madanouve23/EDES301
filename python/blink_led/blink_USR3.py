# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Blinking USR3 LED
--------------------------------------------------------------------------
License:   
Copyright 2026 - Adam Vuong

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Program that uses the Adafruit BBIO library to blink the USR3 LED at 5 Hz (i.e. 5 full on/off cycles
per second).

Operations: None

Error conditions: None

--------------------------------------------------------------------------
"""

# NOTE - Add import statements to allow access to Python library functions
# NOTE - Hint:  Look at  https://docs.python.org/3/library/operator.html
import operator
import Adafruit_BBIO.GPIO as GPIO
import time

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# NOTE - No constants are needed for this example 

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# NOTE - Define the target LED to let blink
LED = "USR3"

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

# NOTE - The python variable "__name__" is provided by the language and can 
# NOTE - be used to determine how the file is being executed.  For example,
# NOTE - if the program is being executed on the command line:
# NOTE -   python3 simple_calc.py
# NOTE - then the "__name__" will be the string:  "__main__".  If the file 
# NOTE - is being imported into another Python file:
# NOTE -   import simple_calc
# NOTE - the "__name__" will be the module name, i.e., the string "simple_calc"

if __name__ == "__main__":

    # NOTE - Total Period = 1 second/5 cycles = 0.2 seconds per cycle
    # NOTE - Assuming equal time on and off, we can calculate delays as such:
    # NOTE - On time = 0.2 seconds/2 = 0.1 seconds
    # NOTE - Off time = 0.2 seconds/2 = 0.1 seconds

    while True:
        # Setup the pin as an output
        GPIO.setup(LED, GPIO.OUT)
    
        print("Blinking USR3 LED on PocketBeagle at 5Hz. Press Ctrl+C to stop.")
        
        try:
            while True:
                # Turn LED ON
                GPIO.output(LED, GPIO.HIGH)
                time.sleep(0.1)
                
                # Turn LED OFF
                GPIO.output(LED, GPIO.LOW)
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            # Clean up GPIO settings on exit
            GPIO.cleanup()
            print("Exiting.")
            break
        break
    
