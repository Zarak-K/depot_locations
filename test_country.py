import pytest
from country import travel_time, Location, Country
from utilities import read_country_data

## TESTS FOR TRAVEL TIME FUNCTION ##
@pytest.mark.parametrize('distance, different_regions, locations_in_dest, speed, expected_time', [
        (36000, 0, 0, 10, 1),      #Testing travel within same region
        (36000, 1, 1, 10, 1.1),    #Testing travel to different region
        (36000, 1, 10, 10, 2),     #Testing for multiple locations within destination region
        (0, 1, 1, 10, 0)           #Testing for no distance provided  
])

def test_travel_time(distance, different_regions, locations_in_dest, speed, expected_time):
    assert travel_time(distance, different_regions, locations_in_dest, speed) == expected_time


#Testing travel_time when speed = 0
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



## TESTS FOR LOCATION CLASS ##
#Testing class instantiation
def test_location_class():
    name = 'Sens Fortress'
    region = 'Clapham'
    r = 140000.342
    theta = -2.496
    depot = False
    
    new_location = Location(name, region, r, theta, depot)
    assert isinstance(new_location, Location)
    assert new_location.name == name
    assert new_location.region == region
    assert new_location.r == r
    assert new_location.theta == theta
    assert new_location.depot == depot


@pytest.mark.parametrize('name, region, r, theta, depot, error_message', [
    (50, 'Clapham', 50, 1.6, False, 'Expected "name" to be a string, got int instead.'),                        #Testing invalid name input                 
    ('Sens Fortress', 50, 50, 1.6, False, 'Expected "region" to be a string, got int instead.'),                #Invalid reigon input          
    ('Sens Fortress', 'Clapham', 'Harambe', 1.6, False, 'Expected "r" type to be a float, got str instead.'),   #Invalid r input
    ('Sens Fortress', 'Clapham', 50, 'Harambe', False, 'Expected "theta" to be a float, got str instead.'),     #Invalid theta input
    ('Sens Fortress', 'Clapham', 50, 1.6, 'Harambe', 'Expected "depot" to be a boolean, got str instead.')      #Invalid depot input
])

def test_invalid_types(name, region, r, theta, depot, error_message):
    with pytest.raises(TypeError) as error:
        Location(name, region, r, theta, depot)
    
    assert str(error.value) == error_message



@pytest.mark.parametrize('name, region, r, theta, depot, error_message', [
    ('Sens Fortress', 'Clapham', -50, 1.6, False, 'Expected r to be non-negative, got -50 instead.'),                      #Testing negative r values                   
    ('Sens Fortress', 'Clapham', 50, 50, False, 'Expected "theta" to lie between -pi and pi radians, got 50 instead.')     #Testing theta out of range 
])

def test_invalid_values(name, region, r, theta, depot, error_message):
    with pytest.raises(ValueError) as error:
        Location(name, region, r, theta, depot)
    
    assert str(error.value) == error_message



#Testing uncapitalized name input
def test_uncapitalized_name():
    name = 'sEns fOrTrESs'
    region = 'Clapham'
    r = 140000.342
    theta = -2.496
    depot = False
    
    with pytest.warns(UserWarning) as warning:
        Location(name, region, r, theta, depot)

    assert len(warning) == 1
    assert str(warning[0].message) == 'name sEns fOrTrESs was not in title format, changed to Sens Fortress'




