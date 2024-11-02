import pytest
from country import travel_time, Location, Country
from utilities import read_country_data

#Tests for travel_time function
def test_same_region():
    distance = 36000
    different_regions = 0
    locations_in_dest = 0
    speed = 10
    expected_time = 1
    assert travel_time(distance, different_regions, locations_in_dest, speed) == expected_time

def test_different_region():
    distance = 36000
    different_regions = 1
    locations_in_dest = 1
    speed = 10
    expected_time = 1.1
    assert travel_time(distance, different_regions, locations_in_dest, speed) == expected_time

def test_locations_in_dest_region():
    distance = 36000
    different_regions = 1
    locations_in_dest = 10
    speed = 10
    expected_time = 2
    assert travel_time(distance, different_regions, locations_in_dest, speed) == expected_time

def test_no_distance():
    distance = 0
    different_regions = 1
    locations_in_dest = 1
    speed = 10
    expected_time = 0
    assert travel_time(distance, different_regions, locations_in_dest, speed) == expected_time

def test_no_speed():
    distance = 36000
    different_regions = 1
    locations_in_dest = 10
    speed = 0
    
    try:
        travel_time(distance, different_regions, locations_in_dest, speed)
        assert False, 'ValueError was not raised'
    except ValueError as e:
        assert str(e) == 'Speed must be non-zero'


