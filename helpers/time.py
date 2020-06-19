def timeSlotDurations():
    durations = [10, 15, 20, 30, 60, 120, 180, 240, 360]
    return durations


def stringTimeToMinutes(time):
    return (int(time.split(":")[0]) * 60) + int(time.split(":")[1])


def minutesToStringTime(minutes):
    time = divmod(minutes, 60)
    hours = time[0]
    minutes = time[1]
    if(hours < 10):
        hours = "0"+str(hours)
    if(minutes < 9):
        minutes = "0"+str(minutes)

    return ("%s:%s" % (hours, minutes))
