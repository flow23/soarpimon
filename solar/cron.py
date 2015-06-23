import Adafruit_DHT
import random
from rrdtool import update

def SerialPolling():
    # RRD filenames
    rrdBatteryFile = '/webapp/solar_django/solar/solar/media/rrd/battery.rrd' 
    rrdSolarFile = '/webapp/solar_django/solar/solar/media/rrd/solar.rrd'
    rrdAM2302File = '/webapp/solar_django/solar/solar/media/rrd/AM2302.rrd'

    # Sensor should be set to Adafruit_DHT.DHT11,
    # Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
    sensor = Adafruit_DHT.AM2302

    # Example using a Raspberry Pi with DHT sensor
    # connected to pin 14.
    pin = 14

    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Fake data for gods sake
    voltBattery = random.uniform(11, 14)
    ampereBattery = random.uniform(0, 1)
    voltSolar = random.uniform(11, 18)
    ampereSolar = random.uniform(0, 5)

    # Building update string
    #updateString = '%s:%s:%s:%s' % (voltBattery, ampereBattery, voltSolar, ampereSolar)

    # Update round-robin-database
    batteryUpdate = update(rrdBatteryFile, 'N:%s:%s' % (voltBattery, ampereBattery))
    solarUpdate = update(rrdSolarFile, 'N:%s:%s' % (voltSolar, ampereSolar))

    AM2302Update = update(rrdAM2302File, 'N:%s:%s' % (temperature, humidity))


if __name__ == '__main__':
    SerialPolling()
