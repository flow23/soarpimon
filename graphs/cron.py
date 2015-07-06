# -*- coding: utf-8 -*-

import datetime, logging
from django.core.mail import EmailMessage
from .models import Graph
from solar import settings

logger = logging.getLogger(__name__)
cronjobLogger = logging.getLogger('cronjob')

# def sendWeatherGraphs():
#     email = EmailMessage('Hello', 'Body goes here', 'fwallburg@gmail.com',
#     ['florian.wallburg@web.de'],
#     #, 'mischa.nistl@web.de'],
#     # BCC ['mischa.nistl@web.de'],
#     reply_to=['florian.wallburg@web.de'], headers={'Message-ID': 'SOLARPIMON graphs'})
#
#     for singleGraph in Graph.weatherObjects.order_by('category', 'unit', 'timePeriod'):
#         email.attach_file(''.join([settings.MEDIA_ROOT, '/..' , singleGraph.imageFilename.url]))
#
#     email.send(fail_silently=False)

def sendDailyStatus():
    cronjobLogger.info('BEGIN')

    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(1)
    date = yesterday.strftime("%Y-%m-%d")
    debug = ''

    # Get all rrds in graph lists
    rrdList = []
    #for singleGraph in Graph.weatherObjects.order_by('rrdFilename'):
    for singleGraph in Graph.weatherObjects.order_by('rrdFilename'):
        rrdList.append(singleGraph.rrdFilename.url)

    cronjobLogger.debug('Used rrd -> %s' % singleGraph.rrdFilename.url)
    temperature = singleGraph.fetchRRD('60','start','end', 'temperature')
    humidity = singleGraph.fetchRRD('60','start','end', 'humidity')

    rrdList = sorted(set(rrdList))

    # for abc in rrdList:
    #     logger.debug('sgraph: %s' % abc)

    email = EmailMessage('[SOLARPIMON] Daily status from %s' % (date),
        'Temperature\nMin: %.1f°C\nAverage: %.1f°C\nMax: %.1f°C\n\nHumidity\nMin: %.0f%%\nAverage: %.0f%%\nMax: %.0f%%\n\nDEBUG\nrrdList -> %s\ndebug -> %s'
        % (temperature[1],temperature[3],temperature[2],humidity[1],humidity[3],humidity[2],rrdList,'free'), 'fwallburg@gmail.com',
    ['florian.wallburg@web.de'],
    #, 'mischa.nistl@web.de'],
    # BCC ['mischa.nistl@web.de'],
    reply_to=['florian.wallburg@web.de'], headers={'Message-ID': 'SOLARPIMON graphs'})

    for singleGraph in Graph.weatherObjects.order_by('category', 'unit', 'timePeriod'):
        singleGraph.generateComparisonGraph()
        cronjobLogger.debug('Graph added to mail -> %s' % singleGraph.imageFilename.url)
        email.attach_file(''.join([settings.MEDIA_ROOT, '/..' , singleGraph.imageFilename.url]))

    email.send(fail_silently=False)

    logger.error('TEST')

    cronjobLogger.info('END')
