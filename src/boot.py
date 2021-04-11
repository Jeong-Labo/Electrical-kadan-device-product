from machine import Pin, RTC, reset
import network
import urequests
from config import *

rtc = RTC()


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        ap_if.active(False)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass

    print('network config:', sta_if.ifconfig())


def setRtc():
    url_jst = "http://worldtimeapi.org/api/timezone/Asia/Tokyo"

    retry_delay = 5000  # interval time of retry after a failed Web query
    response = urequests.get(url_jst)

    # parse JSON
    parsed = response.json()
    # parsed=ujson.loads(res) # in case string
    datetime_str = str(parsed["datetime"])
    year = int(datetime_str[0:4])
    month = int(datetime_str[5:7])
    day = int(datetime_str[8:10])
    hour = int(datetime_str[11:13])
    minute = int(datetime_str[14:16])
    second = int(datetime_str[17:19])
    subsecond = int(round(int(datetime_str[20:26]) / 10000))

    # update internal RTC
    rtc.datetime((year, month, day, 0, hour, minute, second, subsecond))
    response.close()


if __name__ == '__main__':
    # reset()
    do_connect()
    setRtc()
    print('{0:4d}-{1:02d}-{2:02d} {4:02d}:{5:02d}:{6:02d}'.format(*rtc.datetime()))
