import timeit
import matplotlib.pyplot as plt
import numpy as np
from utilities import regular_n_gon

#Plotting execution time Country.best_depot_site as a function of N locations in Country 
n_locs = np.unique(np.logspace(0, 9, base = 2, num = 75, dtype = int))

locs_to_test = n_locs

n_list = []
time_list = []

for integer in range(len(locs_to_test)):
    country = regular_n_gon(locs_to_test[integer])
    execution_time = timeit.timeit('country.best_depot_site(False)', globals = globals(), number = 10)

    n_list.append(locs_to_test[integer])
    time_list.append(execution_time)

plt.plot(n_list, time_list, marker = 'o', color = 'black', linestyle = '-', markersize = 2)
plt.xlabel('N settlements in Country')
plt.ylabel('Execution time (s)')
plt.yscale('log')
plt.grid(True, which='both', linestyle='--', linewidth=0.2)
plt.show()