import numpy as np
import matplotlib.pyplot as plt
from random import randrange
from matplotlib import cm

# Define necessary functions
def numberOfLocal(i, j):
    local_infected = 0
    if (population[(i-1) % SQRT_POPULATION_SIZE][(j-1) % SQRT_POPULATION_SIZE] > 0):
        local_infected += 1
    if (population[i % SQRT_POPULATION_SIZE][(j-1) % SQRT_POPULATION_SIZE] > 0):
        local_infected += 1
    if (population[(i+1) % SQRT_POPULATION_SIZE][(j-1) % SQRT_POPULATION_SIZE] > 0):
        local_infected += 1
    if (population[(i-1) % SQRT_POPULATION_SIZE][j % SQRT_POPULATION_SIZE] > 0):
        local_infected += 1
    if (population[(i+1) % SQRT_POPULATION_SIZE][j % SQRT_POPULATION_SIZE] > 0):
        local_infected += 1
    if (population[(i-1) % SQRT_POPULATION_SIZE][(j+1) % SQRT_POPULATION_SIZE] > 0):
        local_infected += 1
    if (population[i % SQRT_POPULATION_SIZE][(j+1) % SQRT_POPULATION_SIZE] > 0):
        local_infected += 1
    if (population[(i+1) % SQRT_POPULATION_SIZE][(j+1) % SQRT_POPULATION_SIZE] > 0):
        local_infected += 1
    return local_infected

def generateCoordinates(m, length):
  seen = set()
  x, y = randrange(m), randrange(m)
  i = 0
  while i < length:
    seen.add((x, y))
    x, y = randrange(m), randrange(m)
    while (x, y) in seen:
      x, y = randrange(m), randrange(m)
    i += 1
  return seen

# Initialize constants
WAS_INFECTED = -1
NOT_INFECTED = 0
GOT_INFECTED = 1

# Assume that infectivity is constant, in reality, it is best modeled by Gamma
INFECTIVITY = 0.5

# Assume the susceptivity response factors are normally distributed
GLOBAL_SUSCEPTIVITY_MEAN = 0.5
GLOBAL_SUSCEPTIVITY_STD = 0.5
LOCAL_SUSCEPTIVITY_MEAN = 0.5
LOCAL_SUSCEPTIVITY_STD = 0.5

TIME_OF_SICKNESS = 14
TOTAL_TIME_STEPS = 100

TOTAL_NEIGHBORS = 8
SQRT_POPULATION_SIZE = 100
INITIAL_INFECTED = 0.05

# Initialize a matrix and global values
population = np.zeros((SQRT_POPULATION_SIZE, SQRT_POPULATION_SIZE))
global_factors = np.zeros((SQRT_POPULATION_SIZE, SQRT_POPULATION_SIZE))
local_factors = np.zeros((SQRT_POPULATION_SIZE, SQRT_POPULATION_SIZE))

for i in range(SQRT_POPULATION_SIZE):
    for j in range(SQRT_POPULATION_SIZE):
        global_factors[i][j] = np.random.normal(GLOBAL_SUSCEPTIVITY_MEAN, GLOBAL_SUSCEPTIVITY_STD)
        local_factors[i][j] = np.random.normal(LOCAL_SUSCEPTIVITY_MEAN, LOCAL_SUSCEPTIVITY_STD)

total_infected = 0
current_active_infected = 0
total_infected_time = []
current_infected_time = []
time = 0


# Initialize the infected
coordinates = generateCoordinates(SQRT_POPULATION_SIZE, INITIAL_INFECTED*(SQRT_POPULATION_SIZE**2))
for coord in coordinates:
    population[coord[0]][coord[1]] = GOT_INFECTED
    total_infected += 1
    current_active_infected += 1
total_infected_time.append(total_infected)
current_infected_time.append(current_active_infected)

# Simulate
while (time < TOTAL_TIME_STEPS):
    print(time)
    for i in range(SQRT_POPULATION_SIZE):
        for j in range(SQRT_POPULATION_SIZE):
            #print(i)
            #print(j)

            # If infected, increase the duration of sickness
            if (population[i][j] > NOT_INFECTED):
                population[i][j] += 1

                # If duration of sickness exceeds the max time of sickness, change to WAS_INFECTED
                if (population[i][j] > TIME_OF_SICKNESS):
                    population[i][j] = WAS_INFECTED
                    current_active_infected -= 1

            # If not infected, check the neighbors' status and determine whether infected
            elif (population[i][j] == NOT_INFECTED):
                infected_neighbors = numberOfLocal(i, j)
                if (infected_neighbors > 0):
                    percent_local_infected = infected_neighbors / TOTAL_NEIGHBORS
                    percent_current_infected = current_active_infected / (SQRT_POPULATION_SIZE ** 2)

                    # We assume that the odds of susceptivity are exponentially distributed
                    susceptibility = 1 / (1 + np.exp(-1 * (percent_local_infected * local_factors[i][j] + percent_current_infected * global_factors[i][j])))
                    if (np.max(np.random.random(infected_neighbors)) < INFECTIVITY * susceptibility):
                        population[i][j] = GOT_INFECTED
                        total_infected += 1
                        current_active_infected += 1
    total_infected_time.append(total_infected)
    current_infected_time.append(current_active_infected)
    time += 1

time_list = [i for i in range(TOTAL_TIME_STEPS+1)]
plt.scatter(time_list, current_infected_time)
plt.scatter(time_list, total_infected_time)
plt.matshow(population, cmap=plt.cm.PuBu)
plt.show()