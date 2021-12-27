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

#hold_overs = calcBDC(400)
#hold_overs = calcBDC(range = 400, zero_unit = "m")
#hold_overs = calcBDC(zero_unit = "m", range = 400)
hold_overs = calcBDC()

#print()
#print("All Points in hold_overs:")
#for point in hold_overs.points:
#    incline_compensation = get_incline_compensation(point.path_inches, -15)
#
#    cant_compensation = get_cant_compensation(point.seconds, 90, 1.5)
#
#    print("hold_over %8s %8s %s %s %s %s" %
#          (point.yards, point.meters, point.path_inches, incline_compensation, abs(point.path_inches-incline_compensation), cant_compensation))

#table = Table(title="All Points in hold_overs")
#table.add_column("Yards", justify="right", no_wrap=True)
#table.add_column("Meters", justify="right", no_wrap=True)
#table.add_column("Elevation - Inches", justify="right", no_wrap=True)
#table.add_column("Incline Compensation", justify="right", no_wrap=True)
#table.add_column("Inches-Incline", justify="right", no_wrap=True)
#table.add_column("Cant Compensation", justify="right", no_wrap=True)
#for point in hold_overs.points:
#    incline_compensation = get_incline_compensation(point.path_inches, -15)
#
#    cant_compensation = get_cant_compensation(point.seconds, 90, 1.5)
#
##    print("hold_over %8s %8s %s %s %s %s" %
##          (point.yards, point.meters, point.path_inches, incline_compensation, abs(point.path_inches-incline_compensation), cant_compensation))
#    table.add_row (point.yards, point.meters, point.path_inches, incline_compensation, abs(point.path_inches-incline_compensation), cant_compensation)


#print()
#print("Whole Yards Only")
#print("%-8s | %-8s  | %-8s | %-8s | %-9s | %-8s |" %
#      ("Range", "Drop", "MOA", "Mils", "Time", "Velocity"))
#print("%-8s | %-8s  | %-8s | %-8s | %-9s | %-8s |" %
#      ("(Yards)", "(Inches)", "", "", "(Seconds)", "(fps)"))
#for point in hold_overs.points:
#    if float(point.yards).is_integer():
#        pi = '{:.3f}'.format(round(point.path_inches, 3))
#        moac = '{:.2f}'.format(round(point.moa_correction, 2))
#        milc = '{:.2f}'.format(round(point.mil_correction, 2))
#        stime = '{:.3f}'.format(round(point.seconds, 3))
#        vel = '{:.2f}'.format(round(point.velocity, 2))
#        print("%8s | %8s  | %8s | %8s | %9s | %8s |" %
#              (point.yards, pi, moac, milc, stime, vel))
#
table = Table(title="Whole Yards Only")
table.add_column("Yards", justify="right", no_wrap=True)
table.add_column("Drop - Inches", justify="right", no_wrap=True)
table.add_column("Drop - MOA", justify="right", no_wrap=True)
table.add_column("Drop - Mils", justify="right", no_wrap=True)
table.add_column("Time", justify="right", no_wrap=True)
table.add_column("Velocity", justify="right", no_wrap=True)
for point in hold_overs.points:
    if float(point.yards).is_integer():
        pi = '{:.3f}'.format(round(point.path_inches, 3))
        moac = '{:.2f}'.format(round(point.moa_correction, 2))
        milc = '{:.2f}'.format(round(point.mil_correction, 2))
        stime = '{:.3f}'.format(round(point.seconds, 3))
        vel = '{:.2f}'.format(round(point.velocity, 2))
#        print("%8s | %8s  | %8s | %8s | %9s | %8s |" %
#              (point.yards, pi, moac, milc, stime, vel))
        table.add_row(point.yards, pi, moac, milc, stime, vel)

console = Console()
console.print(table)

#print()
#print("Whole Meters Only")
#print("%-8s | %-8s  | %-8s | %-8s | %-9s | %-8s |" %
#      ("Range", "Drop", "MOA", "Mils", "Time", "Velocity"))
#print("%-8s | %-8s  | %-8s | %-8s | %-9s | %-8s |" %
#      ("(Meters)", "(Inches)", "", "", "(Seconds)", "(fps)"))
#for point in hold_overs.points:
#    if float(point.meters).is_integer():
#        pi = '{:.3f}'.format(round(point.path_inches, 3))
#        moac = '{:.2f}'.format(round(point.moa_correction, 2))
#        milc = '{:.2f}'.format(round(point.mil_correction, 2))
#        stime = '{:.3f}'.format(round(point.seconds, 3))
#        vel = '{:.2f}'.format(round(point.velocity, 2))
#        print("%8s | %8s  | %8s | %8s | %9s | %8s |" %
#              (point.meters, pi, moac, milc, stime, vel))
