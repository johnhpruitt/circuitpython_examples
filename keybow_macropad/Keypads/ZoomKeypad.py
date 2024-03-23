# Modified from: https://github.com/NevynUK/Keybow2040
# Brought up to use PMK instead of deprecated pimoroni lib
# and customized layout.

from adafruit_hid.keycode import Keycode
from Keypads import KeypadBase

class ZoomKeypad(KeypadBase.KeypadBase):
    def __init__(self, colour, name, keyboard, layout, consumer_control, keybow):
        KeypadBase.KeypadBase.__init__(self, colour, name, keyboard, layout, consumer_control, keybow)
        self._keys = {
                        0: None, 1: None,  2: None, 3: None,
                        4: None, 5: None,  6: None, 7: None,
                        8: None, 9: None,  10: None, 11: None,
                        12: self.leave_meeting, 13: None,  14: self.start_stop_video, 15: self.mute_unmute
                    }

        self._colours = {
            3: None, 7: None, 11: None, 15: colour,
            2: None, 6: None, 10: None, 14: colour,
            1: None, 5: None, 9: None, 13: None,
            0: (255,255,255), 4: None, 8: None, 12: colour
            }
            
        self._releases = {
                        3: None, 7: None, 11: None, 15: None,
                        2: None, 6: None, 10: None, 14: None,
                        1: None, 5: None, 9: None, 13: None,
                        0: None, 4: None, 8: None, 12: None
            }

    def leave_meeting(self):
        print('Leaving meeting')
        self.send_keystrokes(Keycode.COMMAND, Keycode.W)
        
    def start_stop_video(self):
        print('Start / Stop Video')
        self.send_keystrokes(Keycode.COMMAND, Keycode.SHIFT, Keycode.V)
        
    def mute_unmute(self):
        print('Mute / Unmute')
        self.send_keystrokes(Keycode.COMMAND, Keycode.SHIFT, Keycode.A)
