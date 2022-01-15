from bdc import calcBDC
from utils import get_incline_compensation
from utils import get_cant_compensation
from utils import fpsToMps
from utils import inchToCm
from rich.console import Console
from rich.table import Table
import math
import argparse
import configparser
import os.path

import sys, logging

#logLevel=logging.DEBUG
#logLevel=logging.INFO
#logLevel=logging.WARNING

# If logLevel is unset, we will only display the most serious messages.
try:
    logLevel
except NameError:
    logLevel=logging.CRITICAL
finally:
    logging.basicConfig(format='%(levelname)s : %(filename)s : %(funcName)s : %(lineno)4d : %(message)s', level=logLevel, handlers=[logging.StreamHandler(sys.stdout)])

logging.debug('Example Debug Message')
logging.info('Example Info Message')
logging.warning('Example Warning Message')

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--conffile', type=str, dest='myconffile')
parser.add_argument('-s', '--sharedconf', type=str, dest='sharedconf')
args = parser.parse_args()

if args.sharedconf is not None and os.path.exists(args.sharedconf):
    config = configparser.RawConfigParser()
    config.read(args.sharedconf)
    buildconf = dict(config.items('Common'))
else:
    buildconf = {}

if args.myconffile is not None and os.path.exists(args.myconffile):
    config = configparser.RawConfigParser()
    config.read(args.myconffile)
    buildconf = {**buildconf, **dict(config.items('Base'))}
else:
    if buildconf is not None:
        buildconf = {}

#print(buildconf)
#quit()

if 'ammunition name' not in buildconf:
    buildconf['ammunition name'] = "Configuration"

if 'range max' in buildconf:
    buildconf['range max'] = int(buildconf['range max'])
else:
    buildconf['range max'] = 600

if 'ballistic coefficient' in buildconf:
    buildconf['ballistic coefficient'] = float(buildconf['ballistic coefficient'])
else:
    buildconf['ballistic coefficient'] = 0.269

if 'velocity - muzzle' in buildconf:
    buildconf['velocity - muzzle'] = int(buildconf['velocity - muzzle'])
else:
    buildconf['velocity - muzzle'] = 3165

if 'sight height' in buildconf:
    buildconf['sight height'] = float(buildconf['sight height'])
else:
    buildconf['sight height'] = 1.5

if 'angle - shooting' in buildconf:
    buildconf['angle - shooting'] = int(buildconf['angle - shooting'])
else:
    buildconf['angle - shooting'] = 0

if 'angle - bore' in buildconf:
    if buildconf['angle - bore'].lower() == 'none':
        buildconf['angle - bore'] = None
#    print(type(buildconf['angle - bore']))
#    print("angle - bore: %s" % buildconf['angle - bore'])
    if buildconf['angle - bore'] is not None:
        if buildconf['angle - bore'].replace('.','',1).isdigit():
            buildconf['angle - bore'] = float(buildconf['angle - bore'])
#        print(type(buildconf['angle - bore']))
        if not isinstance(buildconf['angle - bore'], float):
            print("Configuration file error:  angle bore is neither None or Number (floating point)")
            exit()
else:
    buildconf['angle - bore'] = None

if 'zero - distance' in buildconf:
    buildconf['zero - distance'] = int(buildconf['zero - distance'])
else:
    buildconf['zero - distance'] = 50

if 'zero - unit' in buildconf:
    buildconf['zero - unit'] = buildconf['zero - unit'].lower()
else:
    buildconf['zero - unit'] = 'y'

if 'drag function' in buildconf:
    buildconf['drag function'] = buildconf['drag function'].upper()
else:
    buildconf['drag function'] = 'G1'

if 'altitude' in buildconf:
    buildconf['altitude'] = int(buildconf['altitude'])

if 'barometer' in buildconf:
    buildconf['barometer'] = float(buildconf['barometer'])

if 'temperature' in buildconf:
    buildconf['temperature'] = float(buildconf['temperature'])

if 'humidity - relative' in buildconf:
    buildconf['humidity - relative'] = float(buildconf['humidity - relative'])

if 'wind - speed' in buildconf:
    buildconf['wind - speed'] = float(buildconf['wind - speed'])
else:
    buildconf['wind - speed'] = 10

if 'wind - angle' in buildconf:
    buildconf['wind - angle'] = int(buildconf['wind - angle'])
else:
    buildconf['wind - angle'] = 90




if args.myconffile is not None and os.path.exists(args.myconffile):
    config = configparser.RawConfigParser()
#    config.read('./ConfigurationFiles/22lr-CCI-Standard-Velocity.cfg')
    config.read(args.myconffile)
    displayconf = dict(config.items('Display'))
else:
    displayconf = {}

if 'rangetype' in displayconf:
    displayconf['rangetype'] = displayconf['rangetype'].lower()
else:
    displayconf['rangetype'] = 'yards'

if 'interval' in displayconf:
    displayconf['interval'] = int(displayconf['interval'])
else:
    displayconf['interval'] = 50

#configuration, hold_overs = calcBDC()
configuration, hold_overs = calcBDC(buildconf)

console = Console()

