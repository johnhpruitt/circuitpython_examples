import board
import neopixel
import time
from digitalio import DigitalInOut, Direction, Pull

btn = DigitalInOut(board.D2)
btn.direction = Direction.INPUT
btn.pull = Pull.UP

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=.01)

pixel_pin = board.A3
num_pixels = 7
ORDER = neopixel.RGBW

jewel = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=.01, auto_write=True, pixel_order=ORDER)


while True:
    if not btn.value:
        jewel.brightness = 1
        pixel.brightness = 1
        
        jewel.fill((0, 0, 0, 255))
        pixel.fill((0, 0, 0, 255))
        time.sleep(0.5)
    else:
        jewel.brightness = .1
        pixel.brightness = .1
        
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
        pixel.fill((0, 0, 0, 255))
        time.sleep(0.5)