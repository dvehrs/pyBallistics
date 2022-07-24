import logging
import math
import atmosphere
import angles
import ballistics
import constants
import utils


def calcBDC(buildconf = {}):
#def calcBDC(range_max = constants.BALLISTICS_COMPUTATION_MAX_YARDS, bc = 0.269,
#            v = 3165, sh = 1.5, angle = 0,
#            zero_dist = 50, zero_unit = 'y', drag_function = "G1"):

    logger = logging.getLogger()

    # Test for configuration items in buildconf, and set to default if not found
    if 'range max' in buildconf:
        range_max = buildconf['range max']
    else:
        range_max = constants.BALLISTICS_COMPUTATION_MAX_YARDS

    if 'range - unit' in buildconf:
        range_unit = buildconf['range - unit']
    else:
        range_unit = 'yards'

    if 'ballistic coefficient' in buildconf:
        bc = buildconf['ballistic coefficient']
    else:
        bc = 0.269

    if 'bullet weight' in buildconf:
        bw = buildconf['bullet weight']
    else:
        bw = 40

    if 'bullet weight - unit' in buildconf:
        bweight_unit = buildconf['bullet weight - unit']
    else:
        bweight_unit = 'grains'

    if 'velocity - muzzle' in buildconf:
        v = buildconf['velocity - muzzle']
    else:
        v = 3165

    if 'velocity - unit' in buildconf:
        velocity_unit = buildconf['velocity - unit']
    else:
        velocity_unit = 'fps'

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

    if 'altitude - unit' in buildconf:
        altitude_unit = buildconf['altitude - unit']
    else:
        altitude_unit = 'feet'

    if 'barometer' in buildconf:
        barometer = buildconf['barometer']
    else:
        barometer = 29.59

    if 'temperature' in buildconf:
        temperature = buildconf['temperature']
    else:
        temperature = 59

    if 'temperature - unit' in buildconf:
        temperature_unit = buildconf['temperature - unit']
    else:
        temperature_unit = 'fahrenheit'

    if 'humidity - relative' in buildconf:
        relative_humidity = buildconf['humidity - relative']
    else:
        relative_humidity = 0.7

    if 'wind - speed' in buildconf:
        windspeed = buildconf['wind - speed']
    else:
        windspeed = 0

    if 'wind - unit' in buildconf:
        windspeed_unit = buildconf['wind - unit']
    else:
        windspeed_unit = 'mph'

    if 'wind - angle' in buildconf:
        windangle = buildconf['wind - angle']
    else:
        windangle = 0

    # Declare empty dictionary to hold configuration settings
    configuration = {}

    if range_unit == 'yards':
        configuration['range max'] = str(range_max) + ' yards / ' + \
                str(round(utils.yards_to_meters(range_max))) + ' meters'
    else:
        configuration['range max'] = \
                str(round(utils.meters_to_yards(range_max))) + ' yards / ' + \
                str(range_max) + ' meters'

    configuration['ballistic coefficient - configured'] = bc
    if velocity_unit == 'fps':
        configuration['muzzle velocity'] = str(v) + ' fps / ' + \
                str(round(utils.fps_to_mps(v))) + ' mps'
    else:
        configuration['muzzle velocity'] = str(round(utils.mps_to_fps(v))) + \
                ' fps / ' + str(v) + ' mps'
    if bweight_unit == "grains":
        configuration['bullet weight'] = str(bw) + " grains / " + \
                str(round(utils.grains_to_grams(bw), 2)) + ' grams'
    else:
        configuration['bullet weight'] = \
                str(round(utils.grams_to_grains(bw), 2)) + " grains / " + \
                str(bw) + ' grams'
    configuration['zero: sight height'] = str(sh)+" inches"
    configuration['angle - shooting'] = str(angle) + ' degrees'
    if zeroangle is None:
        if zero_unit.lower() == 'm':
            configuration['zero: distance (configured)'] = \
                    str(round(utils.meters_to_yards(zero_dist))) + ' yards / ' \
                    + str(zero_dist) + " meters"
        else:
            configuration['zero: distance (configured)'] = str(zero_dist) + \
                    ' yards / ' + str(round(utils.yards_to_meters(zero_dist))) \
                    + " meters"
    if temperature_unit == "fahrenheit":
        configuration['local: temperature'] = str(temperature) + ' F / ' + \
                      str(utils.degf_to_degc(temperature)) + ' C'
    else:
        configuration['local: temperature'] = str(utils.degc_to_degf(temperature)) + \
                      ' F / ' + str(temperature) + ' C'
    if altitude_unit == "feet":
        configuration['local: altitude'] = str(altitude) + ' feet / ' + \
                str(round(utils.feet_to_meters(altitude))) + ' meters'
    else:
        configuration['local: altitude'] = \
                str(round(utils.meters_to_feet(altitude))) + ' feet / ' + \
                str(altitude) + ' meters'
    configuration['local: barometer'] = str(barometer) + ' Hg'
    configuration['local: relative humidity'] = str(relative_humidity*100) + ' %'
    if windspeed_unit == "mph":
        configuration['local: wind speed'] = str(windspeed) + ' mph / ' + \
                str(round(utils.mph_to_kph(windspeed))) + ' kph'
    else:
        configuration['local: wind speed'] = \
                str(round(utils.kph_to_mph(windspeed))) + ' mph / ' + \
                str(windspeed) + ' kph'
    configuration['local: wind angle'] = str(windangle) + ' degrees'

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

    # Convert altitude in meters to feet for calculations.
    if altitude_unit == 'meters':
        altitude = utils.meters_to_feet(altitude)

    # Convert temperature in celcius to fahrenheit for calculations.
    if temperature_unit == 'celcius':
        temperature = utils.degc_to_degf(temperature)

    # If we wish to use the weather correction features, we need to
    # Correct the BC for any weather conditions.  If we want standard conditions,
    # then we can just leave this commented out.

    bc = atmosphere.atmosphere_correction(
        bc, altitude, barometer, temperature, relative_humidity)

    logger.info("bc {}".format(bc))
    # print("bc {}".format(bc))

    configuration['ballistic coefficient - corrected'] = "{:.3f}".format(bc)

    # Convert zero range in meters to yards for calculating the zero angle
    if zero_unit.lower() == 'm':
