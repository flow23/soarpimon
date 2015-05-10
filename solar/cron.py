import os.path
import logging, random, serial, time
from solar import settings
from rrdtool import update

def SerialPolling():
    # RRD filenames
    rrdBatteryFile = '/webapp/solar/solar/solar/media/rrd/battery.rrd' 
    rrdSolarFile = '/webapp/solar/solar/solar/media/rrd/solar.rrd'

    # Serial tranmission flags
    transmissionSuccessful = ''
    transmissionTimeout = ''

    # Serial setup
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=55)

    start_time = time.time()

    while transmissionSuccessful == '' and transmissionTimeout == '':
        incoming = ser.readline().strip()
        #logger.info('Serial received %s', incoming)
        #ser.write('RPi Received: %s\n' % incoming)

        incomingSplit = str(incoming).split("|")
        incomingCount = len(incomingSplit)

        if incomingCount == 6:
            incomingFirstValue = incoming.split('|')[0]
            incomingLastValue = incoming.split('|')[5]

            if (incomingFirstValue == 'bt' and incomingLastValue == 'et'):
                #logger.info('Complete transmission received')

                voltBattery = incoming.split('|')[1]
                ampereBattery = incoming.split('|')[2]
                voltSolar = incoming.split('|')[3]
                ampereSolar = incoming.split('|')[4]

                #logger.debug('voltBattery: %s', voltBattery)
                #logger.debug('ampereBattery: %s', ampereBattery)
                #logger.debug('voltSolar: %s', voltSolar)
                #logger.debug('ampereSolar: %s', ampereSolar)

                transmissionSuccessful = 'x'
            #else:
                #logger.info('Tranmission is invalid')

        # Runtime
        elapsed_time = time.time() - start_time

        if elapsed_time > 50:
            #logger.info('Timeout reached')
            transmissionTimeout = 'x'

            # Fake data for gods sake
            voltBattery = random.uniform(11, 14)
            ampereBattery = random.uniform(0, 1)
            voltSolar = random.uniform(11, 18)
            ampereSolar = random.uniform(0, 5)

    # Time after successful transmission
    elapsed_time = time.time() - start_time

    #logger.info('Elapsed time: %s', elapsed_time)

    updateString = '%s:%s:%s:%s' % (voltBattery, ampereBattery, voltSolar, ampereSolar)

    #logger.debug('Update rrd: %s', updateString)
    #print updateString

    #voltBattery = string.split(':')[0]
    #ampereBattery = string.split(':')[1]
    #voltSolar = string.split(':')[2]
    #ampereSolar = string.split(':')[3]

    batteryUpdate = update(rrdBatteryFile, 'N:%s:%s' % (voltBattery, ampereBattery))
    solarUpdate = update(rrdSolarFile, 'N:%s:%s' % (voltSolar, ampereSolar))

if __name__ == '__main__':
    SerialPolling()
