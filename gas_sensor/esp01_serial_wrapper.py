import busio
import board
# import ticks to avoid calls to time.sleep()
from adafruit_ticks import ticks_ms, ticks_add, ticks_less

class ESP01wrapper:
    """
    Wrapper for the serial commands to a ESP-01 co-processor.
    This is written because the circuitpython examples are written to take
    advantage of a co-processor with a special firmware, and that doesnt support esp-01.

    https://learn.adafruit.com/adding-a-wifi-co-processor-to-circuitpython-esp8266-esp32/program-esp8266-via-circuitpython

    And most other wrappers are written for micropython instead of circuitpython. 
    https://circuitdigest.com/microcontroller-projects/interfacing-esp8266-01-wifi-module-with-raspberry-pi-pico 
    https://github.com/Circuit-Digest/rpi-pico-micropython-esp8266-lib/tree/main
    
    If I could have found an existing project to use instead, I would have.

    References for AT commands:
    https://duino4projects.com/getting-started-with-the-esp8266-esp-01/

    Input dictionaries look like this:

    conections_dict:
    {0: 'connection_0', 1: 'connection_1'}
    (For keeping track of which connection to use)

    wifi_dict:
    {'connection_0': {'SSID': 'SSID', 'PASSWORD': 'pass'}, 'connection_1': {'SSID': 'SSID', 'PASSWORD': 'pass'}}
    (JSON file for all the passes parsed into a dictionary)
    """

    def __init__(self, UART, conections_dict, wifi_dict, verbose = True):
        self.ssid = None
        self.password = None
        self.connections_dict = conections_dict
        self.wifi_dict = wifi_dict
        self.chosen_connection = 0
        self.found_stations_dict = {}
        self.verbose = verbose
        # Initialize uart object based on parameters
        self.uart = UART
    # Function to handle reading from the uart serial to a buffer
    # https://www.instructables.com/Webserver-Using-Pi-Pico-and-ESP01/
    def SerialRead(self, mode):
        SerialRecv = ""
        if mode == "0" :
            SerialRecv=str(uart.readline())
        else:
            SerialRecv=str(uart.read(mode))
        # replace generates less errors than .decode("utf-8")
        SerialRecv=SerialRecv.replace("b'", "")
        SerialRecv=SerialRecv.replace("\\r", "")
        SerialRecv=SerialRecv.replace("\\n", "\n")
        SerialRecv=SerialRecv.replace("'", "")
        return SerialRecv
        
    # http://helloraspberrypi.blogspot.com/2021/02/connect-esp-01s-esp8266-to-raspberry-pi.html
    def sendCMD_waitResp(self, cmd, uart, timeout=2000):
        print("CMD: " + cmd.decode())
        uart.write(cmd)
        message = self.waitResp(uart, timeout)
        print()
        return message
        
    # http://helloraspberrypi.blogspot.com/2021/02/connect-esp-01s-esp8266-to-raspberry-pi.html
    def waitResp(self, uart, timeout=2000):
        prvMills = ticks_ms()
        resp = b""
        while (ticks_ms()-prvMills)<timeout:
            #if uart.any():
            for i in range(uart.in_waiting):
                resp = b"".join([resp, uart.read(1)])
        print("resp:")
        try:
            print(resp.decode())
            return resp.decode()
        except UnicodeError:
            print(resp)
            return None

    def search_stations(self, wait, limit):
        # wait = time to wait for response 
        # limit = limit the number of search attempts
        self.sendCMD_waitResp(b'AT\r\n', self.uart, timeout=wait)               #Test AT startup
        test = self.sendCMD_waitResp(b'AT+GMR\r\n', self.uart, timeout=2000)           #Check version information
        print("test: " + str(test[-4:-2]))
        
        response = self.sendCMD_waitResp(b'AT+CWLAP\r\n', self.uart, timeout=wait) #List available APs
        attempts = 0
        #the length of the response under 25 indicates there was not even one SSID found.
        while len(response) < 25 and attempts < limit:
            wait += 1000
            print("WAIT: " + str(wait/1000) +"s")
            response = self.sendCMD_waitResp(b'AT+CWLAP\r\n', self.uart, timeout=wait) #List available APs
            attempts += 1
        
        
        return response

"""
# wifi example serial commands.
sendCMD_waitResp(b'AT\r\n', uart, timeout=2000)          			    #Test AT startup
sendCMD_waitResp(b'AT+GMR\r\n', uart, timeout=2000)      			    #Check version information
sendCMD_waitResp(b'AT+RESTORE\r\n', uart, timeout=2000)  			    #Restore Factory Default Settings
sendCMD_waitResp(b'AT+CWMODE?\r\n', uart, timeout=2000)  			    #Query the Wi-Fi mode
sendCMD_waitResp(b'AT+CWMODE=1\r\n', uart, timeout=2000) 			    #Set the Wi-Fi mode = Station mode
sendCMD_waitResp(b'AT+CWMODE?\r\n', uart, timeout=2000)  			    #Query the Wi-Fi mode again
sendCMD_waitResp(b'AT+CWLAP\r\n', uart, timeout=10000) 			        #List available APs
sendCMD_waitResp(b'AT+CWJAP="ssid","password"\r\n',uart, timeout=5000) 	#Connect to AP
sendCMD_waitResp(b'AT+CIFSR\r\n', uart, timeout=10000)    			    #Obtain the Local IP Address
"""