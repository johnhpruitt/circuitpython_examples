# main execution for pimoroni keybow2040
# Modified from: https://github.com/NevynUK/Keybow2040
# Brought up to use PMK instead of deprecated pimoroni lib
# and customized layout.

"""
 This example is really interesting. 
 Intead of cramming a lot of code into the while loop around keybow.update(),
 most of the functionality is jammed into a big shared on_release() function.

 This looks like it's more stable than the delivered PMK macropad example, 
 when I start changing LED colors during that while loop behavior gets odd.

 I want to change an LED color on realeasing the caps lock key so I 
 might have to place a call to a second dict of keys and a second
 function to run in an on_release() event
"""

# Drop the `pmk` folder
# into your `lib` folder on your `CIRCUITPY` drive.
# NOTE! Requires the adafruit_hid CircuitPython library also!
# NOTE! Requires the adafruit_is31fl3731 CircuitPython library also! 

from pmk import PMK
from pmk.platform.keybow2040 import Keybow2040 as Hardware          # for Keybow 2040
# from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware  # for Pico RGB Keypad Base

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import time


from Keypads import NumericKeypad
from Keypads import MediaKeypad
from Keypads import ZoomKeypad

SelectingKeypadState = 1
WaitingForSelectionState = 2
KeypadActivatedState = 3

# Set up the keyboard and layout
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# Set up consumer control (used to send media key presses)
consumer_control = ConsumerControl(usb_hid.devices)

keybow = PMK(Hardware())
keys = keybow.keys

color_light_blue = (16, 255, 192)
color_orange = (255, 32, 0)
color_purple = (255, 0, 255)
color_yellow = (255, 255, 0)
color_light_red = (255, 2, 8)
white = (255, 255, 255)

modifier_key_number = 0

keypads = {
            0: NumericKeypad.NumericKeypad((16, 255, 192), 'Numbers', keyboard, layout, consumer_control, keybow),
            1: MediaKeypad.MediaKeypad((255, 255, 0), 'Media', keyboard, layout, consumer_control, keybow),
            2: ZoomKeypad.ZoomKeypad((255, 0, 0), 'Zoom', keyboard, layout, consumer_control, keybow)
          }

current_keypad = keypads[0]

current_state = KeypadActivatedState

def set_keypad_leds():
    keybow.set_all(0, 0, 0)
    for k in current_keypad.keys:
        if current_keypad._colours[k] is not None:
            keys[k].set_led(*current_keypad._colours[k])

@keybow.on_hold(keys[modifier_key_number])
def hold_handler(key):
    global current_state
    if key.number == modifier_key_number:
        keybow.set_all(0, 0, 0)

        for kp in range(0, 16):
            if (kp in keypads):
                keys[kp].set_led(*keypads[kp].colour)
        current_state = SelectingKeypadState

for key in keys:
    @keybow.on_release(key)
    def release_handler(key):
        global current_keypad
        global current_state
        if current_state == SelectingKeypadState:
            # wait in temporary state to reset the keypad
            current_state = WaitingForSelectionState
        else:
            if current_state == WaitingForSelectionState:
              # this bit does the actual selection of a layer
                if key.number in keypads:
                    current_keypad = keypads[key.number]
                    set_keypad_leds()
                    current_state = KeypadActivatedState
                    # this is where I would put any special keypad specific function on load
            else:
              # keypad is actually active
                # do the key press action.
                if current_keypad.keys[key.number] is not None:
                  # keypad is active and the key actually exists.
                    current_keypad.key_pressed(key.number)
                else:
                  # unknown key
                    print(f'Invalid key {key.number} released')
                # do the key release action.
                if current_keypad.releases[key.number] is not None:
                  # keypad is active and the key actually exists.
                    current_keypad.key_released(key.number)

set_keypad_leds()

while True:
  keybow.update()
  time.sleep(1.0 / 60)
