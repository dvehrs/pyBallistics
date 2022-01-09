from bdc import calcBDC
from utils import get_incline_compensation
from utils import get_cant_compensation
from rich.console import Console
from rich.table import Table
import math

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

# Dictionary for Basic configuration Options
buildconf = {}
buildconf['range max'] = 150
buildconf['ballistic coefficient'] = 0.120
buildconf['velocity - muzzle'] = 1070
buildconf['site height'] = 2
buildconf['angle - shooting'] = 0
buildconf['zero - distance'] = 50
buildconf['zero - units'] = 'y'
buildconf['drag function'] = 'G1'

#hold_overs = calcBDC(400)
#configuration, hold_overs = calcBDC(range_max = 400, zero_unit = "m")
#hold_overs = calcBDC(zero_unit = "m", range = 400)
#configuration, hold_overs = calcBDC(range_max = 100)
#configuration, hold_overs = calcBDC(range_max = 200)
#configuration, hold_overs = calcBDC(range_max = 300, zero_dist = 50)
#configuration, hold_overs = calcBDC(range_max = 300, zero_dist= 190)
#configuration, hold_overs = calcBDC(range_max = 200, zero_dist = 50, v = 1050, bc = 0.120)
#configuration, hold_overs = calcBDC(range_max = 200, zero_dist = 50, bc = 0.120)
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
#
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
#yardstable = Table(title="Whole Yards Only")
#yardstable.add_column("Yards", justify="right", no_wrap=True)
#yardstable.add_column("Drop - Inches", justify="right", no_wrap=True)
#yardstable.add_column("Drop - MOA", justify="right", no_wrap=True)
#yardstable.add_column("Drop - Mils", justify="right", no_wrap=True)
#yardstable.add_column("Time", justify="right", no_wrap=True)
#yardstable.add_column("Velocity", justify="right", no_wrap=True)
#for point in hold_overs.points:
#    if float(point.yards).is_integer():
#        pi = '{:.3f}'.format(round(point.path_inches, 3))
#        moac = '{:.2f}'.format(round(point.moa_correction, 2))
#        milc = '{:.2f}'.format(round(point.mil_correction, 2))
#        stime = '{:.3f}'.format(round(point.seconds, 3))
#        vel = '{:.2f}'.format(round(point.velocity, 2))
#        yardstable.add_row(point.yards, pi, moac, milc, stime, vel)
#
#console.print(yardstable)
#print()
#
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
#meterstable = Table(title="Whole Meters Only")
#meterstable.add_column("Meters", justify="right", no_wrap=True)
#meterstable.add_column("Drop - Inches", justify="right", no_wrap=True)
#meterstable.add_column("Drop - MOA", justify="right", no_wrap=True)
#meterstable.add_column("Drop - Mils", justify="right", no_wrap=True)
#meterstable.add_column("Time", justify="right", no_wrap=True)
#meterstable.add_column("Velocity", justify="right", no_wrap=True)
#for point in hold_overs.points:
#    if float(point.meters).is_integer():
#        if (float(point.meters) / 5).is_integer():
#            pi = '{:.3f}'.format(round(point.path_inches, 3))
#            moac = '{:.2f}'.format(round(point.moa_correction, 2))
#            milc = '{:.2f}'.format(round(point.mil_correction, 2))
#            stime = '{:.3f}'.format(round(point.seconds, 3))
#            vel = '{:.2f}'.format(round(point.velocity, 2))
#            meterstable.add_row(point.meters, pi, moac, milc, stime, vel)
#
#console.print(meterstable)

print()
print()
print()
print()
print("locals test")
print()

# Print Configuration Table
conftable = Table(title="Configuration")
conftable.add_column("Key", justify="left", no_wrap=True)
conftable.add_column("Value", justify="left", no_wrap=True)
for item in sorted(configuration):
    conftable.add_row(item, str(configuration[item]))

console.print(conftable)
print()

rangetype =  'yards'
#rangetype = 'meters'
#rangetype = 'both'

interval = 5


if rangetype == 'both':
    combinedtable = Table(title="Both Whole Meters and Yards")
if rangetype == 'yards':
    combinedtable = Table(title="Whole Yards Only")
elif rangetype == 'meters':
    combinedtable = Table(title="Whole Meters Only")

if rangetype in ['both', 'yards']:
    combinedtable.add_column("Yards", justify="right", no_wrap=True)
if rangetype in ['both', 'meters']:
    combinedtable.add_column("Meters", justify="right", no_wrap=True)

combinedtable.add_column("Drop - Inches", justify="right", no_wrap=True)
combinedtable.add_column("Drop - MOA", justify="right", no_wrap=True)
combinedtable.add_column("Drop - Mils", justify="right", no_wrap=True)
combinedtable.add_column("Time", justify="right", no_wrap=True)
combinedtable.add_column("Velocity", justify="right", no_wrap=True)


for point in hold_overs.points:
    if (rangetype == 'yards' and float(point.yards).is_integer()) or \
       (rangetype == 'meters' and float(point.meters).is_integer()) or \
       (rangetype == 'both' and (float(point.yards).is_integer() or \
                                 float(point.meters).is_integer())):
        if ((float(point.yards) / interval).is_integer() or \
            (float(point.meters) / interval).is_integer()):
            fieldlist = list()
            if rangetype in ['both', 'yards']:
                fieldlist.append(point.yards)
            if rangetype in ['both', 'meters']:
                fieldlist.append(point.meters)
            pi = '{:.3f}'.format(round(point.path_inches, 3))
            fieldlist.append(pi)
            moac = '{:.2f}'.format(round(point.moa_correction, 2))
            fieldlist.append(moac)
            milc = '{:.2f}'.format(round(point.mil_correction, 2))
            fieldlist.append(milc)
            stime = '{:.3f}'.format(round(point.seconds, 3))
            fieldlist.append(stime)
            vel = '{:.2f}'.format(round(point.velocity, 2))
            fieldlist.append(vel)
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
