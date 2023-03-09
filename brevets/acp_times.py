"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
from math import trunc

#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#
def speed(dist):
    if(dist <= 200):
        return [15, 34]
    elif(dist <= 400):
        return [15, 32]
    elif(dist <= 600):
        return[15, 30]
    elif(dist <= 1000):
        return [11.428, 28]
    else:
        return [13.333, 26]


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    distances = [200, 400, 600, 1000, 1300]
    difference = [200, 200, 200, 400, 300]
    time = 0
    i = 0
    for dist in distances:
      if control_dist_km <= 0:
         break
      if control_dist_km - dist > 0:
         speeds = speed(dist)[1]
         time += difference[i] / speeds
      elif control_dist_km - dist == 0:
         speeds = speed(dist)[1]
         time += difference[i] / speeds
         break
      else:
         remainder = control_dist_km -  (0 if i == 0 else distances[i - 1])
         speeds = speed(dist)[1]
         time += remainder / speeds
         break
      i += 1
    hour = trunc(time)
    time = time - hour
    minute = round(time * 60)
    open_time = brevet_start_time.shift(hours=+hour, minutes=+minute)
    return open_time

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    distances = [200, 400, 600, 1000, 1300]
    difference = [200, 200, 200, 400, 300]
    time = 0
    i = 0
    for dist in distances:
      if control_dist_km <= 0:
         break
      if control_dist_km - dist > 0:
         speeds = speed(dist)[0]
         time += difference[i] / speeds
      elif control_dist_km - dist == 0:
         speeds = speed(dist)[0]
         time += difference[i] / speeds
         break
      else:
         remainder = control_dist_km -  (0 if i == 0 else distances[i - 1])
         speeds = speed(dist)[0]
         time += remainder / speeds
         break
      i += 1
    if(control_dist_km < 60):
      time = (control_dist_km / 20) + 1
    hour = trunc(time)
    time = time - hour
    minute = round(time * 60)
    close_time = brevet_start_time.shift(hours=+hour, minutes=+minute)
    return close_time