#        zero_dist = zero_dist*1.093613
#        zero_dist = zero_dist*((100/2.54)/36)
        zero_dist = utils.meters_to_yards(zero_dist)

    # Convert wind speed in kph to mph for calculations.
    if windspeed_unit == 'kph':
        windspeed = utils.kph_to_mph(windspeed)

    # Convert bullet weight in grams to grains for calculations.
    if bweight_unit == 'grams':
        bw = utils.grams_to_grains(bw)

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
        configuration['zero: bore to sight angle (calculated)'] = "{:.6f}".format(zeroangle)
    else:
        configuration['zero: bore to sight angle (configured)'] = zeroangle


    # Now we have everything needed to generate a full solution.
    # So we do.  The solution is stored in the pointer "sln" passed as the last argument.
    # k has the number of yards the solution is valid for, also the number of rows in the solution.
    hold_overs = ballistics.solve(range_max, drag_function, bc, v, bw, sh, angle,
                                  zeroangle, windspeed, windangle)

    # Get near and far zeros.
    zero1 = None
    zero2 = None
    testdir = "up"
    testnum = 1.0
    for point in hold_overs.points:
        if abs(point.path_inches) < testnum:
            testnum = abs(point.path_inches)
        if point.path_inches > 0 and testdir == "up":
            testdir = "down"
            testnum = 1.0
            if abs(point.path_inches) < lastinches:
                zero1 = str(point.yards) + " yards / " + str(point.meters) + " meters"
            else:
                zero1 = lastrange
        if point.path_inches < 0 and testdir == "down":
            if abs(point.path_inches) < lastinches:
                zero2 = str(point.yards) + " yards / " + str(point.meters) + " meters"
            else:
                zero2 = lastrange
            break
        lastinches = abs(point.path_inches)
        lastrange = str(point.yards) + " yards / " + str(point.meters) + " meters"

    if zero1 is not None:
        configuration['zero: 1st (near) approximate'] = zero1

    if zero2 is not None:
        configuration['zero: 2nd (far) approximate'] = zero2

    return configuration, hold_overs
