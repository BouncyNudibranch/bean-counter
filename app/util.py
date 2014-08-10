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


def test_timestring_to_seconds():
    assert timestring_to_seconds('05') == 5
    assert timestring_to_seconds('45') == 45
    assert timestring_to_seconds('1:03') == 63
    assert timestring_to_seconds('1:37') == 97
    assert timestring_to_seconds('02:15') == 135
    assert timestring_to_seconds('01:00:00') == 3600
    assert timestring_to_seconds('1:0:1') == 3601