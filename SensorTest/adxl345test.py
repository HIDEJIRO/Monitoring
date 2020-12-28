#!/usr/bin/env python3

import time
import logging
import csv
import datetime
import board
import busio
import adafruit_adxl34x

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("""
###################################
Press Ctrl+C to exit!
###################################

""")

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.enable_motion_detection()

try:
    while True:
        x = accelerometer.acceleration[0]
        y = accelerometer.acceleration[1]
        z = accelerometer.acceleration[2]

        # コンソール画面表示
        logging.info("""
        XYZ: {:05.02f} {:05.02f} {:05.02f}
        """.format(x, y, z)
        )

        time.sleep(1)

except KeyboardInterrupt:
    pass
