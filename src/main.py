from machine import ADC, Pin, I2C, RTC
import bh1750fvi
import bme280
from time import sleep, sleep_ms,  time
import network
import urequests
import ujson
import ure
from config import *
import ufirebase as ufb
import icon

i2c = I2C(scl=Pin(22), sda=Pin(19))
bme = bme280.BME280(i2c=i2c)
pinin0 = ADC(Pin(33))
pinin0.atten(ADC.ATTN_11DB)
rtc = RTC()

sta_if = network.WLAN(network.STA_IF)
headers = {"content-type": "application/json"}

print('i2c address:', i2c.scan())

for i in range(3):
    icon.heart()
    sleep_ms(200)
    icon.reset()
    sleep_ms(200)

while True:
    lux = bh1750fvi.sample(i2c)
    temperature, pressure, humidity = [
        float(ure.search("\\d+\.\\d+", x).group(0)) for x in bme.values]
    s_humid0 = pinin0.read()
    if s_humid0 > 4000:
        icon.cross()
    else:
        icon.circle()

    date = '{0:4d}-{1:02d}-{2:02d} {4:02d}:{5:02d}:{6:02d}'.format(
        *rtc.datetime())

    print('-'*40)
    print(date)
    print('{}lux {}C {}hPa {}%'.format(
        lux, temperature, pressure, humidity))
    print(s_humid0)

    if sta_if.isconnected():
        try:
            ufb.patch(FBURL, {date: {'temperature': temperature,
                                     'pressure': pressure, 'humidity': humidity,
                                     'lux': lux, 'soil_humidity': [s_humid0]}})
        except Exception as e:
            # [Errno 104] ECONNRESET が発生するがサーバー側には正常にpostされてる
            print('Error occured :', e)
    else:
        print('wifi lost')
    sleep(60*15)
