from bdc import calcBDC
from utils import *
#from utils import inhg_to_mmhg
#from utils import mmhg_to_inhg
#from utils import inhg_to_mbar
#from utils import mbar_to_inhg

import math

import sys, logging

#logLevel=logging.DEBUG
logLevel=logging.INFO
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

print()
print("Conversion Tests for Barometric Pressure")
print()
print("Starting with 29.92 inHG (inches of Mercury)")
print("  - Converting to mmHg (millimeters of Mercury)")

converted = inhg_to_mmhg(29.92)
print("       equal to %s mmHg" % (converted))

print("  - Converting back to inHg (inches of Mercury)")

back = mmhg_to_inhg(converted)
print("       equal to %s inHg" % (back))

print()
print("Starting with 29.92 inHg (inches of Mercury)")
print("  - Converting to mbar (millibar)")
converted = inhg_to_mbar(29.92)
print("       equal to %s mbar" % (converted))

print("  - Converting back to inHg (inches of Mercury)")

back = mbar_to_inhg(converted)
print("       equal to %s inHg" % (back))

print()
print("Starting with 1013 mbar")
print("  - Converting to millimeters of mercury (mmHg)")
converted = mbar_to_mmhg(1013)
print("    equal to %s mmHg" % (converted))
print("  - Converting to inches of mercury (inHg)")
converted = mmhg_to_inhg(converted)
print("    equal to %s inHg" % (converted))
print("  - Converting back to mbar")
back = inhg_to_mbar(converted)
print("    equal to %s mbar" % (back))
