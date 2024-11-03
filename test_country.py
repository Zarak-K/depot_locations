import pytest
from country import travel_time, Location, Country
from utilities import read_country_data
from pathlib import Path
import numpy as np

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

    #Setting settlement manually should raise an error
    try:
        new_location.settlement = True
        assert False, "AttributeError was not raised"
    except AttributeError as e:
        assert str(e) == "property 'settlement' of 'Location' object has no setter"

#Testing print to display Location
def test_print_location(capsys):
    name = 'Sens Fortress'
    region = 'Clapham'
    r = 140000.342
    theta = -2.496
    depot = False
    
    new_location = Location(name, region, r, theta, depot)

    print(new_location)
    captured = capsys.readouterr()
    
    expected_output = 'Sens Fortress, [settlement] in Clapham at  140000.34m, -0.79π'
    assert captured.out.strip() == expected_output

#Testing invalid inputs
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

#Testing out of range inputs
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

#Testing distance_to method
@pytest.mark.parametrize('name1, region1, r1, theta1, depot1, name2, region2, r2, theta2, depot2, expected', [
    ('Location 1', 'Region 1', 1000, 0, False, 'Location 2', 'Region 2', 2000, 0, False, 1000),                      #Testing different r values
    ('Location 1', 'Region 1', 1000, np.pi, False, 'Location 2', 'Region 2', 2000, np.pi/3, False, 2645.75),         #Testing different r and theta values
    ('Location 1', 'Region 1', 1000, np.pi, False, 'Location 2', 'Region 2', 2000, -np.pi/3, False, 2645.75),        #Testing negative theta values
    ('Location 1', 'Region 1', 1000, np.pi, False, 'Location 1', 'Region 1', 1000, np.pi, False, 0),                 #Testing same location
    ('Location 1', 'Region 1', 1000, np.pi, False, 'Location 2', 'Region 2', 2000, np.pi/3, True, 2645.75)           #Testing different depot status       
    ])

def test_distance_to(name1, region1, r1, theta1, depot1, name2, region2, r2, theta2, depot2, expected):
    location_1 = Location(name1, region1, r1, theta1, depot1)
    location_2 = Location(name2, region2, r2, theta2, depot2)

    assert location_1.distance_to(location_2) == expected

#Testing equality
def test_equality():
    name1, name2 = 'Harambe', 'Harambe'
    region1, region2 = 'Heaven', 'Heaven'
    r1, r2 = 500, 500
    theta1, theta2 = np.pi, np.pi
    depot1, depot2 = True, True

    location1 = Location(name1, region1, r1, theta1, depot1)
    location2 = Location(name2, region2, r2, theta2, depot2)

    assert location1 == location2



##TESTS FOR COUNTRY CLASS
#Testing Country instantiation using read_country_data function
def test_read_country():
    file_path = Path("./data/test_set.csv").resolve()
    
    new_country = read_country_data(file_path)

    expected_locations = [
        Location('Firelink Shrine', 'Wimbledon', 100000, 0.24, True),
        Location('Anor Londo', 'Croydon', 120000, -0.08, True),
        Location('Undead Asylum', 'Kingston', 80000, 1.4, False),
        Location('Crystal Cave', 'Tooting Broadway', 60000, -1.9, False),
        Location('Izalith', 'Vietnam', 90000, 2.4, False)
    ]

    for i, location in enumerate(expected_locations):
        assert str(new_country._all_locations[i]) == str(location)

#Testing Country instantiation with a list of Locations
def test_country():
    list_of_locations = [
        Location('Firelink Shrine', 'Wimbledon', 100000, 0.24, True),
        Location('Anor Londo', 'Croydon', 120000, -0.08, True),
        Location('Undead Asylum', 'Kingston', 80000, 1.4, False),
        Location('Crystal Cave', 'Tooting Broadway', 60000, -1.9, False),
        Location('Izalith', 'Vietnam', 90000, 2.4, False),
    ]

    new_country = Country(list_of_locations)

    for i, location in enumerate(list_of_locations):
        assert str(new_country._all_locations[i]) == str(location)

#Testing invalid inputs
@pytest.mark.parametrize('file_path, error_message', [
    (Path("./data/test_no_location.csv").resolve(), 'DataFrame must contain a location column'),    #Testing no Location Column
    (Path("./data/test_duplicate_locs.csv").resolve(), 'Duplicate locations found'),                #Testing duplicate Locations
])

def test_invalid_dataframe(file_path, error_message):
    
    with pytest.raises(ValueError) as error:
        Country(read_country_data(file_path))
        assert str(error.value) == error_message

#Testing Duplicate locations in a list input
def test_invalid_list():
    locations = [
        Location('Firelink Shrine', 'Wimbledon', 100000, 0.24, True),
        Location('Firelink Shrine', 'Croydon', 120000, -0.08, True),
        Location('Undead Asylum', 'Kingston', 80000, 1.4, False),
        Location('Crystal Cave', 'Tooting Broadway', 60000, -1.9, False),
        Location('Izalith', 'Vietnam', 90000, 2.4, False)
    ]

    try:
        Country(locations)
        assert False, 'ValueError was not raised'
    except ValueError as e:
        assert str(e) == 'Duplicate locations found'

#Testing input which is neither a dataframe nor list of locations
def test_invalid_input_type():
    locations = 'Harambe'

    try:
        Country(locations)
        assert False, 'ValueError was not raised'
    except ValueError as e:
        assert str(e) == 'Input must be Pandas DataFrame or list of Location objects.'









