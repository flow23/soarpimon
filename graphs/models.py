import rrdtool, os

from django.db import models
from django.utils import timezone
from solar import settings

class SolarGraphManager(models.Manager):
    def get_queryset(self):
        return super(SolarGraphManager, self).get_queryset().filter(category='solar')

class BatteryGraphManager(models.Manager):
    def get_queryset(self):
        return super(BatteryGraphManager, self).get_queryset().filter(category='battery')

class Graph(models.Model):
    CATEGORIES = (
        ('solar', 'Solar'),
        ('battery', 'Battery'),
        ('wattage', 'Wattage'),
    )
    category = models.CharField(max_length=7, choices=CATEGORIES)

    description = models.CharField(max_length=100,default='description')

    rrdFilename = models.FileField(upload_to='rrd/', blank=True)
    imageFilename = models.ImageField(upload_to='graph/', blank=True)

    TIMEPERIODS = (
        ('3600', '1hour'),
        ('43200', '12hours'),
        ('86400', '1day'),
        ('604800', '1week'),
        ('2419200', '1month'),
        ('14515200', '6months'),
        ('29030400', '1year'),
    )
    timePeriod = models.IntegerField(choices=TIMEPERIODS, default=3600)
    start = models.CharField(max_length=50,default='end-3600')
    end = models.CharField(max_length=50,default='now')

    UNITS = (
        ('A', 'Ampere'),
        ('V', 'Volt'),
        ('W', 'Wattage'),
    )
    unit = models.CharField(max_length=3, choices=UNITS, default='A')

    verticalLabel = models.CharField(max_length=50,default='verticalLabel')
    watermark = models.CharField(max_length=50,default='watermark')
    width = models.IntegerField(default='640')
    height = models.IntegerField(default='180')
    upperLimit = models.IntegerField()
    lowerLimit = models.IntegerField(default='0')
    lowerLimitRigid = models.BooleanField(default='true')

    lastChange = models.DateTimeField('last change', auto_now=True)
    generationDate = models.DateTimeField('date generated', default=timezone.now)

    # Manager stuff
    objects = models.Manager()
    batteryObjects = BatteryGraphManager()
    solarObjects = SolarGraphManager()

    # defs
    #def categories(self):
    #    category = self.order_by('category').distrinct.values_list('caategory', flat=True)
    #    lists = []
    #    for c in category:
    #        if c[0] == 

    def generateComparisonGraph(self):
        #graphDestinationFilename = ''.os.path.join([settings.MEDIA_ROOT, '/..' , self.imageFilename.url])
        #import pdb; pdb.set_trace()
        #abnc = settings.MEDIA_ROOT

        if (self.category == 'solar'):
            definitionOne = 'ampere'
            definitionOneShift= 'ampereShift'
        elif (self.category == 'battery'):
            definitionOne = 'volt'
            definitionOneShift= 'voltShift'
        else:
            definitionOne = 'solar'
            definitionOneShift= 'solarShift'

        if (self.lowerLimitRigid == True):
            lowerLimitRigid = '--rigid'
        else:
            lowerLimitRigid = ''

        ret = rrdtool.graph(''.join([settings.MEDIA_ROOT, '/..' ,self.imageFilename.url]),
        #ret = rrdtool.graph(graphDestinationFilename,
            "--start", "end-%s" % (self.timePeriod),
            "--end", "%s" % (self.end),
            #"--vertical-label=%s" % (self.verticalLabel),
            "--watermark=%s" % (self.watermark),
            "--width", "%s" % (self.width),
            "--upper-limit", "%s" % (self.upperLimit),
            "--lower-limit", "%s" % (self.lowerLimit), lowerLimitRigid,
            "DEF:%s=%s:%s:AVERAGE" % (definitionOne, ''.join([settings.MEDIA_ROOT, '/..' ,self.rrdFilename.url]), definitionOne),
            "DEF:%s=%s:%s:AVERAGE:end=now-%s:start=end-%s" % (definitionOneShift, ''.join([settings.MEDIA_ROOT, '/..' ,self.rrdFilename.url]), definitionOne, self.timePeriod, self.timePeriod),
            "AREA:%s#00FF0066" % (definitionOne) ,
            "LINE2:%s#00990066:%s" % (definitionOne, self.get_unit_display()) ,
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

        self.generationDate = timezone.now()
        self.save()

        return self
