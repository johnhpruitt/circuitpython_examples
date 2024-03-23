# Modified from: https://github.com/NevynUK/Keybow2040
# Brought up to use PMK instead of deprecated pimoroni lib
# and customized layout.

from adafruit_hid.keycode import Keycode
from Keypads import KeypadBase

#added for volume buttons 
from adafruit_hid.consumer_control_code import ConsumerControlCode

class MediaKeypad(KeypadBase.KeypadBase):
    def __init__(self, colour, name, keyboard, layout, consumer_control, keybow):
        KeypadBase.KeypadBase.__init__(self, colour, name, keyboard, layout, consumer_control, keybow)
        self._keys = {
                        3: None, 7: self.key7_pressed, 11: self.key11_pressed, 15: self.key15_pressed,
                        2: None, 6: self.key6_pressed, 10: self.key10_pressed, 14: self.key14_pressed,
                        1: None, 5: None, 9: None, 13: None,
                        0: None, 4: None, 8: None, 12: None
            }

        self._colours = {
            3: None, 7: colour, 11: colour, 15: colour,
            2: None, 6: colour, 10: (255, 32, 0), 14: colour,
            1: None, 5: None, 9: None, 13: None,
            0: (255,255,255), 4: None, 8: None, 12: None
            }
            
        self._releases = {
                        3: None, 7: None, 11: None, 15: None,
                        2: None, 6: None, 10: self.key10_released, 14: None,
                        1: None, 5: None, 9: None, 13: None,
                        0: None, 4: None, 8: None, 12: None
            }
    def key6_pressed(self):
        print('Press M[6]')
        self._consumer_control.send(ConsumerControlCode.VOLUME_DECREMENT)
        
    def key7_pressed(self):
        print('Press M[7]')
        self._consumer_control.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)

    def key10_pressed(self):
        print('Press M[10]')
        self._consumer_control.send(ConsumerControlCode.MUTE)

    def key11_pressed(self):
        print('Press M[11]')
        self._consumer_control.send(ConsumerControlCode.PLAY_PAUSE)

    def key14_pressed(self):
        print('Press M[14]')
        self._consumer_control.send(ConsumerControlCode.VOLUME_INCREMENT)
        
    def key15_pressed(self):
        print('Press M[15]')
        self._consumer_control.send(ConsumerControlCode.SCAN_NEXT_TRACK)

    def key10_released(self):
        print('Special Release M[10]')
        """"
        if self._keyboard.led_on(Keyboard.LED_NUM_LOCK):
            self._colours[10] = (255, 255, 0)
            self._keybow.keys[2].set_led(255, 255, 255)
        else:
            self._colours[10] = (255, 255, 255)
            self._keybow.keys[2].set_led(255, 255, 0)
        """

