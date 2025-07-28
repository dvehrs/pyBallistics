
import windage
import constants
import angles
import math
import numpy as np
import drag
import utils
from holdover import holdover
from points import points

import logging

def solve(range_max, drag_function, drag_coefficient, vi, bulletweight, sight_height, shooting_angle, zero_angle, wind_speed, wind_angle):

    logger = logging.getLogger()

    t = 0
    dt = 0
    v = 0
    vx = 0
    vx1 = 0
    vy = 0
    vy1 = 0
    dv = 0
    dvx = 0
    dvy = 0
    x = 0
    y = 0
    z = 0

    # Convert BALLISTICS_COMPUTATION_MAX_YARDS to feet
#    r = math.floor(constants.BALLISTICS_COMPUTATION_MAX_YARDS*3)
    r = math.floor((range_max+1)*3)

#    # Convert wind speed to inches per second.
#    # 1 mile == 5280 feet
#    # 3600 seconds in one hour
#    # (1 *  5280) * 12 / 3600 = 17.6
#    wind_ips = wind_speed * 17.6

#  20250727 - Meters calculation.
#    Testing 3.28084 feet per meter
#    This makes our individual step equal to  0.82021 feet.
#
#    Also tested with 3.280839895 and 0.82020997375
#
#   NEED TO REMEMBER TO CHANGE THE INTERVAL VALUE USED HERE BELOW IN DISPLAY
#   LOOP.  When they do not match, we will start seeing values skipped after 410
#   meters or so.
#
#   From testing there does not appear to be a difference between using 3.28084
#   and 3.280839895.  However there is a small difference in the Drop and Drift
#   Inches when using 3.2808.  So it appears that we need to go at least 5
#   decimal places into the value even though this value has been rounded up.
#
#    Using 3.28084 feet per meter

    # for determing the distances at which calculations are made, we work on
    # intervals of 1 foot or 0.82021 feet.  When we calculate our steps, the
    # step feet starts at zero but because we will combine step_meters with it
    # then step meters can start at the first 0.82021 interval.
#    step_feet = [*range(1, r, 1)]
    step_feet = [*range(0, r, 1)]
    step_meters = [*np.arange(0.82021, r, 0.82021)]
    # Old test values
#    step_meters = [*np.arange(0.8202, r, 0.8202)]
#    step_meters = [*np.arange(0.82020997375, r, 0.82020997375)]
    step_combined = np.round(sorted(step_feet + step_meters), 4)

    # Interval yards and meters has the same issue that steps does.  Interval
    # yards starts at zero and intercal meters starts at the first meter
    # (3.28084 feet).  That way when combined we only get one zero value.
#    interval_yards = [*range(3, r, 3)]
    interval_yards = [*range(0, r, 3)]
    interval_meters = [*np.arange(3.28084, r, 3.28084)]
    # Old test values
#    interval_meters = [*np.arange(3.2808, r, 3.2808)]
#    interval_meters = [*np.arange(3.280839895, r, 3.280839895)]
    interval_combined = set(np.round(sorted(interval_yards + interval_meters), 4))

    hwind = windage.headwind(wind_speed, wind_angle)
    cwind = windage.crosswind(wind_speed, wind_angle)

    # Convert crosswind speed to inches per second.
    cwind_ips = cwind * 17.6

    gy = constants.GRAVITY * \
        math.cos(angles.deg_to_rad((shooting_angle + zero_angle)))

    gx = constants.GRAVITY * \
        math.sin(angles.deg_to_rad((shooting_angle + zero_angle)))

    vx = vi * math.cos(angles.deg_to_rad(zero_angle))
    vy = vi * math.sin(angles.deg_to_rad(zero_angle))

    # y is in feet
    y = -sight_height/12

    n = 0

    hold_overs = points()

    for STEP in step_combined:
        logger.info("STEP: {}".format(STEP))
        vx1 = vx
        vy1 = vy
        v = math.pow(math.pow(vx, 2)+math.pow(vy, 2), 0.5)
        dt = (STEP - x)/v

        # Compute acceleration using the drag function retardation
        dv = drag.retard(drag_function, drag_coefficient, v+hwind)
        dvx = -(vx/v)*dv
        dvy = -(vy/v)*dv

        # Compute velocity, including the resolved gravity vectors.
        vx = vx + dt*dvx + dt*gx
        vy = vy + dt*dvy + dt*gy


        if STEP in interval_combined:
            range_yards = '{:.2f}'.format(round(STEP/3, 2))
#            print("range_yards {}".format(range_yards))
            logger.info("range_yards {}".format(range_yards))
            # Interval size for meters here needs to match what was used above.
            range_meters = '{:.2f}'.format(round(STEP/3.28084, 2))
            # Old Test Values - See notes on why we choose the value to use
            #                   above.
#            range_meters = '{:.2f}'.format(round(STEP/3.2808, 2))
#            range_meters = '{:.2f}'.format(round(STEP/3.280839895, 2))
#            print("range_meters {}".format(range_meters))
            logger.info("range_meters {}".format(range_meters))
            if x == 0:
                moa_correction = 0.0
            else:
                moa_correction = -angles.rad_to_moa(math.atan(y / x))
#            print("moa_correction {}". format(moa_correction))
            logger.info("moa_correction {}". format(moa_correction))
            mil_correction = utils.moaToMil(moa_correction)
#            print("mil_correction {}".format(mil_correction))
            logger.info("mil_correction {}". format(mil_correction))
            path_inches = y*12
#            print("path_inches {}". format(path_inches))
            logger.info("path_inches {}".format(path_inches))
            impact_in = utils.moaToInch(moa_correction, x)
            # Z already in inches, no need to convert.
            drift_inches = z
            logger.info("horizontal position inches {}".format(drift_inches))
            # Need to remember to convert X to inches so that both are in the
            # same unit of measurement.
            if x == 0:
                drift_moa = 0.0
            else:
                drift_moa = angles.rad_to_moa(math.atan(z / (x*12)))
            logger.info("drift MOA {}". format(drift_moa))
            drift_mil = utils.moaToMil(drift_moa)
            logger.info("drift MIL {}". format(drift_mil))
            seconds = t+dt
#            print("seconds {}". format(seconds))
            logger.info("seconds {}". format(seconds))
#            print("velocity {}", format(v))
            logger.info("velocity {}". format(v))
            ke = utils.kineticEnergy( v, bulletweight )
            logger.info("kinetic energy {}". format(ke))

            hold_overs.add_point(
                holdover(range_yards, range_meters, moa_correction, \
                         mil_correction, impact_in, path_inches, drift_inches, \
                         drift_moa, drift_mil, seconds, v, ke))

        z = z + ( cwind_ips * (dt - ((STEP - x)/vi)))
        # Compute position based on average velocity.
        y = y + dt * (vy+vy1)/2
        x = STEP

        if (math.fabs(vy) > math.fabs(3*vx) or n >= constants.BALLISTICS_COMPUTATION_MAX_YARDS):
            break

        t = t + dt

    return hold_overs
