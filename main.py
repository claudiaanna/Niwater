# from smbus import SMBus
import time
import noteCenter
import logging
import json
import datetime

ADS = 0x48
LGT = 0x40
TMP = 0x41
HMT = 0x42
PTN = 0x43
RES = 255

SLEEP_TIME = 7200 #2h
# bus = SMBus(1)

filename = ('logfile_Niwater.log')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-5s %(message)s', datefmt='%m-%d %H:%M',
                    filename=filename, filemode='a')

def readRawData(channel):
    bus.write_byte(ads, channel)
    return bus.read_byte(ads)

def readVoltageData(channel):
    return readRawData(channel) * 3.3 / res

lastSts = -1
lastHmt = -1

while True:
    currentHmt = 300 #readRawData(HMT)
    if abs(currentHmt - lastHmt) > 10:
        if currentHmt < 300:
            message = 'Soil is dry. Watering is needed!'
            currentSts = 1
        elif 300 <= currentHmt < 700:
            message = 'Soil is properly moist.'
            currentSts = 2
        elif 700 <= currentHmt:
            message = 'Soil is too damp!'
            currentSts = 3
        logging.info('{} {}'.format('Measured humidity: {} '.format(currentHmt), message))
        if (currentSts != lastSts):
            noteCenter.sendNotification(message)

        lastSts = currentSts
        lastHmt = currentHmt
    break
    # time.sleep(SLEEP_TIME)