import math

def degc_to_degf(deg):
    """ This function converts from degrees centigrade to
        degrees fahrenheit.
          Input:   deg = degrees centigrade
          Output:  none
          Returns: degrees fahrenheit
    """
    return (deg * 1.8) + 32

def degf_to_degc(deg):
    """ This function converts from degrees fahrenheit to
        degrees centigrade.
          Input:   deg = degrees fahrenheit
          Output:  none
          Returns: degrees centigrade
    """
    return (deg - 32)/1.8

def grains_to_grams(grains):
    """ Convert bullet weight from grains to grams
          Input:   grains = weight in grains
          Output:  none
          Returns: weight in grams
    """
    return grains/15.432

def grams_to_grains(grams):
    """ This function converts bullet weight from grams to grains
          Input:   grams = weight in grams
          Output:  none
          Returns: weight in grains
    """
    return grams*15.432

def feet_to_meters(feet):
    """ This function converts a distance in feet to meters
          Input:   feet = distance in feet
          Output:  none
          Returns: distance in meters
    """
    return feet * 0.3048

def fps_to_mps(fps):
    """ This function coverts from feet per second to
        meters per second
         Inputs:  fps = bullet velocity in feet per second
         Outputs: none
         Returns: bullet velocity in meters per second
    """
    return fps * 0.3048

def inchToCm(inch):
    """ This function coverts from inches to centimeters.
         Inputs:  inch = length in inches
         Outputs: none
         Returns: length in centimeters.
    """
    return inch * 2.54

def inhg_to_mbar(pressure):
    """ This function converts inches of mercury to millibar
       Input:  pressure = inches of mercury (inHg) of pressure
       Output: measurement of pressure in mbar (millibar)
    """
    return round((pressure * 33.86386), 0)

def inhg_to_mmhg(pressure):
    """ This function converts inches of mercury to millimeters of mercury.
       Input:  pressure = inches of mercury (inHg) of pressure
       Output: measurement of pressure in mmHG (millimeters of mercury)
    """
    return round((pressure * 25.4), 2)

def kineticEnergy(vel, weight):
    """ This function returns kinetic energy of a projectile
         Inputs:  vel = velocity in feet per second
                  weight = bullet weight in grains
         Outputs: none
         Returns: length in centimeters.
    """
    return ((weight*(pow(vel,2)))/450800)

def kph_to_mph(kph):
    """ This function converts from kilometers per hour (kph)
        to miles per hour (mph)
          Input:   kph = speed in kilometers per hour
          Output:  none
          Returns: speed in miles per hour
    """
    return kph/1.609344

def mbar_to_inhg(pressure):
    """ This function converts millibar to inches of mercury
       Input:  pressure = millibar (mbar) of pressure
       Output: measurement of pressure in inhg (inches of mercury)
    """
    return round((pressure / 33.86386), 2)

def milToInch(mil, feet):
    """ This function us used to convert mils to inches
         Inputs:
           mil =  angle in milliradians
           feet = adjacent side in feet
         Outputs: none
         returns: adjacent side in inches
    """
    return (feet * 12) * (mil / 1000)

def meters_to_feet(meters):
    """ This function converts a distance in meters to feet
          Input:   meters = distance in meters
          Output:  none
          Returns: distance in feet
    """
    return meters * 3.280839895

def meters_to_yards(meters):
    """ This function converts a distance in meters to yards.
          Input:   meters = distance in meters
          Output:  none
          Returns: distance in yards
    """
    return meters*((100/2.54)/36)

def moaToMil(moa):
    """ This function us used
         Inputs: moa = angle in minutes
         Outputs: none
         returns: angle in milliradians
    """
    return moa * 0.29088821

def moaToInch(moa, feet):
    """ This function us used to convert moa to inches
         Inputs:
           moa =  angle in minutes
           feet = adjacent side in feet
         Outputs: none
         returns: adjacent side in inches
    """
    mil = moaToMil(moa)
    return milToInch(mil, feet)

def mmhg_to_inhg(pressure):
    """ This function converts millimeters of mercury to inches of mercury.
        Input:  pressure = millimeters of mercury (mmHg) of pressure
        Output: measurement of pressure in inHG (inches of mercury)
    """
    return round((pressure / 25.4), 2)

def mph_to_kph(mph):
    """ This function converts from miles per hour (mph) to
        kilometers per hour (kph).
          Input:   mph = speed in miles per hour
          Output:  none
          Returns: speed in kilometers per hour
    """
    return mph * 1.609344

def mps_to_fps(mps):
    """ This function converts from meters per second (mps) to
        feet per second (fps)
          Input:   mps = speed in meters per second
          Output:  none
          Returns: speed in feet per second
    """
    return mps*3.2808

def yards_to_meters(yards):
    """ This function converts a distance in yards to meters.
          Input:   yards = distance in yards
          Output:  none
          Returns: distance in meters
    """
    return yards/((100/2.54)/36)

def get_inital_upward_velocity(sight_height, time_of_flight):
    """ This function calculates the initial upward velocity used in the
    cant compensation calculation
    Inputs:
        sight_height =  distance of sight above bore height in inches
        time_of_flight = total time of flight to the target

    returns: initial upward velocity in feet per second (fps)

    Formula:
        vz0 = ( Sz / t ) - 1/2(gt)
        vz0 = initial upward velocity
        Sz = upward distance
        t = time of flight
        g = −32.137 feet per second squared
      Note:  the minus indicating the acceleration is “down”
      Source: https://www.empyrealsciences.com/Estimation%20of%20Shot%20Error%20due%20to%20Rifle%20Cant.pdf
    """

    return ((sight_height/12) / time_of_flight) + (0.5 * 32.137 * time_of_flight)


def get_incline_compensation(path_inches, incline_angle):
    return path_inches * math.cos(incline_angle) * -1


def get_cant_compensation(time_of_flight, cant_angle, sight_height):
    """
      https://www.empyrealsciences.com/Estimation%20of%20Shot%20Error%20due%20to%20Rifle%20Cant.pdf
    """
    initial_upward_velocity = get_inital_upward_velocity(
        sight_height, time_of_flight)
    horizontal_error = (initial_upward_velocity *
                        math.sin(cant_angle)) * time_of_flight
    vertical_error = -(initial_upward_velocity *
                       (1 - math.cos(cant_angle))) * time_of_flight
    return horizontal_error, vertical_error
