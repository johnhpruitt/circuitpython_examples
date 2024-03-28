# gas_sensor

> :warning: **SAFETY NOT GUARANTEED**: Never trust an idiot on the internet!
> **Without knowing the composition of the gasses in the environment it wont be possible to assert a specific value as hazardous or not. 
> This project should not be used in any safety critical systems.**
> Your safety is important, and also your own responsibility. Follow all local laws and regulations.
> 
## References 
- https://www.hackster.io/agxies/raspberry-pi-temperature-and-co2-monitor-a881aa

## Pimoroni Pico lipo layout

|          USE          |       PROTOCOL        | LABEL | PIN |     MIDDLE     | PIN |  LABEL   |       PROTOCOL        |       USE       |
| :-------------------: | :-------------------: | :---: | :-: | :------------: | :-: | :------: | :-------------------: | :-------------: |
|                       |      SPI0 / i2c0      |  GP0  |  1  |    USB/TOP     | 40  |   VBUS   |        USB 5v         |                 |
|                       |      SPI0 / i2c0      |  GP1  |  2  |                | 39  |   VSYS   |        Ext. 5v        |     GAS VCC     |
| GAS GND (and/or WAKE) |                       |  GND  |  3  |                | 38  |   GND    |          GND          |                 |
|        GAS SDA        |      SPI0 / i2c1      |  GP2  |  4  |                | 37  |  3V3_EN  |         RESET         |                 |
|        GAS SCL        |      SPI0 / i2c1      |  GP3  |  5  |                | 36  | 3V3_OUT  |       Ext. 3.3v       | OLED, ESP01 VCC |
|                       |      SPI0 / i2c0      |  GP4  |  6  |                | 35  | ADC_VREF |                       |                 |
|                       |      SPI0 / i2c0      |  GP5  |  7  |                | 34  |   GP28   |                       |                 |
|      (GAS WAKE)       |                       |  GND  |  8  |                | 33  |   GND    |                       |    ESP01 GND    |
|                       |      SPI0 / i2c1      |  GP6  |  9  |                | 32  |   GP27   |         i2c1          |                 |
|                       |      SPI0 / i2c1      |  GP7  | 10  |                | 31  |   GP26   |         i2c1          |                 |
|       ESP01 RX        | SPI1 / i2c0 / UART1TX |  GP8  | 11  |                | 30  |   RUN    |         RESET         |                 |
|       ESP01 TX        | SPI1 / i2c0 / UART1RX |  GP9  | 12  |                | 29  |   GP22   |                       |                 |
|                       |                       |  GND  | 13  |                | 28  |   GND    |                       |                 |
|                       |      SPI1 / i2c1      | GP10  | 14  |                | 27  |   GP21   |         i2c0          |                 |
|       OLED RES        |      SPI1 / i2c1      | GP11  | 15  |                | 26  |   GP20   |         i2c0          |                 |
|        OLED DC        |      SPI1 / i2c0      | GP12  | 16  |                | 25  |   GP19   |      SPI0 / i2c1      |                 |
|        OLED CS        |      SPI1 / i2c0      | GP13  | 17  | I2C0 (GP4,GP6) | 24  |   GP18   |      SPI0 / i2c1      |                 |
|       OLED GND        |                       |  GND  | 18  |                | 23  |   GND    |                       |                 |
|    OLED CLK (SCL)     |      SPI1 / i2c1      | GP14  | 19  |                | 22  |   GP17   | SPI0 / i2c0 / UART0RX |                 |
|    OLED MOSI (SDA)    |      SPI1 / i2c1      | GP15  | 20  |  LIPO HEADER   | 21  |   GP16   | SPI0 / i2c0 / UART0TX |                 |

## Parts and Manufacturer Documentation
### PICO pinout
https://pico.pinout.xyz/pimoroni-pico-lipo

