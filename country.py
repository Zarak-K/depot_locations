from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from plotting_utilities import plot_country, plot_path
import numpy as np
import pandas as pd
import warnings

if TYPE_CHECKING:
    from pathlib import Path

    from matplotlib.figure import Figure


def travel_time(
    distance,
    different_regions,
    locations_in_dest_region,
    speed=4.75,
):
    """
    Computes the travel time (in hours) between two locations based on the distance between them.
    Penalties are added if travelling between regions, and if there are many locations in the destination region i.e heavier traffic in busier regions.

    Inputs:
    1) distance - this is the distance in meters between the two locations
    2) different_regions - this is equal to 0 if the two locations are in the same region and 1 otherwise.
    3) locations_in_dest_region - this is the number of locations in the same region as the destination region (including the destination itself).
    4) speed - this is the speed in meters per second.
    """

    if speed == 0:
        raise ValueError('Speed must be non-zero')
    
    return float((1/3600)*(distance/speed)*(1+(different_regions*locations_in_dest_region)/10))


class Location:
    def __init__(self, name : str, region : str, r : float, theta : float, depot : bool):
        if not isinstance(name, str):
            raise TypeError(f'Expected "name" to be a string, got {type(name).__name__} instead.')

        if not isinstance(region, str):
            raise TypeError(f'Expected "region" to be a string, got {type(region).__name__} instead.')
        
        if not isinstance(r, (float, int)):
            raise TypeError(f'Expected "r" type to be a float, got {type(r).__name__} instead.')
        
        if not isinstance(theta, (float, int)):
            raise TypeError(f'Expected "theta" to be a float, got {type(theta).__name__} instead.')
        
        if not isinstance(depot, bool):
            raise TypeError(f'Expected "depot" to be a boolean, got {type(depot).__name__} instead.')
        
        if r < 0:
            raise ValueError(f'Expected r to be non-negative, got {r} instead.')
        
        if not (-np.pi <= theta <= np.pi):
            raise ValueError(f'Expected "theta" to lie between -pi and pi radians, got {theta} instead.')
        
        if not name.istitle():
            initial_name = name
            name = name.title()
            warnings.warn(f'name {initial_name} was not in title format, changed to {name}')

        self.name = name
        self.region = region
        self.r = r
        self.theta = theta
        self._depot = depot
        self._settlement = not self.depot

    @property
    def depot(self) -> bool:
        return self._depot
        
    @depot.setter
    def depot(self, value : bool):
        self._depot = value
        self._settlement = not value
    
    @property
    def settlement(self) -> bool:
        return self._settlement

    def __repr__(self):
        """
        Do not edit this function.
        You are NOT required to document or test this function.

        Not all methods of printing variable values delegate to the
        __str__ method. This implementation ensures that they do,
        so you don't have to worry about Locations not being formatted
        correctly due to these internal Python caveats.
        """
        return self.__str__()

    def __str__(self):
        if self.depot == True:
            return f'{self.name}, [depot] in {self.region} at {self.r: .2f}m, {self.theta / np.pi: .2f}π'
        else:
            return f'{self.name}, [settlement] in {self.region} at {self.r: .2f}m, {self.theta / np.pi: .2f}π'

    def distance_to(self, other):
        """
        Computes the distance between two locations in units of r.
        Inputs are two objects of the Location class.
        """
        distance = np.sqrt(self.r**2 + other.r**2 - 2*self.r*other.r*np.cos(self.theta - other.theta))
        return round(distance, 2)

    def __eq__(self, other):
        if not isinstance(other, Location):
            return NotImplemented
        return self.__dict__ == other.__dict__
    
    def __hash__(self) -> str:
        return hash(self.name + self.region)

