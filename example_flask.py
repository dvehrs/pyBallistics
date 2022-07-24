"""
Simple flask application for calculating bullet ballistics
"""

import os
import operator
from flask import Flask, render_template, request, redirect
from cachetools import cached, TTLCache
from bdc import calcBDC
from utils import get_incline_compensation
from utils import get_cant_compensation
from utils import fps_to_mps
from utils import inchToCm

#app = Flask(__name__)
#app = Flask(__name__, root_path='flask_files/')
app = Flask(__name__, root_path=os.path.join(os.getcwd(), 'FlaskFiles/'))
app.config.from_pyfile('config.py')

# Caching is useful for apps and data that do not change frequently.  Be
# interesting to see what effect it has on pages generated dynamically by scripts.
cache = TTLCache(maxsize=100, ttl=60)

@app.route('/', methods=['GET', 'POST'])
def base():
    '''
    Decides how to handle incoming methods
    '''
    if request.method == 'POST':
        my_data=request.form
    elif request.method == 'GET':
        # Returns base page
        my_data={
            "dragfunc": "G1",
            "bc": 0.121,
            "bweight": 41,
            "muzvel": 1051,
            "unitsp": "fps",
            "zerofilter": "range",
            "zerorange": 51,
            "unitzero": 'y',
            "sheight": 1.6,
            "sangle": 1,
            "wspeed": 1,
            "unit_wndspd": "mph",
            "wangle": 1,
            "altitude": 1,
            "unit_altitude": "feet",
            "temperature": 59,
            "unit_temp": "fahrenheit",
            "barometric": 29.92,
            "humidity": 50,
            "localadjust" : 'False'
        }

        # for base page default values, it seems to be best to not include
        # "bangle" for zero bore angle.

    else:
        return 'Not a valid request method for this route'

#    print("my_data stuff")
#    for key,value in my_data.items():
#        print(key, ':', value)
#    print("------------")
#    print("Does Python", "automatically add spaces", "between items?")
#    answer: yes it does.
#    print("------------")

    buildconf = {}
    buildconf['ammunition name'] = 'Configuration'
    buildconf['range max'] = 1001

    buildconf['ballistic coefficient'] = float(my_data['bc']) if 'bc' in my_data else 0.120
    buildconf['bullet weight'] = float(my_data['bweight']) if 'bweight' in my_data else 40
    buildconf['velocity - muzzle'] = int(my_data['muzvel']) if 'muzvel' in my_data else 1050
    buildconf['sight height'] = float(my_data['sheight']) if 'sheight' in my_data else 2
    buildconf['angle - shooting'] = float(my_data['sangle']) if 'sangle' in my_data else 0
    buildconf['zero - distance'] = float(my_data['zerorange']) if 'zerorange' in my_data else 50

    buildconf['zero - unit'] = my_data['unitzero'] if 'unitzero' in my_data else 'y'

    buildconf['drag function'] = my_data['dragfunc'] if 'dragfunc' in my_data else 'G1'

    buildconf['localadjust'] = my_data['localadjust'] if 'localadjust' in my_data else 'False'

    print("local adjust: \'", my_data['localadjust'], "\'")
    if "localadjust" in my_data and my_data["localadjust"] == "False":
        print("true side")
        print("local adjust: ", buildconf['localadjust'])
        buildconf['wind - speed'] = 0
        buildconf['wind - unit'] = "mph"
        buildconf['wind - angle'] = 0
        buildconf['altitude'] = 0
        buildconf['altitude - unit'] = "feet"
        buildconf['temperature'] = 59
        buildconf['temperature - unit'] = "fahrenheit"
        buildconf['barometer'] = 29.92
        buildconf['humidity - relative'] = 0.5
    else:
        print("else side")
        print("local adjust: ", buildconf['localadjust'])
        buildconf['wind - speed'] = float(my_data['wspeed']) if 'wspeed' in my_data else 10
        buildconf['wind - unit'] = my_data['unit_wndspd'] if 'unit_wndspd' in my_data else "mph"
        buildconf['wind - angle'] = float(my_data['wangle']) if 'wangle' in my_data else 90
        buildconf['altitude'] = float(my_data['altitude']) if 'altitude' in my_data else 0
        buildconf['altitude - unit'] = my_data['unit_altitude'] \
                if 'unit_altitude' in my_data else "feet"
        buildconf['temperature'] = float(my_data['temperature']) if 'temperature' in my_data else 59
        buildconf['temperature - unit'] = my_data['unit_temp'] \
                if 'unit_temp' in my_data else "fahrenheit"
        buildconf['barometer'] = float(my_data['barometric']) if 'barometric' in my_data else 29.92
        buildconf['humidity - relative'] = float(my_data['humidity'])/100 \
                if 'humidity' in my_data else  0.5



    #buildconf['angle - bore'] = float(my_data['bangle']) if 'bangle' in my_data else None
    #buildconf['angle - bore'] = None
    #buildconf['angle - bore'] = None if 'bangle' not in my_data else float(my_data['bangle'])
    try:
        buildconf['angle - bore'] = float(my_data['bangle'])
    except (KeyError, ValueError):
        buildconf['angle - bore'] = None