### Pimoroni Pico in CircuitPython
```
>>> dir(board)
['__class__', '__name__', 'A0', 'A1', 'A2', 'A3', 'BAT_SENSE', 'GP0', 'GP1', 'GP10', 'GP11', 'GP12',
 'GP13', 'GP14', 'GP15', 'GP16', 'GP17', 'GP18', 'GP19', 'GP2', 'GP20', 'GP21', 'GP22', 'GP25', 'GP26',
 'GP26_A0', 'GP27', 'GP27_A1', 'GP28', 'GP28_A2', 'GP3', 'GP4', 'GP5', 'GP6', 'GP7', 'GP8', 'GP9', 'I2C',
 'LED', 'SCL', 'SDA', 'STEMMA_I2C', 'USER_SW', 'VBUS_DETECT', 'board_id']
```

### Inland Inland IIC SPI 128x64 OLED Module
https://www.microcenter.com/product/643965/inland-iic-spi-13-128x64-oled-v20-graphic-display-module-for-arduino-uno-r3
https://wiki.keyestudio.com/Ks0056_keyestudio_1.3%22_128x64_OLED_Graphic_Display

### Inland CCS811 Module
https://www.microcenter.com/product/632703/inland-ccs811-air-quality-sensor-module
https://wiki.keyestudio.com/KS0457_keyestudio_CCS811_Carbon_Dioxide_Air_Quality_Sensor

According to Keyestudio the pinout is:
| Pin  | Purpose                                                                                                      |
| :--: | :----------------------------------------------------------------------------------------------------------- |
| GND  | Ground                                                                                                       |
| VCC  | Input power (5v)                                                                                             |
| SDA  | I2C Data pin                                                                                                 |
| SCL  | I2c Click pin                                                                                                |
| RST  | Reset pin: Connect to ground, sensor will reset                                                              |
| WAKE | WAKE pin should connect to ground to communicate with sensor conveniently                                    |
| INT  | This is the interrupt output pin that detects when a new reading is ready or the reading is too high or low. |

### Inland ESP8266 Module
https://community.microcenter.com/kb/articles/665-inland-8266-wifi-module-2pcs
https://www.microcenter.com/product/616024/inland-esp8266-wifi-transceiver-receiver-module-2-pack
https://wiki.keyestudio.com/KS0339_Keyestudio_8266_WIFI_Module_2PCS
(The microcenter store page references KS0338, but that's an unrelated NRF24L01 module.)

## References and reasons for pin choices
- Inland ESP8266 with circuitpython
  - https://www.instructables.com/Webserver-Using-Pi-Pico-and-ESP01/
  - Connection between the ESP8266 and pico is serial.
  
- Inland CCS811 with circuitpython
  - According to the Keyestudio docs, VCC for this module should be 5v, not 3.3v like the adafruit module.
  - I moved the gas sensor module to i2c1 because i2c0 is also on the stemmaQT connector.
  - https://learn.adafruit.com/adafruit-ccs811-air-quality-sensor/python-circuitpython
  - Ground WAKE pin to keep module in serial mode. 
  - I could pull a pin low to reset the module, but the adafruit library has a function to do it.
    - https://docs.circuitpython.org/projects/ccs811/en/latest/index.html
  - In the future, it would be interesting to use the INT pin as an input to the pico.
    - could wait for an event on this instead of CCS811.data_ready
  
- Inland OLED with circuitpython
  - https://joe.blog.freemansoft.com/2023/01/inland-iic-spi-13-128x64-oled-v20.html
  - micropython, but this is the pinout I used.
  - default is SPI on the oled board, but you could desolder a jumper to change it. 
  - after some reading, a lot of OLED modules have a virtual size about 2 pixels wider than 128 (so 132 or more)
  - The SH1107 driver in circuitpython has an offest for this, but this uses SH1106 who does not have an offset. 
  - Fast solution is:
    - just set the size to 130 to blank the 2 columns on the right
    - and do not draw on the left edge for 2 pixels
    - I also rotated the screen for my build. 
 
