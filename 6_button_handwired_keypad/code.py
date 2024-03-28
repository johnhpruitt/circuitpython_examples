# Based on
# https://learn.adafruit.com/key-pad-matrix-scanning-in-circuitpython/keys-one-key-per-pin
# https://learn.adafruit.com/key-pad-matrix-scanning-in-circuitpython/keymatrix
# Dan Halbert for Adafruit Industries
#
# Test for waveshare rp2040-zero handwired navigation pad
import keypad
import board
import keypad
import neopixel
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

KEYCODES = (	
    Keycode.ZERO,		#0
    Keycode.UP_ARROW,		#1
    Keycode.ZERO,		#2
    Keycode.A,			#3
    Keycode.LEFT_ARROW,		#4
    Keycode.DOWN_ARROW,		#5
    Keycode.RIGHT_ARROW,	#6
    Keycode.B,			#7
)

km = keypad.KeyMatrix(
    row_pins=(board.GP28, board.GP29),
    column_pins=(board.GP27, board.GP26, board.GP15, board.GP14),
    columns_to_anodes=True,
)

kbd = Keyboard(usb_hid.devices)

while True:
    event = km.events.get()
    if event:
        print(event)
        key_number = event.key_number
        # A key transition occurred.
        if event.pressed:
            kbd.press(KEYCODES[key_number])
        if event.released:
            kbd.release(KEYCODES[key_number])
