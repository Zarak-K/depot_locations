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
        
        if not name.istitle():
            initial_name = name
            name = name.title()
            warnings.warn(f'name {initial_name} was not in title format, changed to {name}')

        if not isinstance(region, str):
            raise TypeError(f'Expected "region" to be a string, got {type(region).__name__} instead.')
        
        if not isinstance(r, (float, int)):
            raise TypeError(f'Expected "r" type to be a float, got {type(r).__name__} instead.')
        
        if r < 0:
            raise ValueError(f'Expected r to be non-negative, got {r} instead.')
        
        if np.pi > theta > np.pi:
            raise ValueError(f'Expected "theta" to lie between -pi and pi radians, got {theta} instead.')
        
        if not isinstance(theta, (float, int)):
            raise TypeError(f'Expected "theta" to be a float, got {type(theta).__name__} instead.')
        
        if not isinstance(depot, bool):
            raise TypeError(f'Expected "depot" to be a boolean, got {type(depot).__name__} instead.')

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
        raise NotImplementedError

    def distance_to(self, other):
        raise NotImplementedError


class Country:

    def travel_time(self, start_location, end_location):
        raise NotImplementedError

    def fastest_trip_from(
        self,
        current_location,
        potential_locations,
    ):
        raise NotImplementedError

    def nn_tour(self, starting_depot):
        raise NotImplementedError

    def best_depot_site(self, display):
        raise NotImplementedError

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