#    print("drag function: ", my_data['dragfunc'])
#    print("ballistic coefficient: ", my_data['bc'])
#    print("bullet weight: ", my_data['bweight'])
#    print("velocity - muzzle: ", my_data['muzvel'])
#    print("sight height: ", my_data['sheight'])
#    print("drag function: ", buildconf['drag function'])
#    print("ballistic coefficient: ", buildconf['ballistic coefficient'])
#    print("bullet weight: ", buildconf['bullet weight'])
#    print("velocity - muzzle: ", buildconf['velocity - muzzle'])
#    print("sight height: ", buildconf['sight height'])
#    print("zero range: ", buildconf['zero - distance'])
#    print("zero unit: ", buildconf['zero - unit'])
#    print("local adjust: ", buildconf['localadjust'])
#    print("wind - speed", buildconf['wind - speed'])
#    print("wind - unit", buildconf['wind - unit'])
#    print("wind - angle", buildconf['wind - angle'])
#    print("altitude", buildconf['altitude'])
#    print("altitude - unit", buildconf['altitude - unit'])
#    print("temperature", buildconf['temperature'])
#    print("temperature - unit", buildconf['temperature - unit'])
#    print("barometer", buildconf['barometer'])
#    print("humidity - relative", buildconf['humidity - relative'])

    configuration, hold_overs = calcBDC(buildconf)

    my_list = []
    for point in hold_overs.points:
        if (float(point.yards).is_integer()) or (float(point.meters).is_integer()):
            tmpdict = {}
            tmpdict["yards"] = point.yards
            tmpdict["meters"] = point.meters
            tmpdict["dinch"] = f'{round(point.path_inches, 3):.3f}'
            tmpdict["dcent"] = f'{round(inchToCm(point.path_inches), 3):.3f}'
            tmpdict["dmoa"] = f'{round(point.moa_correction, 2):.2f}'
            tmpdict["dmil"] = f'{round(point.mil_correction, 2):.2f}'
            tmpdict["hinch"] = f'{round(point.drift_inches, 3):.3f}'
            tmpdict["hcent"] = f'{round(inchToCm(point.drift_inches), 3):.3f}'
            tmpdict["hmoa"] = f'{round(point.drift_moa, 2):.2f}'
            tmpdict["hmil"] = f'{round(point.drift_mil, 2):.2f}'
            tmpdict["time"] = f'{round(point.seconds, 3):.3f}'
            tmpdict["vfps"] = f'{round(point.velocity, 2):.2f}'
            tmpdict["vmps"] = f'{round(fps_to_mps(point.velocity), 2):.2f}'
            tmpdict["kine"] = f'{round(point.kinetic_energy, 2):.2f}'
            my_list.append(tmpdict)

    # Sort configuration so it reads better
#    myConf = dict(sorted(configuration.items(), key=operator.itemgetter(0)))

    # Copy out parts of dictionaries to have three parts.
    conf_dict1 = dict(filter(lambda item: "local" in item[0], configuration.items()))
    conf_dict2 = dict(filter(lambda item: "zero" in item[0], configuration.items()))

    # Remove keys and items for things in previous dictionaries.
    conf_dict3 = configuration.copy()
    for key in conf_dict1.keys():
        conf_dict3.pop(key, None)

    for key in conf_dict2.keys():
        conf_dict3.pop(key, None)

    # Update keys in conf_dict1 to remove "local:"
    tmpset = set(conf_dict1.keys())
    for key in tmpset:
        newkey = key.replace("local: ", "", 1)
        conf_dict1[newkey] = conf_dict1.pop(key)

    # Update keys in conf_dict2 to remove "zero:"
    tmpset = set(conf_dict2.keys())
    for key in tmpset:
        newkey = key.replace("zero: ", "", 1)
        conf_dict2[newkey] = conf_dict2.pop(key)

    # Sort Dictionaries
    conf_dict1 = dict(sorted(conf_dict1.items(), key=operator.itemgetter(0)))
    conf_dict2 = dict(sorted(conf_dict2.items(), key=operator.itemgetter(0)))
    conf_dict3 = dict(sorted(conf_dict3.items(), key=operator.itemgetter(0)))

    # Remove items from output list because of what appear to be duplicate
    # records.  This seems to happen because of rounding to the hundredths
    # position for the meters and yards values.
    #
    # Using various inputs, this appeared to happen at:
    #    Yards:  35 222 257 444 479 666 701 888 923
    #    Meters: 32 203 235 406 438 609 641 812 844
    #
    # I believe this is caused by how we are incrementing our position in
    # horizontal axis.  Since the output table is oriented around distance
    # from the shooting position the listing of two apparently very similar
    # results could cause confusion about which to use.
    #
    # The second listing for each point had minor differences but probably
    # not enough to justify keeping the duplicate listings.  For example,
    # for the drop category the difference in MOA and MIL were frequently
    # in the hundredths position so far below what any scope can adjust for.
    #
    # If we want to see these, we can add a check to disable this
    # deduplication loop.
    seenset = set()
    deduplicatedlist = []
    for tmpdict2 in my_list:
        tup1 = tuple(tmpdict2['yards'])
        tup2 = tuple(tmpdict2['meters'])
        tup3 = tup1 + tup2
        if tup3 not in seenset:
            seenset.add(tup3)
            deduplicatedlist.append(tmpdict2)
        #else:
        #    print("duplicate found at yard: ", tmpdict2['yards'])


    return render_template('base.html', myData=my_data, myList=deduplicatedlist,
                           confdict1=conf_dict1, confdict2=conf_dict2, confdict3=conf_dict3)

if __name__ == "__main__":
    app.run()
