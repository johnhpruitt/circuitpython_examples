"""
waveshare rp2040 zero
>>> dir(board)
['__class__', '__name__', 'A0', 'A1', 'A2', 'A3', 'GP0', 'GP1', 'GP10', 'GP11', 'GP12', 'GP13', 'GP14', 'GP15', 'GP16', 'GP17', 'GP18', 'GP19', 'GP2', 'GP20', 'GP21', 'GP22', 'GP23', 'GP24', 'GP25', 'GP26', 'GP26_A0', 'GP27', 'GP27_A1', 'GP28', 'GP28_A2', 'GP29', 'GP29_A3', 'GP3', 'GP4', 'GP5', 'GP6', 'GP7', 'GP8', 'GP9', 'NEOPIXEL', 'RX', 'TX', 'UART', 'board_id']
"""

# built in
import keypad
import board
import usb_hid
import microcontroller

# official adafruit libraries
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

km = keypad.KeyMatrix(
    row_pins=(board.GP6, board.GP7, board.GP8),
    column_pins=(board.GP14, board.GP15, board.GP26),
    interval=0.050,
)

kbd = Keyboard(usb_hid.devices)
last_2_events = {1: None, 2: None}

while True:
    # This is an incredibly basic example 
    # real implementations woukd use KMK
    # https://learn.adafruit.com/navi10-macropad-with-kb2040-and-kmk-circuitpython-keyboard-firmware/installing-kmk
    # but this simple example in a while loop will be useful for
    # controlling simple circuitpython scripts that are in a loop.
    event = km.events.get()
    if event:
        if ( last_2_events[1] != None 
        and last_2_events[2] != None ) :
            print(str(event.key_number)+':'+str(event.pressed)+'|'+ str(last_2_events[1].key_number) + str(last_2_events[2].key_number))
        else:
            print(event)

        # 0
        if event.pressed and event.key_number == 0:
            kbd.send(Keycode.ESCAPE)
            while km.events.get() == event: # Wait for button to be released
                pass

        # 1
        if event.pressed and event.key_number == 1:
            kbd.send(Keycode.UP_ARROW)
            while km.events.get() == event: # Wait for button to be released
                pass

        # 2
        if event.pressed and event.key_number == 2:
            kbd.send(Keycode.ENTER)
            while km.events.get() == event: # Wait for button to be released
                pass

        # 3
        if event.pressed and event.key_number == 3:
            kbd.send(Keycode.LEFT_ARROW)
            while km.events.get() == event: # Wait for button to be released
                pass
        # 4
        if event.pressed and event.key_number == 4:
            kbd.send(Keycode.DOWN_ARROW)
            while km.events.get() == event: # Wait for button to be released
                pass

        # 5
        if event.pressed and event.key_number == 5:
            kbd.send(Keycode.RIGHT_ARROW)
            while km.events.get() == event: # Wait for button to be released
                pass

        # 6
        if event.pressed and event.key_number == 6:
            kbd.send(Keycode.CONTROL)
            while km.events.get() == event: # Wait for button to be released
                pass

        # 7
        if event.pressed and event.key_number == 7:
            kbd.send(Keycode.ALT)
            while km.events.get() == event: # Wait for button to be released
                pass
        # 8
        if event.pressed and event.key_number == 8:
            kbd.send(Keycode.DELETE)
            while km.events.get() == event: # Wait for button to be released
                pass

        # reset condition
        if ((event.pressed and event.key_number == 8)
            and (last_2_events[1] != None and last_2_events[2] != None )
            and (last_2_events[1].key_number == 7 and last_2_events[1].pressed) 
            and (last_2_events[2].key_number == 6 and last_2_events[2].pressed)):
            print("FREAK OUT!!!")
            microcontroller.on_next_reset(microcontroller.RunMode.NORMAL)
            microcontroller.reset()

        # store last 2 presses        
        if event.pressed:
            last_event = last_2_events [1]
            last_2_events[2] = last_event
            last_2_events[1] = event