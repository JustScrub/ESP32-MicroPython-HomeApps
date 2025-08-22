
from wget import wget
from env import *

def wifi_connect():
    import network
    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ipconfig('addr4'))

if __name__ == '__main__':
   wifi_connect()