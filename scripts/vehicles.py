# vehicles.py
# read travel times from csv and animate in blender
# created 2013-11-04, sunarjob@ethz.ch

# file structure (headings)
# 0: eventId
# 1: serviceDate
# 2: date
# 3: tripId
# 4: tripStart
# 5: routeId
# 6: routeNumber
# 7: routeNameShort
# 8: routeName
# 9: routeVLD
# 10: runNumber
# 11: direction
# 12: stopSequenceNr
# 13: stopId
# 14: stopNumber
# 15: stopNameShort
# 16: stopName
# 17: arrivalScheduled
# 18: departureScheduled
# 19: arrivalActual
# 20: departureActual
# 21: mileage
# 22: vehicleId
# 23: vehicleTechnicalId
# 24: vehicleNumber
# 25: vehiclePlate
# 26: vehicleVLD
# 27: patternId
# 28: patternNumber
# 29: patternNameShort
# 30: patternName
# 31: patternType
# 32: patternVld
# 33: blockId
# 34: blockNumber
# 35: blockVld
# 36: daytyp_id
# 37: daytyp_number
# 38: daytyp_short
# 39: daytyp_long
# 40: daytyp_vld
# 41: branchId
# 42: branchNumber
# 43: branchNameShort
# 44: branchName
# 45: branchVld
# 46: longitudeScheduled
# 47: latitudeScheduled
# 48: longitudeActual
# 49: latitudeActual
# 50: directionScheduled
# 51: directionActual


# import libraries
import csv  # provides csv reader object for parsing


# Data on bus/train/tram stops
stops = {}
# read csv
with open('../data/vbz_stops.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=';')
    reader.next() # skip one row (header)
    for row in reader:
        # stops[id] = [x-coord, y-coord]
        stops[row[0]] = [row[4], row[5]]


# Data on scheduled and actual arrival and departure times
vehicles_actual = {}
vehicles_scheduled = {}
# read csv
# ( takes 46s to read 124213 lines )
with open('../data/vbz_selection.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    reader.next() # skip one row (header)
    for row in reader:
        vID = row[22] # vehicleId
        sID = row[13] # stopID
        pos = stops[sID] # x/y-coordinates
        tsa = row[17] # arrivalScheduled
        tsd = row[18] # departureScheduled
        taa = row[19] # arrivalActual
        tad = row[20] # departureActual
        
        # if vehicleID exists, append arrival, otherwise initialize
        if vID in vehicles_actual:
            # vehicleID = [[time, pos], [time, pos], ...]
            vehicles_actual[vID].append([taa, pos])
            vehicles_scheduled[vID].append([tsa, pos])
        else:
            vehicles_actual[vID] = [[taa, pos]]
            vehicles_scheduled[vID] = [[tsa, pos]]
        
        # if departure and arrival times are different, append departure
        # (some buses don't always stop, no need to add duplicate points)
        if tsa != tsd:
            vehicles_actual[vID].append([tsd, pos])
        if taa != tad:
            vehicles_scheduled[vID].append([tad, pos])


# create blender animation!
# iterate through all vehicles
for vehicle, values in vehicles_scheduled.iteritems():
    # create a point in blender using shapely
    # ... = k
    
    # set keyframes for that point
    for v in values:
        time = v[0] # time in seconds
        pos = v[1] # position vector CH1903
        #print time, pos


