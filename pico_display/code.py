"""
This script uses a pico display pack to make a simple GUI

File Structure:
    boot_out.txt   |    .gitignore, circuitpython
    code.py        |    main script
    examples/      |    .gitignore, developer examples
    lib/           |    3rd party circuitpython libraries
    wifi.toml      |    wifi configuration
        
Todo:
    * buttons
    * led
    * wifi
    * scrolling text

References: 
    http://helloraspberrypi.blogspot.com/2021/01/raspberry-pi-picocircuitpython-st7789.html
    https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/examples/pico_display
"""

import os
import time
import board
import busio
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_st7789 import ST7789

#===============#
# display block #
#===============#

# some display parameters
BORDER = 6
FONTSCALE = 2
BACKGROUND_COLOR = 0x000D1B
FOREGROUND_COLOR = 0x001935
TEXT_COLOR = 0x00B300

# Release any resources currently in use for the displays
displayio.release_displays()
tft_cs = board.GP17
tft_dc = board.GP16
spi_mosi = board.GP19
spi_clk = board.GP18
spi = busio.SPI(spi_clk, spi_mosi)
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(
    display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53
)

# Make the display context
splash = displayio.Group()
display.show(splash)
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(
    display.width - BORDER * 2, display.height - BORDER * 2, 1
)
inner_palette = displayio.Palette(1)
inner_palette[0] = FOREGROUND_COLOR
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

# Draw a label
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
text_width = text_area.bounding_box[2] * FONTSCALE
text_group = displayio.Group(
    scale=FONTSCALE,
    x=display.width // 2 - text_width // 2,
    y=display.height // 2,
)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)

#============#
# main block #
#============#
 
time.sleep(1.0) 
#displayio.release_displays()
splash = displayio.Group()
display.show(splash)

while True:
    pass