class Country:
    def __init__(self, list_of_locations):

        if isinstance(list_of_locations, pd.DataFrame):
            
            if 'location' not in list_of_locations.columns:
                raise ValueError('DataFrame must contain a location column')
            
            if len(list_of_locations['location']) != len(set(list_of_locations['location'])):
                raise ValueError('Duplicate locations found')
            
            self._all_locations = tuple(Location(row['location'], row['region'], row['r'], row['theta'], row.get('depot', False))
                for _, row in list_of_locations.iterrows())
        
        elif isinstance(list_of_locations, list):
            locations = [location for location in list_of_locations]
            
            if len(locations) != len(set(locations)):
                raise ValueError('Duplicate locations found')
            
            self._all_locations = tuple(list_of_locations)
            
        else:
            raise ValueError('Input must be Pandas DataFrame or list of Location objects.')
        
    @property
    def all_locations(self):
        return self._all_locations
    
    @property
    def settlements(self):
        return [location for location in self._all_locations if not location.depot]
    
    @property
    def n_settlements(self):
        return len(self.settlements)

    @property
    def depots(self):
        return [location for location in self._all_locations if location.depot]
    
    @property
    def n_depots(self):
        return len(self.depots)
    
    def get_location(self, index : int):
        if isinstance(self._all_locations, pd.DataFrame):
            location = self._all_locations.iloc[index]
        else:
            location = self._all_locations[index]
        return location

    def __len__(self):
        return len(self.list_of_locations)

    def locations_in_region(self, region):
        count = sum(1 for location in self._all_locations if location.region == region)
        return count
    
    def travel_time(self, start_location, end_location):
        if start_location == None:
            raise ValueError('No start location was given')
        
        elif end_location == None:
            raise ValueError('No end location was given')

        elif start_location not in self._all_locations:
            raise ValueError(f'{start_location.name} is not a location in this Country')
        
        elif end_location not in self._all_locations:
            raise ValueError(f'{end_location.name} is not a location in this Country')
        
        else:
            distance = Location.distance_to(start_location, end_location)

            if start_location.region == end_location.region:
                different_regions = 0
            else:
                different_regions = 1

            n_locations_in_region = self.locations_in_region(end_location.region)
            time = travel_time(distance, different_regions, n_locations_in_region)

            return round(time, 2)

    def fastest_trip_from(self, current_location, potential_locations = None):
        
        if potential_locations is None:
            potential_locations = [location for location in self.settlements if location != current_location]
        
        travel_times = []
        travel_locations = []

        for location in potential_locations:
            if isinstance(location, Location):
                time = self.travel_time(current_location, location)
                travel_times.append(time)
                travel_locations.append(location)

            elif isinstance(location, int):
                indexed_location = self.get_location(location)
                time = self.travel_time(current_location, indexed_location)
                travel_times.append(time)
                travel_locations.append(indexed_location)
            
            else:
                raise ValueError('potential_locations must be a list containing objects of Location class or ints')

        fastest_time = np.min(travel_times)
        min_indices = np.where(travel_times == fastest_time)[0]
        closest_location_list = [travel_locations[i] for i in min_indices]

        if len(closest_location_list) > 1:
                sorted_closest_locations = sorted(closest_location_list, key = lambda location: (location.name, location.region))
                closest_location = sorted_closest_locations[0]
        else:
                closest_location = closest_location_list[0]

        if potential_locations == []:
                closest_location = None
                fastest_time = None

        return closest_location, fastest_time


    def nn_tour(self, starting_depot):
        settlements = list(self.settlements)

        tour = [starting_depot]
        time_between_settlements = []

        while settlements:
            current_location = tour[-1]
            next_settlement, time = self.fastest_trip_from(current_location, settlements)
            tour.append(next_settlement)
            time_between_settlements.append(time)
            settlements.remove(next_settlement)

            if next_settlement is None:
                break

        back_to_start_time = self.travel_time(tour[-1], starting_depot)
        tour.append(starting_depot)
        time_between_settlements.append(back_to_start_time)

        tour_time = sum(time_between_settlements)

        return tour, tour_time

    def best_depot_site(self, display = True):
        if not self.depots:
            raise ValueError('Country contains no depots')
        
        depots = list(self.depots)

        tour_time_list = []
        tour_list = []

        for depot in depots:
            tour, tour_time = self.nn_tour(depot)
            tour_list.append(tour)
            tour_time_list.append(tour_time)

        best_tour_time = min(tour_time_list)
        best_tour = tour_list[np.argmin(tour_time_list)]
        best_depot = depots[np.argmin(tour_time_list)]

        if display == True:
            print(f'The best depot is {best_depot} \nWith a total tour time of {best_tour_time: .2f}h \nThe route taken is:')
            for location in best_tour:
                print(f'\t{location}')

        return best_depot.name

    def plot_country(
        self,
        distinguish_regions: bool = True,
        distinguish_depots: bool = True,
        location_names: bool = True,
        polar_projection: bool = True,
        save_to: Optional[Path | str] = None,
    ) -> Figure:
        """

        Plots the locations that make up the Country instance on a
        scale diagram, either displaying or saving the figure that is
        generated.

        Use the optional arguments to change the way the plot displays
        the information.

        Attention
        ---------
        You are NOT required to write tests or documentation for this
        function; and you are free to remove it from your final
        submission if you wish.

        You should remove this function from your submission if you
        choose to delete the plotting_utilities.py file.

        Parameters
        ----------
        distinguish_regions : bool, default: True
            If True, locations in different regions will use different
            marker colours.
        distinguish_depots bool, default: True
            If True, depot locations will be marked with crosses
            rather than circles.  Their labels will also be in
            CAPITALS, and underneath their markers, if not toggled
            off.
        location_names : bool, default: True
            If True, all locations will be annotated with their names.
        polar_projection : bool, default: True
            If True, the plot will display as a polar
            projection. Disable this if you would prefer the plot to
            be displayed in Cartesian (x,y) space.
        save_to : Path, str
            Providing a file name or path will result in the diagram
            being saved to that location. NOTE: This will suppress the
            display of the figure via matplotlib.
        """
        return plot_country(
            self,
            distinguish_regions=distinguish_regions,
            distinguish_depots=distinguish_depots,
            location_names=location_names,
            polar_projection=polar_projection,
            save_to=save_to,
        )

    def plot_path(
        self,
        path: List[Location],
        distinguish_regions: bool = True,
        distinguish_depots: bool = True,
        location_names: bool = True,
        polar_projection: bool = True,
        save_to: Optional[Path | str] = None,
    ) -> Figure:
        """
        Plots the path provided on top of a diagram of the country,
        in order to visualise the path.

        Use the optional arguments to change the way the plot displays
        the information. Refer to the plot_country method for an
        explanation of the optional arguments.

        Attention
        ---------
        You are NOT required to write tests or documentation for this
        function; and you are free to remove it from your final
        submission if you wish.

        You should remove this function from your submission if you
        choose to delete the plotting_utilities.py file.

        Parameters
        ----------
        path : list
            A list of Locations in the country, where consecutive
            pairs are taken to mean journeys from the earlier location to
            the following one.
        distinguish_regions : bool, default: True,
        distinguish_depots : bool, default: True,
        location_names : bool, default: True,
        polar_projection : bool, default: True,
        save_to : Path, str

        See Also
        --------
        self.plot_path for a detailed description of the parameters
        """
        return plot_path(
            self,
            path,
            distinguish_regions=distinguish_regions,
            distinguish_depots=distinguish_depots,
            location_names=location_names,
            polar_projection=polar_projection,
            save_to=save_to,
        )
