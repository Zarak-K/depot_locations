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
    theta = -0.79
    depot = False
    
    new_location = Location(name, region, r, theta, depot)

    print(new_location)
    captured = capsys.readouterr()
    
    expected_output = 'Sens Fortress [settlement] in Clapham @ (140000.34m, -0.25pi)'
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
    ('Location 1', 'Region 1', 1000, 0, False, 'Location 2', 'Region 2', 2000, 0, False, 1000),                                #Testing different r values
    ('Location 1', 'Region 1', 1000, np.pi, False, 'Location 2', 'Region 2', 2000, np.pi/3, False, 2645.751311064591),         #Testing different r and theta values
    ('Location 1', 'Region 1', 1000, np.pi, False, 'Location 2', 'Region 2', 2000, -np.pi/3, False, 2645.751311064591),        #Testing negative theta values
    ('Location 1', 'Region 1', 1000, np.pi, False, 'Location 1', 'Region 1', 1000, np.pi, False, 0),                           #Testing same location
    ('Location 1', 'Region 1', 1000, np.pi, False, 'Location 2', 'Region 2', 2000, np.pi/3, True, 2645.751311064591)           #Testing different depot status       
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

#Testing Country instantiation with a list of Locations & properties of Country class
def test_country():
    list_of_locations = [
        Location('Firelink Shrine', 'Wimbledon', 100000, 0.24, True),
        Location('Anor Londo', 'Croydon', 120000, -0.08, True),
        Location('Undead Asylum', 'Kingston', 80000, 1.4, False),
        Location('Crystal Cave', 'Tooting Broadway', 60000, -1.9, False),
        Location('Izalith', 'Vietnam', 90000, 2.4, False),
    ]

    new_country = Country(list_of_locations)
    expected_settlements = [location for location in list_of_locations if not location.depot]
    expected_depots = [location for location in list_of_locations if location.depot]

    for i, location in enumerate(list_of_locations):
        assert str(new_country._all_locations[i]) == str(location)
    
    assert new_country.all_locations == tuple(list_of_locations)
    assert new_country.settlements == expected_settlements
    assert new_country.n_settlements == len(expected_settlements)
    assert new_country.depots == expected_depots
    assert new_country.n_depots == len(expected_depots)
    
#Testing Duplicate locations in DataFrame
def test_invalid_dataframe():
    file_path = Path("./data/test_duplicate_locs.csv").resolve()

    try:
        read_country_data(file_path)
        assert False, 'ValueError was not raised'
    except ValueError as e:
        assert str(e) == 'Duplicate locations found'

#Testing Duplicate locations in a list input
def test_invalid_list():
    locations = [
        Location('Firelink Shrine', 'Wimbledon', 100000, 0.24, True),
        Location('Firelink Shrine', 'Wimbledon', 100000, 0.24, True),
        Location('Undead Asylum', 'Kingston', 80000, 1.4, False),
        Location('Crystal Cave', 'Tooting Broadway', 60000, -1.9, False),
        Location('Izalith', 'Vietnam', 90000, 2.4, False)
    ]

    try:
        Country(locations)
        assert False, 'ValueError was not raised'
    except ValueError as e:
        assert str(e) == 'Duplicate locations found'

#Testing travel_time method
@pytest.mark.parametrize('name1, region1, r1, theta1, depot1, name2, region2, r2, theta2, depot2, expected', [
    ('Location 1', 'Region 1', 1000, 0, False, 'Location 2', 'Region 1', 2000, 0, False, 0.05847953216374269),              #Testing travel between locations in the same region
    ('Location 1', 'Region 1', 1000, 0, False, 'Location 2', 'Region 2', 2000, 0, False, 0.06432748538011696),              #Testing travel between regions
    ('Location 1', 'Region 1', 1000, np.pi, False, 'Location 2', 'Region 2', 2000, np.pi/3, False, 0.17019452878193278),    #Testing different r and theta values
    ('Location 1', 'Region 1', 1000, np.pi, False, 'Location 2', 'Region 2', 2000, -np.pi/3, False, 0.17019452878193278),   #Testing negative theta values
    ])

def test_travel_time_method(name1, region1, r1, theta1, depot1, name2, region2, r2, theta2, depot2, expected):
    location1 = Location(name1, region1, r1, theta1, depot1)
    location2 = Location(name2, region2, r2, theta2, depot2)
    
    locations = [location1, location2]

    new_country = Country(locations)
    assert new_country.travel_time(location1, location2) == expected

