#!/usr/bin/env python3

import time
import csv
import datetime
import board
import busio
import adafruit_tsl2561
import adafruit_adxl34x
import bme680

state = 2

# BME680
try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

print('Calibration data:')
for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

        if isinstance(value, int):
            print('{}: {}'.format(name, value))

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)


print('\n\nInitial reading:')
for name in dir(sensor.data):
    value = getattr(sensor.data, name)

    if not name.startswith('_'):
        print('{}: {}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the TSL2561 instance, passing in the I2C bus
tsl = adafruit_tsl2561.TSL2561(i2c)


#i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.enable_motion_detection()


try:
    while True:
        # LTR559 light sensor
        lux = tsl.lux

        temperature = sensor.data.temperature
        humidity = sensor.data.humidity

        x = accelerometer.acceleration[0]
        y = accelerometer.acceleration[1]
        z = accelerometer.acceleration[2]

        if sensor.get_sensor_data():
            output = ''
            temperature = sensor.data.temperature
            humidity = sensor.data.humidity

            if sensor.data.heat_stable:
                print('{0} Ohms'.format(sensor.data.gas_resistance))
                gas = sensor.data.gas_resistance
            else:
                print(output)

        print("""
        Light: {:05.02f} Lux {:05.02f} C,{:05.02f} %RH XYZ: {:05.02f} {:05.02f} {:05.02f} 
        """.format(lux,temperature,humidity,x, y, z )
        )

        # CSVファイルに追記
        now = datetime.datetime.now()
        recordtime = '{0:%Y%m%d %H:%M:%S}'.format(now)
        filename = '/home/pi/Monitoring/logs/log_' + now.strftime('%Y%m%d') + '.csv'
        data = recordtime + ",{:04},{:05.02f},{:05.02f},{:05.02f},{:05.02f},{:05.02f},{:05.02f}".format(state, lux, temperature, humidity, x, y, z)
        with open( filename, 'a') as f:
            print( data, file=f)

        time.sleep(6)

except KeyboardInterrupt:
    pass
