
# Pimoroni Pico Lipo 16mb
# >>> dir(board)
# ['__class__', '__name__', 'A0', 'A1', 'A2', 'A3', 'BAT_SENSE', 'GP0', 'GP1', 'GP10', 'GP11', 'GP12',
#  'GP13', 'GP14', 'GP15', 'GP16', 'GP17', 'GP18', 'GP19', 'GP2', 'GP20', 'GP21', 'GP22', 'GP25', 'GP26',
#  'GP26_A0', 'GP27', 'GP27_A1', 'GP28', 'GP28_A2', 'GP3', 'GP4', 'GP5', 'GP6', 'GP7', 'GP8', 'GP9', 'I2C',
#  'LED', 'SCL', 'SDA', 'STEMMA_I2C', 'USER_SW', 'VBUS_DETECT', 'board_id']

#------------------------------------------------------------------------------#
# IMPORT STATEMENTS
#------------------------------------------------------------------------------#

import os
import board
import time
import terminalio
import displayio
import busio

# Display Text
from adafruit_display_text import label
from adafruit_display_text.scrolling_label import ScrollingLabel
from adafruit_progressbar.horizontalprogressbar import (
    HorizontalProgressBar,
    HorizontalFillDirection,
)

# Needed for Voltage / Battery
import analogio
import digitalio

# OLED
import adafruit_displayio_sh1106

# ccs811 gas sensor
# also requires adafruit_register
# I2C address for inland ccs811: ['0x5a']
import adafruit_ccs811

# Imports for Wifi and it's config
import json

#------------------------------------------------------------------------------#
# Function Definitions
#------------------------------------------------------------------------------#

# Adafruit function for enumerating I2C addresses
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-i2c
def enumerate_i2c(i2c):
    try:
        while True:
            print(
                "I2C addresses found:",
                [hex(device_address) for device_address in i2c.scan()],
            )
            time.sleep(2)

    finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
        i2c.unlock()

def init_battery():
    # Set up battery voltage
    vsys = analogio.AnalogIn(board.A3)
    # reads the system input voltage

    # In Pimoroni branded micropython, this is GP24.
    # Adafruit circuitpython has no GP24 for this board, but it has VBUS_DETECT.
    charging = digitalio.DigitalInOut(board.VBUS_DETECT)
    # reading GP24 tells us whether or not USB power is connected

    
    # Emojis arent in the default font, even though the circuitpython snake 
    # shows up on the oled in a debug event? That's a little odd.
    # charging indicator symbol set to ^
    # reference voltages for a full/empty battery, in volts
    # defaults are 2.8 to 4.2
    # the values could vary by battery size/manufacturer so you might need to adjust them
    battery_dict = {
    'show_percent': True,
    'lightning': '^',
    'full_battery': 4.30,
    'empty_battery': 2.8,
    } 

    return (vsys, charging, battery_dict)

def get_voltage(raw):
    return ((raw * 3.3) / 65536)*3

def battery_string(voltage, battery_dict):
     # convert the raw ADC read into a voltage, and then a percentage
    percentage = 100 * ((voltage - battery_dict["empty_battery"]) / (battery_dict["full_battery"] - battery_dict["empty_battery"]))
    if percentage > 100:
        percentage = 100

    if battery_dict["show_percent"]:
        percent_string = " - " + str(round(percentage)) + "%"
    else:
        percent_string = ""

    if charging.value:
        footer_text = "BATT:" +  battery_dict["lightning"] + str(round(voltage,2)) + "v" + percent_string
    else: 
        footer_text = "BATT: " + str(round(voltage,2)) + "v" + percent_string
    return footer_text

def read_wifi_json():
    try:
        with open("/wifi.json", "r") as fp:
            wifi_json = json.load(fp)
            #print(wifi_json)
            i = 0
            conections_dict = {}
            for key, value in wifi_json.items():
                conections_dict.update({i:key})
                i += 1
            print("wifi.json options: "+str(conections_dict))
            return(conections_dict,wifi_json)
    except OSError as error:  # Typically when the filesystem isn't writeable...
        print(str(error))
        return None

# Function to handle reading from the uart serial to a buffer
# https://www.instructables.com/Webserver-Using-Pi-Pico-and-ESP01/
def SerialRead(mode):
    SerialRecv = ""
    if mode == "0" :
        SerialRecv=str(uart.readline())
    else:
        SerialRecv=str(uart.read(mode))
    #replace generates less errors than .decode("utf-8")
    SerialRecv=SerialRecv.replace("b'", "")
    SerialRecv=SerialRecv.replace("\\r", "")
    SerialRecv=SerialRecv.replace("\\n", "\n")
    SerialRecv=SerialRecv.replace("'", "")
    return SerialRecv
#------------------------------------------------------------------------------#
## SET UP STEPS FOR THE MAIN LOOP
## SHOULD NOT DEFINE ANY FUNCTIONS BELOW THIS LINE
## Variables should not be defined above this line, for readability
#------------------------------------------------------------------------------#
  
