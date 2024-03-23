import board
import time
from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Button
import neopixel
import supervisor
import random
import traceback

#------------------------------------------------------------------------------#
# Waste of flashRAM to import all these, but here are the class names.         #
# https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation/tree/main   #
#------------------------------------------------------------------------------#

from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.customcolorchase import CustomColorChase
from adafruit_led_animation.animation.grid_rain import Rain
from adafruit_led_animation.animation.multicolor_comet import MulticolorComet
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.sparklepulse import SparklePulse

from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.sequence import AnimationSequence
import adafruit_led_animation.color as color
### RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, BLUE, PURPLE, MAGENTA, WHITE, BLACK, GOLD, PINK, AQUA, JADE, AMBER, OLD_LACE

DEBUG = False
default_brightness = .1
brightness = default_brightness

button_pin = DigitalInOut(board.D2)
button_pin.direction = Direction.INPUT
button_pin.pull = Pull.UP
switch = Button(button_pin) 


# https://blog.adafruit.com/2023/01/06/john-parks-circuitpython-parsec-short-vs-long-press-adafruit-johnedgarpark-adafruit-circuitpython/
# This tutorial asks for Pull.DOWN and the following params. That combination breaks Button.update().
# should probably research pull directions or try adding the params in one at a time.
# switch = Button(button_pin, long_duration_ms=500, value_when_pressed = True)

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=.01)
pixel.brightness = default_brightness

jewel_pin = board.A3
jewel_pixels = 7
jewel_ORDER = neopixel.GRBW
jewel = neopixel.NeoPixel(jewel_pin, jewel_pixels, brightness=.01, auto_write=True, pixel_order=jewel_ORDER)
jewel.brightness = brightness

def strobe4():  
        jewel.fill((255, 0, 0, 0))
        pixel.fill((255, 0, 0))
        time.sleep(0.5)
        jewel.fill((0, 255, 0, 0))
        pixel.fill((0, 255, 0))
        time.sleep(0.5)
        jewel.fill((0, 0, 255, 0)) 
        pixel.fill((0, 0, 255))
        time.sleep(0.5)
        jewel.fill((0, 0, 0, 255))
        pixel.fill((0, 0, 0))
        time.sleep(0.5)

def jewel_error_red():
        jewel.brightness = brightness
        jewel.fill((255, 0, 0, 0))
        time.sleep(0.5)
        jewel.fill((0, 0, 0, 0))
        time.sleep(0.5)
        jewel.fill((255, 0, 0, 0))
        time.sleep(0.5)
        jewel.fill((0, 0, 0, 0))

def jewel_bright_white(p_pix, p_switch):
        p_pix.brightness = brightness
        p_pix.fill((0, 0, 0, 255))
        p_pix.show()
        while True:
                p_switch.update()
                if p_switch.long_press or p_switch.short_count != 0:
                        all_blank(p_pix)
                        p_pix.show()
                        break

def jewel_blank():
        jewel.brightness = brightness
        jewel.fill((0, 0, 0, 0))
        jewel.show()

def all_blank(p_pix):
        p_pix.fill((0, 0, 0, 0))

def jewel_indicator(bright, COLOR, delay, times):
        before = jewel.brightness
        jewel.brightness = bright
        jewel.show()
        for x in range(0,times):
            jewel.fill((0, 0, 0, 0))
            jewel.show()
            jewel[0] = COLOR
            jewel.show()
            time.sleep(delay)
            jewel.fill((0, 0, 0, 0))
            jewel.show()
            time.sleep(delay)
        jewel.brightness = before

def bound(value, low, high):
        return max(low, min(high, value))

def mode_1(p_pix, p_switch):
        if DEBUG:
                print("Mode: 1")
        jewel.brightness = .1
        # animation = Blink(jewel, speed=0.25, color=RED)
        animation = Comet(p_pix, 0.05, color.TEAL, tail_length=3)

        while True:
                animation.animate() 
                p_switch.update()
                if p_switch.long_press or p_switch.short_count != 0:
                        animation.reset()
                        all_blank(p_pix)
                        p_pix.show()
                        return
        
def mode_2(p_pix, p_switch):
        mode_DEBUG = False
        if DEBUG:
                print("Mode: 2")
        # fire test
        while True:
                r = 226
                g = 121
                b = 35

                before_brightness = jewel.brightness
                max_brightness = .2
                jewel.brightness = before_brightness

                #Flicker, based on our initial RGB values
                for i in range (0, 7):
                        modifier = random.randint(0,100) / 100
                        temp_bright = bound(modifier * max_brightness, 0, max_brightness)
                        p_pix.brightness = temp_bright

                        if DEBUG and mode_DEBUG:
                                print("fire temp_bright =", temp_bright)

                        flicker = random.randint(0,100)

                        r1 = bound(r-flicker, 0, 255)
                        g1 = bound(g-flicker, 0, 255)
                        b1 = bound(b-flicker, 0, 255)
                        p_pix[i] = (r1,g1,b1)
                        p_pix.show()
                        time.sleep(random.randint(100,500) / 5000)

                p_switch.update()
                if p_switch.long_press or p_switch.short_count != 0:
                        #all_blank(p_pix)
                        #p_pix.show()
                        p_pix.brightness = before_brightness
                        return
                

