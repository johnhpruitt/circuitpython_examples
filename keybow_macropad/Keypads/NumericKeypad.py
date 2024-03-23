# Modified from: https://github.com/NevynUK/Keybow2040
# Brought up to use PMK instead of deprecated pimoroni lib
# and customized layout.

import time
from adafruit_hid.keycode import Keycode
from Keypads import KeypadBase

### added for num lock light
from adafruit_hid.keyboard import Keyboard 
### 

class NumericKeypad(KeypadBase.KeypadBase):
    def __init__(self, colour, name, keyboard, layout, consumer_control, keybow):
        KeypadBase.KeypadBase.__init__(self, colour, name, keyboard, layout, consumer_control, keybow)
        self._keys = {
                        3: self.key3_pressed, 7: self.key7_pressed, 11: self.key11_pressed, 15: self.key15_pressed,
                        2: self.key2_pressed, 6: self.key6_pressed, 10: self.key10_pressed, 14: self.key14_pressed,
                        1: self.key1_pressed, 5: self.key5_pressed, 9: self.key9_pressed, 13: self.key13_pressed,
                        0: None, 4: self.key4_pressed, 8: self.key8_pressed, 12: self.key12_pressed
            }

        self._colours = {
                    3: (255,0,0), 7: colour, 11: colour, 15: colour,
                    2: colour, 6: colour, 10: colour, 14: colour,
                    1: (0,255,0), 5: colour, 9: colour, 13: colour,
                    0: (255,255,255), 4: (0,0,255), 8: colour, 12: (0,0,255)
            }

        self._releases = {
                        3: None, 7: None, 11: None, 15: None,
                        2: self.key2_released, 6: None, 10: None, 14: None,
                        1: None, 5: None, 9: None, 13: None,
                        0: None, 4: None, 8: None, 12: None
            }
        
    def key1_pressed(self):
        print('Press K[1]')
        self.send_keystrokes(Keycode.TAB)
        
    def key2_pressed(self):
        print('Press K[2]')
        self.send_keystrokes(Keycode.KEYPAD_NUMLOCK)
        
    def key3_pressed(self):
        print('Press K[3]')
        self.send_keystrokes(Keycode.CONTROL, Keycode.S)

    def key4_pressed(self):
        print('Press K[4]')
        self.send_keystrokes(Keycode.BACKSPACE)

    def key5_pressed(self):
        print('Press K[5]')
        self.send_keystrokes(Keycode.KEYPAD_ONE)

    def key6_pressed(self):
        print('Press K[6]')
        self.send_keystrokes(Keycode.KEYPAD_FOUR)
        
    def key7_pressed(self):
        print('Press K[7]')
        self.send_keystrokes(Keycode.KEYPAD_SEVEN)

    def key8_pressed(self):
        print('Press K[8]')
        self.send_keystrokes(Keycode.KEYPAD_ZERO)

    def key9_pressed(self):
        print('Press K[9]')
        self.send_keystrokes(Keycode.KEYPAD_TWO)

    def key10_pressed(self):
        print('Press K[10]')
        self.send_keystrokes(Keycode.KEYPAD_FIVE)

    def key11_pressed(self):
        print('Press K[11]')
        self.send_keystrokes(Keycode.KEYPAD_EIGHT)
        
    def key12_pressed(self):
        print('Press K[12]')
        self.send_keystrokes(Keycode.KEYPAD_ENTER)

    def key13_pressed(self):
        print('Press K[13]')
        self.send_keystrokes(Keycode.KEYPAD_THREE)
        
    def key14_pressed(self):
        print('Press K[14]')
        self.send_keystrokes(Keycode.KEYPAD_SIX)
        
    def key15_pressed(self):
        print('Press K[15]')
        self.send_keystrokes(Keycode.KEYPAD_NINE)

    def key2_released(self):
        print('Special Release K[2]')
        if self._keyboard.led_on(Keyboard.LED_NUM_LOCK):
            self._colours[2] = (255, 255, 0)
            self._keybow.keys[2].set_led(255, 255, 255)
        else:
            self._colours[2] = (255, 255, 255)
            self._keybow.keys[2].set_led(255, 255, 0)