# Could move this to a function, but the OLED is all the monitoring 
# this project has so far. So, it would be silly to run without OLED plugged in. 
# Set up display
displayio.release_displays()

spi = busio.SPI(board.GP14, board.GP15)
display_bus = displayio.FourWire(
    spi,
    command=board.GP12,
    chip_select=board.GP13,
    reset=board.GP11,
    baudrate=1000000,
)

# The inland OLED has an offset of 2 but, circuit python doesnt
# have an offset definition for sh1106 like it does for sh1107.
# Plus, for the board I'm using it will be upside down. 
# so setting width to 130 is mostly suffiencent to fix things.
# (130, not 132 or 128)

WIDTH = 130
HEIGHT = 64
BORDER = 3
display = adafruit_displayio_sh1106.SH1106(display_bus, width=WIDTH, height=HEIGHT,rotation=180)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

# Top Line
header_text = "Air Quality Monitor"
header_text_area = label.Label(
    terminalio.FONT, text=header_text, color=0xFFFFFF, x=0, y=6
)
splash.append(header_text_area)

# Line 0
# Underlines the top title line. Turn this off if the characters extend below
underline_title = True
if underline_title:
    line0_text = "_____________________"
    line0_text_area = label.Label(
        terminalio.FONT, text=line0_text, color=0xFFFFFF, x=0, y=8
    )
    splash.append(line0_text_area)

# Line 1
line1_text = "ECO2: "
line1_text_area = label.Label(
    terminalio.FONT, text=line1_text, color=0xFFFFFF, x=0, y=20  
)
splash.append(line1_text_area)

# Line 2
line2_text = "TVOC: "
line2_text_area = label.Label(
    terminalio.FONT, text=line2_text, color=0xFFFFFF, x=0, y=30 , line_spacing = 0.8
)
splash.append(line2_text_area)

# Footer Line
footer_text = "FOOTER_TEXT_INIT"
footer_text_area = label.Label(
    terminalio.FONT, text=footer_text, color=0xFFFFFF, x=0, y=58
)
splash.append(footer_text_area)

# Set up Gas Sensor
# i2c = busio.I2C(board.SCL1, board.SDA1)
# i2c object is a singleton
i2c = busio.I2C(board.GP3, board.GP2)
ccs811 =  adafruit_ccs811.CCS811(i2c)

# Shows a horizonal progress bar sweeping between sensor polls.
# timing is set in the loop for updating the screen / sensor poll
# by updating progress_bar.value
show_sweeper = True
if show_sweeper:
    # Create a new progress_bar object at (x, y)
    progress_bar = HorizontalProgressBar(
        (5, 40), (115, 10), direction=HorizontalFillDirection.LEFT_TO_RIGHT
    )
    splash.append(progress_bar)
    sweeper_value = progress_bar.minimum

if os.getenv("BATTERY_ENABLED") == 'True':
    show_battery = True
else:
    show_battery = False

if show_battery:
    (vsys, charging, battery_dict) = init_battery()

# Read wifi config file
(conections_dict,wifi_json) = read_wifi_json()

# Determine if there is enough information to start internet connection. 
attempt_wifi = False
if os.getenv("WIFI_ENABLED") == 'True':
    if len(conections_dict) > 0:
        wifi_ssid = wifi_json[conections_dict[0]]['SSID']
        wifi_password = wifi_json[conections_dict[0]]['PASSWORD']
        if wifi_ssid is not None and wifi_password is not None:
            print("Wifi configurtion found.")
            attempt_wifi = True
            footer_text = "Looking for WIFI"
            footer_text_area.text = footer_text

if attempt_wifi:
    print("Test")
    try:
        uart = busio.UART(board.GP8, board.GP9, baudrate=115200)
        while True:
            #data = uart.read(32)
            #print(str(data))
            test = uart.read(32)
            print(test)
            footer_text_area.text =  test
    except Exception as error:
        print(str(error))

# Some debug prints
print( "BATTERY_ENABLED = " + str(os.getenv("BATTERY_ENABLED")))
print( "WIFI_ENABLED = " + str(os.getenv("WIFI_ENABLED")))

#------------------------------------------------------------------------------#
## MAIN EXECUTION LOOP
#------------------------------------------------------------------------------#
while True:
    # CCS811 text display
    if not ccs811.data_ready:
        line1_text = "  CCS811  "
        line2_text = "NOT READY!"
        line1_text_area.text = line1_text
        line2_text_area.text = line2_text
    else:
        line1_text = "ECO2: " + str(ccs811.eco2)
        line2_text = "TVOC: " + str(ccs811.tvoc)
        line1_text_area.text = line1_text
        line2_text_area.text = line2_text

    if show_battery:
        raw = vsys.value
        voltage = get_voltage(raw)
        footer_text = battery_string(voltage, battery_dict)
        footer_text_area.text = footer_text

    if show_sweeper:
        for current_value in range(progress_bar.minimum, progress_bar.maximum + 1, 1):
            progress_bar.value = current_value
            #it will take 100 inner loops per outer loop since bar.max = 100
            time.sleep(1/100)
    else:
        time.sleep(01)
    pass