def mode_3(p_pix, p_switch):
        mode_DEBUG = False
        if DEBUG:
                print("Mode: 3")
        # police test
        while True:
                p_red = (255,0,0,0)
                p_blue = (0,0,255,0)
                p_white = (100,100,100,255)

                before_brightness = p_pix.brightness
                max_brightness = .15

                #Flicker, based on our initial RGB values
                for i in range (0, 7):
                        modifier = random.randint(0,100) / 100
                        temp_bright = bound(modifier * max_brightness, 0, max_brightness)
                        p_pix.brightness = temp_bright
                        
                        chance = random.randint(0,100) / 100
                        if chance < .45:
                                p_color = p_red
                        elif chance <.9:
                                p_color = p_blue
                        else:
                                p_color = p_white

                        flicker = random.randint(0,125)

                        temp_r = bound(p_color[0]-flicker, 0, 255)
                        temp_g = 0 #bound(p_color[1]-flicker, 0, 255)
                        temp_b = bound(p_color[2]-flicker, 0, 255)
                        p2_color = (p_color[0], p_color[1], p_color[2], p_color[3]) 
                        if DEBUG and mode_DEBUG:
                                print("police pixel: chance/color =", chance, "/", p2_color)

                        p_pix[i] = p2_color
                        p_pix.show()
                        time.sleep(random.randint(100,500) / 5000)

                p_switch.update()
                if p_switch.long_press or p_switch.short_count != 0:
                        #all_blank(p_pix)
                        #p_pix.show()
                        p_pix.brightness = before_brightness
                        return


def mode_4(p_pix, p_switch):
        if DEBUG:
                print("Mode: 4")
        jewel.brightness = .2
        # animation = Blink(jewel, speed=0.25, color=RED)
        # animation = Comet(p_pix, 0.05, color.TEAL, tail_length=3)
        animation = Rainbow(p_pix, .05, period=5, step=1, name=None, precompute_rainbow=True)
        while True:
                animation.animate() 
                p_switch.update()
                if p_switch.long_press or p_switch.short_count != 0:
                        animation.reset()
                        all_blank(p_pix)
                        p_pix.show()
                        return

def mode_5(p_pix, p_switch):
        if DEBUG:
                print("Mode: 5")
        jewel.brightness = .2
        # animation = Blink(jewel, speed=0.25, color=RED)
        # animation = Comet(p_pix, 0.05, color.TEAL, tail_length=3)
        # animation = Rainbow(p_pix, .05, period=5, step=1, name=None, precompute_rainbow=True)
        animation = Pulse(p_pix, speed=.005, color=color.CYAN, period=3)

        while True:
                animation.animate() 
                p_switch.update()
                if p_switch.long_press or p_switch.short_count != 0:
                        animation.reset()
                        all_blank(p_pix)
                        p_pix.show()
                        return

def mode_6(p_pix, p_switch):
        if DEBUG:
                print("Mode: 6")
        # REMEMBER
        # jewel_ORDER = neopixel.GRBW 
        p_test = (255,0,0,0) #red
        p_pix.fill(p_test)
        p_pix.show()
        time.sleep(1)
        p_test = (0,255,0,0) #green
        p_pix.fill(p_test)
        p_pix.show()
        time.sleep(1)
        p_test = (0,0,255,0) #blue
        p_pix.fill(p_test)
        p_pix.show()
        time.sleep(1)
        pass

# DICT of animation modes
animations  = { 'mode_1': mode_1,
                'mode_2': mode_2,
                'mode_3': mode_3,
                'mode_4': mode_4,
                'mode_5': mode_5,
                'mode_6': mode_6,}

while True:
        ### Animation section
        # jewel_off()
   
        ### Switch at the end

        switch.update()
        if switch.long_press and switch.short_count == 0:
                # Long Press (alone)
                if DEBUG:
                        print("Long Press")
                # use this as the token to leave an animation if timing is off. 
                # just blank everything after yellow indicator.
                jewel_indicator(.2, (255, 255, 0, 0), .1, 3)
                continue

        if switch.long_press and switch.short_count == 1:
                # long double press!
                if DEBUG:
                        print("That's a long double press !")
                jewel_indicator(.2, (0, 255, 0, 0), .5, 1)
                jewel_bright_white(jewel, switch)
                continue

        if switch.long_press and switch.short_count == 2:
                # long triple press!
                if DEBUG:
                        print("That's a long triple press !")
                # use this as a special token to reset the board
                jewel_indicator(.2, color.JADE, .1, 3)
                supervisor.reload()
                continue

        if switch.short_count != 0 and not switch.long_press:
                # Short Press Count = switch.short_count
                if DEBUG:
                        print("Short Press Count =", switch.short_count)
                jewel_indicator(.2, (0, 0, 255, 0), .25, switch.short_count)

                if  switch.short_count > 0 and switch.short_count <= len(list(animations.keys())):
                        
                        try:
                                method_name = "mode_" + str(switch.short_count)
                                #print("try : ", method_name)
                                animations[method_name](jewel, switch) 
                                # reference function from DICT
                                # pulling out of an animation does something odd in circutpython
                                # if an  animaiton has played, then there needs to be a NeoPixel.show()
                                # after EVERY change to the pixels. Annoying, but can be placed in jewel_indicator()
                                jewel_indicator(.5, (255, 0, 0, 0), .25, 1)
                                continue
                        except Exception as ex:
                                jewel_error_red() 

                                print("Exception in animation code:")
                                print("-"*60)
                                traceback.print_exception(ex)
                                print("-"*60)
                continue