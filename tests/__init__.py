"""
Bean Counter - Track Your Coffee!
Copyright (C) 2014  BonucyNudibranch (bouncynudibranch@gmail.com)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

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