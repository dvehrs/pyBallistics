import atmosphere
import angles
import ballistics
import constants
import logging


def calcBDC(buildconf = {}):
#def calcBDC(range_max = constants.BALLISTICS_COMPUTATION_MAX_YARDS, bc = 0.269, v = 3165, sh = 1.5, angle = 0,
#            zero_dist = 50, zero_unit = 'y', drag_function = "G1"):

    logger = logging.getLogger()

    # Test for configuration items in buildconf, and set to default if not found
    if 'range max' in buildconf:
        range_max = buildconf['range max']
    else:
        range_max = constants.BALLISTICS_COMPUTATION_MAX_YARDS

    if 'ballistic coefficient' in buildconf:
        bc = buildconf['ballistic coefficient']
    else:
        bc = 0.269

    if 'velocity - muzzle' in buildconf:
        v = buildconf['velocity - muzzle']
    else:
        v = 3165

    if 'sight height' in buildconf:
        sh  = buildconf['sight height']
    else:
        sh = 1.5

    if 'angle - shooting' in buildconf:
        angle = buildconf['angle - shooting']
    else:
        angle = 0

    if 'angle - bore' in buildconf:
        zeroangle = buildconf['angle - bore']
    else:
        zeroangle = None

    if 'zero - distance' in buildconf:
        zero_dist = buildconf['zero - distance']
    else:
        zero_dist = 50

    if 'zero - unit' in buildconf:
        zero_unit = buildconf['zero - unit']
    else:
        zero_unit = 'y'

    if 'drag function' in buildconf:
        drag_function = buildconf['drag function']
    else:
        drag_function = 'G1'

    if 'altitude' in buildconf:
        altitude = buildconf['altitude']
    else:
        altitude = 0

    if 'barometer' in buildconf:
        barometer = buildconf['barometer']
    else:
        barometer = 29.59

    if 'temperature' in buildconf:
        temperature = buildconf['temperature']
    else:
        temperature = 59

    if 'humidity - relative' in buildconf:
        relative_humidity = buildconf['humidity - relative']
    else:
        relative_humidity = 0.7

    if 'wind - speed' in buildconf:
        windspeed = buildconf['wind - speed']
    else:
        windspeed = 0

    if 'wind - angle' in buildconf:
        windangle = buildconf['wind - angle']
    else:
        windangle = 0

    # Declare empty dictionary to hold configuration settings
    configuration = {}

    configuration['range max'] = range_max
    configuration['ballistic coefficint - input'] = bc
    configuration['velocity'] = v
    configuration['zero: sight height'] = str(sh)+" inches"
    configuration['angle - shooting'] = angle
    if zeroangle is None:
        if zero_unit.lower() == 'm':
            configuration['zero: distance (configured)'] = str(zero_dist)+" meters"
        else:
            configuration['zero: distance (configured)'] = str(zero_dist)+" yards"
    configuration['local: altitude'] = altitude
    configuration['local: temperature'] = temperature
    configuration['local: barometer'] = barometer
    configuration['local: relative humidity'] = relative_humidity
    configuration['local: wind speed'] = windspeed
    configuration['local: wind angle'] = windangle

    k = 0
    # The wind speed in miles per hour.
#    windspeed = 0
#    # The wind angle (0=headwind, 90=right to left, 180=tailwind, 270/-90=left to right)
#    windangle = 0

#    altitude = 6000
##    altitude = 0
#    barometer = 29.59
#    temperature = 59
#    relative_humidity = 0.7

    # If we wish to use the weather correction features, we need to
    # Correct the BC for any weather conditions.  If we want standard conditions,
    # then we can just leave this commented out.

    bc = atmosphere.atmosphere_correction(
        bc, altitude, barometer, temperature, relative_humidity)

    logger.info("bc {}".format(bc))
    # print("bc {}".format(bc))

    configuration['ballistic coefficint - corrected'] = bc

    # Convert zero range in meters to yards for calculating the zero angle
    if zero_unit.lower() == 'm':
#        zero_dist = zero_dist*1.093613
        zero_dist = zero_dist*((100/2.54)/36)

    # First find the angle of the bore relative to the sighting system.
    # We call this the "zero angle", since it is the angle required to
    # achieve a zero at a particular yardage.  This value isn't very useful
    # to us, but is required for making a full ballistic solution.
    # It is left here to allow for zero-ing at altitudes (bc) different from the
    # final solution, or to allow for zero's other than 0" (ex: 3" high at 100 yds)
    #
    # Note: Added test for zeroangle being None to allow the user to specify a
    # given zero angle for the bore to be able to compare cartridges with
    # different bc or velocities.
    if zeroangle is None:
        zeroangle = angles.zero_angle(drag_function, bc, v, sh, zero_dist, 0)
        configuration['zero: bore to sight angle (calculated)'] = zeroangle
    else:
        configuration['zero: bore to sight angle (configured)'] = zeroangle


    # Now we have everything needed to generate a full solution.
    # So we do.  The solution is stored in the pointer "sln" passed as the last argument.
    # k has the number of yards the solution is valid for, also the number of rows in the solution.
    hold_overs = ballistics.solve(range_max, drag_function, bc, v, sh, angle,
                                  zeroangle, windspeed, windangle)

    # Get near and far zeros.
    zero1 = None
    zero2 = None
    testdir = "up"
    testnum = 1.0
    for point in hold_overs.points:
        if abs(point.path_inches) < testnum:
            testnum = point.path_inches
        if point.path_inches > 0 and testdir == "up":
            testdir = "down"
            if zero_unit.lower() == 'm':
                zero1 = round(float(point.meters))
            else:
                zero1 = round(float(point.yards))
            testnum = 1.0
        if point.path_inches < 0 and testdir == "down":
            if zero_unit.lower() == 'm':
                zero2 = round(float(point.meters))
            else:
                zero2 = round(float(point.yards))
            break

    if zero1 is not None:
        if zero_unit.lower() == 'm':
            configuration['zero: 1st (near) approximate'] = str(zero1) + " meters"
        else:
            configuration['zero: 1st (near) approximate'] = str(zero1) + " yards"

    if zero2 is not None:
        if zero_unit.lower() == 'm':
            configuration['zero: 2nd (far) approximate'] = str(zero2) + " meters"
        else:
            configuration['zero: 2nd (far) approximate'] = str(zero2) + " yards"





    return configuration, hold_overs
