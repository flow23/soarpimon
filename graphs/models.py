import datetime, logging, rrdtool, os

from django.db import models
from django.utils import timezone
from solar import settings

# Get a logger instance
logger = logging.getLogger(__name__)

class SolarGraphManager(models.Manager):
    def get_queryset(self):
        return super(SolarGraphManager, self).get_queryset().filter(category='solar')

class BatteryGraphManager(models.Manager):
    def get_queryset(self):
        return super(BatteryGraphManager, self).get_queryset().filter(category='battery')

class StatusGraphManager(models.Manager):
    def get_queryset(self):
        return super(StatusGraphManager, self).get_queryset().filter(displayOnStatusPage=True)

class WeatherGraphManager(models.Manager):
    def get_queryset(self):
        return super(WeatherGraphManager, self).get_queryset().filter(category='weather')

class Graph(models.Model):
    CATEGORIES = (
        ('solar', 'Solar'),
        ('battery', 'Battery'),
        ('wattage', 'Wattage'),
        ('weather', 'Weather'),
    )
    category = models.CharField(max_length=7, choices=CATEGORIES)

    description = models.CharField(max_length=100,default='description')

    rrdFilename = models.FileField(upload_to='rrd/', blank=True)
    imageFilename = models.ImageField(upload_to='graph/', blank=True)

    TIMEPERIODS = (
        (3600, '1hour'),
        (43200, '12hours'),
        (86400, '1day'),
        (604800, '1week'),
        (2419200, '1month'),
        (14515200, '6months'),
        (29030400, '1year'),
    )
    timePeriod = models.IntegerField(choices=TIMEPERIODS, default=3600)
    start = models.CharField(max_length=50,default='end-3600')
    end = models.CharField(max_length=50,default='now')

    UNITS = (
        ('A', 'Ampere'),
        ('C', 'Celsius'),
        ('P', '%'),
        ('V', 'Volt'),
        ('W', 'Wattage'),
    )
    unit = models.CharField(max_length=3, choices=UNITS, default='A')

    lineColor = models.CharField(max_length=9,default='#00000066')
    areaColor = models.CharField(max_length=9,default='#00000066')

    verticalLabel = models.CharField(max_length=50,default='verticalLabel',blank=True)
    watermark = models.CharField(max_length=50,default='watermark',blank=True)
    width = models.IntegerField(default='640')
    height = models.IntegerField(default='180')
    upperLimit = models.IntegerField(blank=True)
    lowerLimit = models.IntegerField(default='0',blank=True)
    lowerLimitRigid = models.BooleanField(default=True)

    displayOnStatusPage = models.BooleanField(default=False)

    lastChange = models.DateTimeField('last change', auto_now=True)
    generationDate = models.DateTimeField('date generated', default=timezone.now)

    # Manager stuff
    objects = models.Manager()
    batteryObjects = BatteryGraphManager()
    solarObjects = SolarGraphManager()
    statusObjects = StatusGraphManager()
    weatherObjects = WeatherGraphManager()

    def generateComparisonGraph(self):
        logger.info('BEGIN')

        #graphDestinationFilename = ''.os.path.join([settings.MEDIA_ROOT, '/..' , self.imageFilename.url])
        #import pdb; pdb.set_trace()
        #abnc = settings.MEDIA_ROOT

        if (self.category == 'solar'):
            definitionOne = 'ampere'
            definitionOneShift= 'ampereShift'
        elif (self.category == 'battery'):
            definitionOne = 'volt'
            definitionOneShift= 'voltShift'
        elif (self.category == 'weather'):
            if (self.unit == 'C'):
                definitionOne = 'temperature'
                definitionOneShift= 'temperatureShift'
            elif (self.unit == 'P'):
                definitionOne = 'humidity'
                definitionOneShift= 'humidityShift'
            else:
                definitionOne = 'example'
                definitionOneShift= 'exampleShift'
        else:
            definitionOne = 'solar'
            definitionOneShift= 'solarShift'

        if (self.lowerLimitRigid == True):
            lowerLimitRigid = '--rigid'
        else:
            lowerLimitRigid = ''

        self.generationDate = timezone.now()

        try:
            rrdtoolGraph = rrdtool.graph(''.join([settings.MEDIA_ROOT, '/..' ,self.imageFilename.url]),
                "--start", "end-%s" % (self.timePeriod),
                "--end", "%s" % (self.end),
                "--vertical-label=%s" % (self.verticalLabel),
                "--watermark=[%s] / %s / %s" % (self.pk, self.watermark, self.generationDate.strftime("%Y.%m.%d %H:%M")),
                "--width", "%s" % (self.width),
                "--upper-limit", "%s" % (self.upperLimit),
                "--lower-limit", "%s" % (self.lowerLimit), lowerLimitRigid,
                "--slope-mode",
                "DEF:%s=%s:%s:AVERAGE" % (definitionOne, ''.join([settings.MEDIA_ROOT, '/..' ,self.rrdFilename.url]), definitionOne),
                "DEF:%s=%s:%s:AVERAGE:end=now-%s:start=end-%s" % (definitionOneShift, ''.join([settings.MEDIA_ROOT, '/..' ,self.rrdFilename.url]), definitionOne, self.timePeriod, self.timePeriod),
                "AREA:%s%s" % (definitionOne, self.areaColor) ,
                "LINE2:%s%s:%s" % (definitionOne, self.lineColor, self.get_unit_display()) ,
                "GPRINT:{0}:MIN:Min\: %2.2lf{1}".format(definitionOne, self.unit) ,
                "GPRINT:{0}:AVERAGE:Average\: %2.2lf{1}".format(definitionOne, self.unit) ,
                "GPRINT:{0}:MAX:Max\: %2.2lf{1}".format(definitionOne, self.unit) ,
                "GPRINT:{0}:LAST:Current\: %2.2lf{1}\\r".format(definitionOne, self.unit) ,
                "SHIFT:{0}:{1}".format(definitionOneShift, self.timePeriod),
                "LINE1:{0}#00000066:{1} comparison:dashes".format(definitionOneShift, self.get_unit_display()),
                "GPRINT:{0}:MIN:Min\: %2.2lf{1}".format(definitionOneShift, self.unit),
                "GPRINT:{0}:AVERAGE:Average\: %2.2lf{1}".format(definitionOneShift, self.unit),
                "GPRINT:{0}:MAX:Max\: %2.2lf{1}".format(definitionOneShift, self.unit),
                "GPRINT:{0}:LAST:Current\: %2.2lf{1}\\r".format(definitionOneShift, self.unit)),

            self.save()
        except:
            logger.error('TRY FETCH ERROR')
            pass

        logger.info('END')

    def fetchRRD(self, resolution, start, end, datasourceToFetch):
        logger.info('BEGIN -> resolution: %s, start: %s, end: %s, datasourceToFetch: %s' % (resolution, start, end, datasourceToFetch))
        # rrdtool fetch AM2302.rrd AVERAGE -r 60 -e now-5minutes -s e-1day
        rrdtoolFetch = rrdtool.fetch(''.join([settings.MEDIA_ROOT, '/../' ,self.rrdFilename.url]), 'AVERAGE', '-r 60', '-e now', '-s e-1d')

        #logger.info('rrdtoolFetch -> %s, %s ,%s' % (rrdtoolFetch[0], rrdtoolFetch[1], rrdtoolFetch[2]))
        logger.info('rrdtoolFetch -> %s, %s' % (rrdtoolFetch[0], rrdtoolFetch[1]))

        datasources =  rrdtoolFetch[1]
        i = 0
        datasourceMatch = 9999

        for datasource in datasources:
            # logger.debug('i: %s' % i)
            # logger.debug('datasourceMatch: %s' % datasourceMatch)
            # logger.debug('datasource: %s' % datasource)
            # logger.debug('datasourceToFetch: %s' % datasourceToFetch)
            if datasource == datasourceToFetch:
                datasourceMatch = i
            else:
                i += 1

        valueList = []
        for value in rrdtoolFetch[2]:
            # logger.debug('value: %s' % value[datasourceMatch])
            if value[datasourceMatch] is not None:
                valueList.append(float(value[datasourceMatch]))

        minValue = min(valueList)
        maxValue = max(valueList)
        averageValue = sum(valueList) / float(len(valueList))

        returnValues = []
        returnValues.append(rrdtoolFetch[2])
        returnValues.append(minValue)
        returnValues.append(maxValue)
        returnValues.append(averageValue)

        logger.info('END -> minValue: %s, averageValue: %s, maxValue: %s' % (minValue, averageValue, maxValue))

        return returnValues
