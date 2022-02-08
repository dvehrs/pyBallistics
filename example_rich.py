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

conffile = configparser.RawConfigParser()
if args.sharedconf is not None and os.path.exists(args.sharedconf):
    conffile.read(args.sharedconf)

if args.myconffile is not None and os.path.exists(args.myconffile):
    conffile.read(args.myconffile)

buildconf = {}

buildconf['ammunition name'] = conffile.get('Build', \
                                            'ammunition name', \
                                             fallback='Configuration')

buildconf['range max'] = conffile.getint('Build', 'range max', \
                                           fallback=600)

buildconf['ballistic coefficient'] = conffile.getfloat('Build', \
                                                  'ballistic coefficient', \
                                                   fallback=0.269)

buildconf['bullet weight'] = conffile.getfloat('Build', \
                                               'bullet weight', \
                                                fallback=40)

buildconf['velocity - muzzle'] = conffile.getint('Build', \
                                              'velocity - muzzle', \
                                               fallback=3165)

buildconf['sight height'] = conffile.getfloat('Build', 'sight height', \
                                           fallback=1.5)

buildconf['angle - shooting'] = conffile.getint('Build', 'angle - shooting', \
                                           fallback=0)

try:
    buildconf['angle - bore'] = conffile.getfloat('Build', 'angle - bore', \
                                                   fallback=None)
except:
    buildconf['angle - bore'] = conffile.get('Build', 'angle - bore')
    if buildconf['angle - bore'].lower() == 'none':
        buildconf['angle - bore'] = None
    else:
        print("Error in configuration file for 'angle - bore'")
        quit()

buildconf['zero - distance'] = conffile.getint('Build', 'zero - distance', \
                                           fallback=50)

buildconf['zero - unit'] = conffile.get('Build', 'zero - unit', \
                                         fallback='y')

buildconf['drag function'] = conffile.get('Build', 'drag function', \
                                           fallback='G1')

buildconf['altitude'] = conffile.getint('Build', 'altitude', \
                                         fallback=0)

buildconf['barometer'] = conffile.getfloat('Build', 'barometer', \
                                           fallback=29.92)

buildconf['temperature'] = conffile.getfloat('Build', 'temperature', \
                                         fallback=59.0)

buildconf['humidity - relative'] = conffile.getfloat('Build', \
                                                     'humidity - relative', \
                                                      fallback=0.5)

buildconf['wind - speed'] = conffile.getfloat('Build', 'wind - speed', \
                                               fallback=10)

buildconf['wind - angle'] = conffile.getint('Build', 'wind - angle', \
                                             fallback=90)

#print (buildconf)
#quit()
#
displayconf = {}

displayconf['rangetype'] = conffile.get('Display', 'rangetype', \
                                           fallback='yards')
displayconf['interval'] = conffile.getint('Display', 'interval', \
                                             fallback=25)
displayconf['Drop - Inches'] = conffile.getboolean('Display','Drop - Inches', \
                                                      fallback=True)
displayconf['Drop - Centimeters'] = conffile.getboolean('Display', \
                                                           'Drop - Centimeters', \
                                                            fallback=False)
displayconf['Drop - MOA'] = conffile.getboolean('Display','Drop - MOA', \
                                                    fallback=False)
displayconf['Drop - Mil'] = conffile.getboolean('Display','Drop - Mil', \
                                                    fallback=True)
displayconf['Drift - Inches'] = conffile.getboolean('Display', \
                                                       'Drift - Inches', \
                                                        fallback=True)
displayconf['Drift - Centimeters'] = conffile.getboolean('Display', \
                                                            'Drift - Centimeters', \
                                                             fallback=False)
displayconf['Drift - MOA'] = conffile.getboolean('Display', 'Drift - MOA', \
                                                      fallback=False)
displayconf['Drift - Mil'] = conffile.getboolean('Display', 'Drift - Mil', \
                                                      fallback=True)