#Testing fastest_trip_from method
def test_fastest_trip():
    location1 = Location('Location 1', 'Region 1', 10000, 0, False)
    location2 = Location('Location 2', 'Region 2', 20000, 0, False)
    location3 = Location('Location 3', 'Region 3', 50000, 0, False)

    locations = [location1, location2, location3]

    new_country = Country(locations)

    closest_location, fastest_time = new_country.fastest_trip_from(location1)

    assert closest_location == location2
    assert fastest_time == 0.6432748538011696

#Testing locations being input as indices from a list of locations
def test_potential_locations_as_indices():
    location1 = Location('Location 1', 'Region 1', 10000, 0, False)
    location2 = Location('Location 2', 'Region 2', 20000, 0, False)
    location3 = Location('Location 3', 'Region 3', 50000, 0, False)

    locations = [location1, location2, location3]

    new_country = Country(locations)

    closest_location, fastest_time = new_country.fastest_trip_from(location1, [1, 2])

    assert closest_location == location2
    assert fastest_time == 0.6432748538011696

#Testing inputs as a mixture of indices and location objects
def test_potential_locations_as_mixed_and_indices():
    location1 = Location('Location 1', 'Region 1', 10000, 0, False)
    location2 = Location('Location 2', 'Region 2', 20000, 0, False)
    location3 = Location('Location 3', 'Region 3', 50000, 0, False)

    locations = [location1, location2, location3]

    new_country = Country(locations)

    closest_location, fastest_time = new_country.fastest_trip_from(location1, [location2, 2])

    assert closest_location == location2
    assert fastest_time == 0.6432748538011696

#Testing tie breaker based on alphabetical order of name
def test_tie_breaker_name():
    location1 = Location('Location 1', 'Region 1', 10000, 0, False)
    location2 = Location('Harambe', 'Region 2', 20000, 0, False)
    location3 = Location('Anor Londo', 'Region 3', 20000, 0, False)

    locations = [location1, location2, location3]

    new_country = Country(locations)

    closest_location, fastest_time = new_country.fastest_trip_from(location1)

    assert closest_location == location3
    assert fastest_time == 0.6432748538011696

#Testing tied names being broken by alphabetical order of region
def test_tie_breaker_region():
    location1 = Location('Location 1', 'Region 1', 10000, 0, False)
    location2 = Location('Harambe', 'A', 20000, 0, False)
    location3 = Location('Harambe', 'Z', 20000, 0, False)

    locations = [location1, location2, location3]

    new_country = Country(locations)

    closest_location, fastest_time = new_country.fastest_trip_from(location1)

    assert closest_location == location2
    assert fastest_time == 0.6432748538011696

#Testing nn_tour method returns appropriate tour and tour time. Testing invalid input.
def test_nn_tour():
    
    depot1 = Location('Firelink Shrine', 'Wimbledon', 0, 0, True)
    depot2 = Location('Anor Londo', 'Croydon', 50000, 0, True)
    settlement1 = Location('Undead Asylum', 'Kingston', 100000, 0, False)
    settlement2 = Location('Crystal Cave', 'Tooting Broadway', 150000, 0, False)

    locations = [depot1, depot2, settlement1, settlement2]
    dark_souls = Country(locations)

    tour_dep1, tour_time_dep1 = dark_souls.nn_tour(depot1)

    assert tour_dep1 == [depot1, settlement1, settlement2, depot1]
    assert tour_time_dep1 == 19.29824561403509

#Testing best_depot_site function
def test_best_depot_site():

    depot1 = Location('Firelink Shrine', 'Wimbledon', 0, 0, True)
    depot2 = Location('Anor Londo', 'Croydon', 50000, 0, True)
    depot3 = Location('Izalith', 'Essex', 200000, 0, True)
    depot4 = Location('Amanita Muscaria', 'A', 200000, 0, True)
    settlement1 = Location('Undead Asylum', 'Kingston', 100000, 0, False)
    settlement2 = Location('Crystal Cave', 'Tooting Broadway', 150000, 0, False)

    locations_basic = [depot1, depot2, settlement1, settlement2]
    dark_souls_basic = Country(locations_basic)

    best_depot_tied = [depot1, depot2, depot3, settlement1, settlement2]
    dark_souls_tied = Country(best_depot_tied)

    best_depot_name_tied = [depot2, depot3, depot4, settlement1, settlement2]
    dark_souls_name_tied = Country(best_depot_name_tied)

    assert dark_souls_basic.best_depot_site() == depot2          #Testing basic functionality
    assert dark_souls_tied.best_depot_site() == depot2           #Testing tied best depots, selecting first in alphabetical order by name
    assert dark_souls_name_tied.best_depot_site() == depot4      #Testing tied name alphabetical order, selecting first in alphabetical order by region
