## Print Configuration Table
#conftable = Table(title="Configuration")
#conftable.add_column("Key", justify="left", no_wrap=True)
#conftable.add_column("Value", justify="left", no_wrap=True)
#for item in sorted(configuration):
#    conftable.add_row(item, str(configuration[item]))
#
#console.print(conftable)
#print()
#
#alltable = Table(title="All Points in hold_overs")
#alltable.add_column("Yards", justify="right", no_wrap=True)
#alltable.add_column("Meters", justify="right", no_wrap=True)
#alltable.add_column("Elevation - Inches", justify="right", no_wrap=True)
#alltable.add_column("Incline Compensation", justify="right", no_wrap=True)
#alltable.add_column("Inches-Incline", justify="right", no_wrap=True)
#alltable.add_column("Cant Compensation", justify="right", no_wrap=True)
#for point in hold_overs.points:
#    incline_compensation = get_incline_compensation(point.path_inches, -15)
#
#    cant_compensation = get_cant_compensation(point.seconds, 90, 1.5)
#
#    alltable.add_row (point.yards, point.meters, str(point.path_inches), str(incline_compensation), str(abs(point.path_inches-incline_compensation)), str(cant_compensation))
#
#console.print(alltable)
#print()

console.print()

# Print Configuration Table
if buildconf['ammunition name'] != "Configuration":
    conftable = Table(title = buildconf['ammunition name'])
else:
    conftable = Table(title = "Configuration")
conftable.add_column("Key", justify="left", no_wrap=True)
conftable.add_column("Value", justify="left", no_wrap=True)
for item in sorted(configuration):
    conftable.add_row(item, str(configuration[item]))

console.print(conftable)
console.print()


if displayconf['rangetype'] == 'both':
    if buildconf['ammunition name'] != "Configuration":
        tablename = buildconf['ammunition name']
    else:
        tablename = "Both Whole Meters and Yards"
    combinedtable = Table(title = tablename)
if displayconf['rangetype'] == 'yards':
    if buildconf['ammunition name'] != "Configuration":
        tablename = buildconf['ammunition name']
    else:
        tablename = "Whole Yards Only"
    combinedtable = Table(title = tablename)
elif displayconf['rangetype'] == 'meters':
    if buildconf['ammunition name'] != "Configuration":
        tablename = buildconf['ammunition name']
    else:
        tablename = "Whole Meters Only"
    combinedtable = Table(title = tablename)

if displayconf['rangetype'] in ['both', 'yards']:
    combinedtable.add_column("Yards", justify="right", no_wrap=True)
if displayconf['rangetype'] in ['both', 'meters']:
    combinedtable.add_column("Meters", justify="right", no_wrap=True)

combinedtable.add_column("Drop - In.", justify="right", no_wrap=True)
combinedtable.add_column("Drop - Cm.", justify="right", no_wrap=True)
combinedtable.add_column("Drop - MOA", justify="right", no_wrap=True)
combinedtable.add_column("Drop - Mil", justify="right", no_wrap=True)
combinedtable.add_column("Drift - In.", justify="right", no_wrap=True)
combinedtable.add_column("Drift - Cm.", justify="right", no_wrap=True)
combinedtable.add_column("Drift - MOA", justify="right", no_wrap=True)
combinedtable.add_column("Drift - Mil", justify="right", no_wrap=True)
combinedtable.add_column("Time", justify="right", no_wrap=True)
combinedtable.add_column("Velocity - fps", justify="right", no_wrap=True)
combinedtable.add_column("Velocity - mps", justify="right", no_wrap=True)
combinedtable.add_column("Kinetic Energy", justify="right", no_wrap=True)


for point in hold_overs.points:
    if (displayconf['rangetype'] == 'yards' and float(point.yards).is_integer()) or \
       (displayconf['rangetype'] == 'meters' and float(point.meters).is_integer()) or \
       (displayconf['rangetype'] == 'both' and (float(point.yards).is_integer() or \
                                 float(point.meters).is_integer())):
        if ((float(point.yards) / displayconf['interval']).is_integer() or \
            (float(point.meters) / displayconf['interval']).is_integer()):
            fieldlist = list()
            if displayconf['rangetype'] in ['both', 'yards']:
                fieldlist.append(point.yards)
            if displayconf['rangetype'] in ['both', 'meters']:
                fieldlist.append(point.meters)
            # Consider reducing this to two decimal places as there is a minor
            # difference exposed when using three decimal places and specifying
            # a fixed bore (zero) angle
            pi = '{:.3f}'.format(round(point.path_inches, 3))
#            pi = '{:.2f}'.format(round(point.path_inches, 3))
            fieldlist.append(pi)
            pc = '{:.3f}'.format(round(inchToCm(point.path_inches), 3))
            fieldlist.append(pc)
            moac = '{:.2f}'.format(round(point.moa_correction, 2))
            fieldlist.append(moac)
            milc = '{:.2f}'.format(round(point.mil_correction, 2))
            fieldlist.append(milc)
            dinch = '{:.3f}'.format(round(point.drift_inches, 3))
            fieldlist.append(dinch)
            dcent = '{:.3f}'.format(round(inchToCm(point.drift_inches), 3))
            fieldlist.append(dcent)
            dmoa = '{:.2f}'.format(round(point.drift_moa, 2))
            fieldlist.append(dmoa)
            dmil = '{:.2f}'.format(round(point.drift_mil, 2))
            fieldlist.append(dmil)
            stime = '{:.3f}'.format(round(point.seconds, 3))
            fieldlist.append(stime)
            velf = '{:.2f}'.format(round(point.velocity, 2))
            fieldlist.append(velf)
            velm = '{:.2f}'.format(round(fpsToMps(point.velocity), 2))
            fieldlist.append(velm)
            ke = '{:.2f}'.format(round(point.kinetic_energy, 2))
            fieldlist.append(ke)
            combinedtable.add_row(*fieldlist)


console.print(combinedtable)

#for point in hold_overs.points:
#    if not float(point.yards).is_integer() and \
#       not float(point.meters).is_integer():
#        print("yards: %s  meters: %s" % point.yards, point.meters)
#    else:
#        print("nope")

#print()
#for point in hold_overs.points:
#    exec("print(point.%s)" % (tempdict["rangetype"]))
#print("end")
