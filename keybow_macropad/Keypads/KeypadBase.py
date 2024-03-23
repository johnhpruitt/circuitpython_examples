# Modified from: https://github.com/NevynUK/Keybow2040
# Brought up to use PMK instead of deprecated pimoroni lib
# and customized layout.

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

class KeypadBase():
    def __init__(self, colour, name, keyboard, layout, consumer_control, keybow):
        self._colour = colour
        self._keyboard = keyboard
        self._layout = layout
        self._name = name
        self._consumer_control = consumer_control
        self._keys = {
                3: None, 7: None, 11: None, 15: None,
                2: None, 6: None, 10: None, 14: None,
                1: None, 5: None, 9: None, 13: None,
                0: None, 4: None, 8: None, 12: None
            }
        self._releases = {
                3: None, 7: None, 11: None, 15: None,
                2: None, 6: None, 10: None, 14: None,
                1: None, 5: None, 9: None, 13: None,
                0: None, 4: None, 8: None, 12: None
            }
        self._keybow = keybow

    @property
    def name(self):
        return(self._name)

    @property
    def colour(self):
        return(self._colour)

    @property
    def keys(self):
        return(self._keys)

    @property
    def releases(self):
        return(self._releases)

    def send_keystrokes(self, *keycodes: int):
        self._keyboard.send(*keycodes)

    def execute_command(self, command):
        self._layout.write(f'{command}\n')

    def key_pressed(self, number):
        if number in self.keys:
            self.keys[number]()
        else:
            print(f'Unknown key {number}')

    # Secondary realese function
    # This will make sense in code.py, 
    # where relase is used for almost everything,
    # including presses. 
    # This would be a second realese action when it is not None.
    def key_released(self, number):
        if number in self.keys:
            self.releases[number]()
        else:
            print(f'Unknown key released {number}')