displayconf['Time'] = conffile.getboolean('Display', 'Time', fallback=True)
displayconf['Velocity - fps'] = conffile.getboolean('Display', \
                                                       'Velocity - fps', \
                                                        fallback=True)
displayconf['Velocity - mps'] = conffile.getboolean('Display', \
                                                       'Velocity - mps', \
                                                        fallback=False)
displayconf['Kinetic Energy'] = conffile.getboolean('Display', \
                                                       'Kinetic Energy', \
                                                        fallback=True)


#configuration, hold_overs = calcBDC()
configuration, hold_overs = calcBDC(buildconf)

console = Console()

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


if displayconf['Drop - Inches']:
    combinedtable.add_column("Drop - In.", justify="right", no_wrap=True)
if displayconf['Drop - Centimeters']:
    combinedtable.add_column("Drop - Cm.", justify="right", no_wrap=True)
if displayconf['Drop - MOA']:
    combinedtable.add_column("Drop - MOA", justify="right", no_wrap=True)
if displayconf['Drop - Mil']:
    combinedtable.add_column("Drop - Mil", justify="right", no_wrap=True)
if displayconf['Drift - Inches']:
    combinedtable.add_column("Drift - In.", justify="right", no_wrap=True)
if displayconf['Drift - Centimeters']:
    combinedtable.add_column("Drift - Cm.", justify="right", no_wrap=True)
if displayconf['Drift - MOA']:
    combinedtable.add_column("Drift - MOA", justify="right", no_wrap=True)
if displayconf['Drift - Mil']:
    combinedtable.add_column("Drift - Mil", justify="right", no_wrap=True)
if displayconf['Time']:
    combinedtable.add_column("Time", justify="right", no_wrap=True)
if displayconf['Velocity - fps']:
    combinedtable.add_column("Velocity - fps", justify="right", no_wrap=True)
if displayconf['Velocity - mps']:
    combinedtable.add_column("Velocity - mps", justify="right", no_wrap=True)
if displayconf['Kinetic Energy']:
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
            # a fixed bore angle for zero
            pi = '{:.3f}'.format(round(point.path_inches, 3))
#            pi = '{:.2f}'.format(round(point.path_inches, 3))
            if displayconf['Drop - Inches']:
                fieldlist.append(pi)
            pc = '{:.3f}'.format(round(inchToCm(point.path_inches), 3))
            if displayconf['Drop - Centimeters']:
                fieldlist.append(pc)
            moac = '{:.2f}'.format(round(point.moa_correction, 2))
            if displayconf['Drop - MOA']:
                fieldlist.append(moac)
            milc = '{:.2f}'.format(round(point.mil_correction, 2))
            if displayconf['Drop - Mil']:
                fieldlist.append(milc)
            dinch = '{:.3f}'.format(round(point.drift_inches, 3))
            if displayconf['Drift - Inches']:
                fieldlist.append(dinch)
            dcent = '{:.3f}'.format(round(inchToCm(point.drift_inches), 3))
            if displayconf['Drift - Centimeters']:
                fieldlist.append(dcent)
            dmoa = '{:.2f}'.format(round(point.drift_moa, 2))
            if displayconf['Drift - MOA']:
                fieldlist.append(dmoa)
            dmil = '{:.2f}'.format(round(point.drift_mil, 2))
            if displayconf['Drift - Mil']:
                fieldlist.append(dmil)
            stime = '{:.3f}'.format(round(point.seconds, 3))
            if displayconf['Time']:
                fieldlist.append(stime)
            velf = '{:.2f}'.format(round(point.velocity, 2))
            if displayconf['Velocity - fps']:
                fieldlist.append(velf)
            velm = '{:.2f}'.format(round(fpsToMps(point.velocity), 2))
            if displayconf['Velocity - mps']:
                fieldlist.append(velm)
            ke = '{:.2f}'.format(round(point.kinetic_energy, 2))
            if displayconf['Kinetic Energy']:
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
