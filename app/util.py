from math import floor

SEC_PER_MIN = 60
SEC_PER_HR = 60 * SEC_PER_MIN
SEC_PER_DAY = 24 * SEC_PER_HR


def timestring_to_seconds(timestr):
    time = timestr.split(':')
    if len(time) == 4:  # dd:hh:mm:ss
        return int(time[0]) * SEC_PER_DAY + int(time[1]) * SEC_PER_HR + int(time[2]) * SEC_PER_MIN + int(time[3])
    elif len(time) == 3:  # hh:mm:ss
        return int(time[0]) * SEC_PER_HR + int(time[1]) * SEC_PER_MIN + int(time[2])
    elif len(time) == 2:  # mm:ss
        return int(time[0]) * SEC_PER_MIN + int(time[1])
    elif len(time) == 1:  # ss
        return int(time[0])
    else:
        return None


def seconds_to_timestring(seconds):
    if seconds < SEC_PER_MIN:
        return "00:{:02d}".format(seconds)
    elif seconds < SEC_PER_HR:
        mins = int(floor(seconds / SEC_PER_MIN))
        sec = seconds % SEC_PER_MIN
        return "{:02d}:{:02d}".format(mins, sec)
    elif seconds < SEC_PER_DAY:
        hrs = int(floor(seconds / SEC_PER_HR))
        mins = int(floor((seconds - (hrs * SEC_PER_HR)) / SEC_PER_MIN))
        sec = seconds - mins * SEC_PER_MIN - hrs * SEC_PER_HR
        return "{:02d}:{:02d}:{:02d}".format(hrs, mins, sec)
    else:
        days = int(floor(seconds / SEC_PER_DAY))
        hrs = int(floor((seconds - days * SEC_PER_DAY) / SEC_PER_HR))
        mins = int(floor((seconds - days * SEC_PER_DAY - hrs * SEC_PER_HR) / SEC_PER_MIN))
        sec = seconds - days * SEC_PER_DAY - hrs * SEC_PER_HR - mins * SEC_PER_MIN
        return "{:02d}:{:02d}:{:02d}:{:02d}".format(days, hrs, mins, sec)