from app.util import timestring_to_seconds, seconds_to_timestring


def test_timestring_to_seconds():
    assert timestring_to_seconds('05') == 5
    assert timestring_to_seconds('45') == 45
    assert timestring_to_seconds('1:03') == 63
    assert timestring_to_seconds('1:37') == 97
    assert timestring_to_seconds('02:15') == 135
    assert timestring_to_seconds('01:00:00') == 3600
    assert timestring_to_seconds('1:0:1') == 3601


def test_seconds_to_timestring():
    assert seconds_to_timestring(5) == '00:05'
    assert seconds_to_timestring(63) == '01:03'
    assert seconds_to_timestring(601) == '10:01'
    assert seconds_to_timestring(3601) == '01:00:01'
    assert seconds_to_timestring(3663) == '01:01:03'