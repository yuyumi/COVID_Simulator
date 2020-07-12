import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib import cm

WAS_INFECTED = -1
NOT_INFECTED = 0
GOT_INFECTED = 1

# Define necessary functions
def _local_infected(i, j, population, sqrt_population_size, total_neighbors):
    local_infected_array = []
    if (total_neighbors==8):
        if (population[(i-1) % sqrt_population_size][(j-1) % sqrt_population_size] > 0):
            local_infected_array.append(((i-1) % sqrt_population_size, (j-1) % sqrt_population_size))
        if (population[(i+1) % sqrt_population_size][(j-1) % sqrt_population_size] > 0):
            local_infected_array.append(((i+1) % sqrt_population_size, (j-1) % sqrt_population_size))
        if (population[(i-1) % sqrt_population_size][(j+1) % sqrt_population_size] > 0):
            local_infected_array.append(((i-1) % sqrt_population_size, (j+1) % sqrt_population_size))
        if (population[(i+1) % sqrt_population_size][(j+1) % sqrt_population_size] > 0):
            local_infected_array.append(((i+1) % sqrt_population_size, (j+1) % sqrt_population_size))
    if (population[i % sqrt_population_size][(j-1) % sqrt_population_size] > 0):
        local_infected_array.append((i % sqrt_population_size, (j-1) % sqrt_population_size))
    if (population[(i-1) % sqrt_population_size][j % sqrt_population_size] > 0):
        local_infected_array.append(((i-1) % sqrt_population_size, j % sqrt_population_size))
    if (population[(i+1) % sqrt_population_size][j % sqrt_population_size] > 0):
        local_infected_array.append(((i+1) % sqrt_population_size, j % sqrt_population_size))
    if (population[i % sqrt_population_size][(j+1) % sqrt_population_size] > 0):
        local_infected_array.append((i % sqrt_population_size, (j+1) % sqrt_population_size))
    return local_infected_array

# Generate 'length' distinct coordinates with each coordinate ranging from 0 to m
def generate_coordinates(m, length):
  seen = set()
  x, y = random.randrange(m), random.randrange(m)
  i = 0
  while i < length:
    seen.add((x, y))
    x, y = random.randrange(m), random.randrange(m)
    while (x, y) in seen:
      x, y = random.randrange(m), random.randrange(m)
    i += 1
  return seen

# Generate a gathering
_gathering_array = set()

def _gathering(case, m, length, p):
    global _gathering_array
    if (case==1):
        if not len(_gathering_array):
            _gathering_array = generate_coordinates(m, length)
        return _gathering_array
    elif (case==2):
        return generate_coordinates(m, length)
    elif (case==3):
        if (np.random.random < p):
            return generate_coordinates(m, length)
        else:
            return set()
    else:
        return set()

def _gathering_infected(g_set, population):
    infected = []
    global NOT_INFECTED
    for x in g_set:
        if (population[x[0]][x[1]] > NOT_INFECTED):
            infected.append(x)
    return infected

# Main function to simulate the infection spread
def simulate(case,
            sqrt_population_size=100, 
            time_of_sickness=1,
            total_time_steps=100,
            infectivity=1,
            global_susceptivity_mean=0.5, global_susceptivity_std=0, 
            local_susceptivity_mean=0.5, local_susceptivity_std=0,
            total_neighbors=8,
            initial_infected=0,
            gathering_size=100,
            gathering_probability=0.0,
            gathering_frequency=1,
            gathering_number=4):

    global WAS_INFECTED
    global NOT_INFECTED
    global GOT_INFECTED

    # Initialize a matrix and global values
    population = np.zeros((sqrt_population_size, sqrt_population_size))
    global_factors = np.zeros((sqrt_population_size, sqrt_population_size))
    local_factors = np.zeros((sqrt_population_size, sqrt_population_size))
    infected_by = [[(-1,-1) for i in range(sqrt_population_size)] for j in range(sqrt_population_size)]
    time_list = [i for i in range(total_time_steps+1)]

    for i in range(sqrt_population_size):
        for j in range(sqrt_population_size):
            # Assume the susceptivity response factors are normally distributed
            global_factors[i][j] = np.random.normal(global_susceptivity_mean, global_susceptivity_std)
            local_factors[i][j] = np.random.normal(local_susceptivity_mean, local_susceptivity_std)

    total_infected = 0
    current_active_infected = 0
    total_infected_time = []
    current_infected_time = []
    time = 0


    # Initialize the infected
    coordinates = generate_coordinates(sqrt_population_size, initial_infected*(sqrt_population_size**2))
    for coord in coordinates:
        population[coord[0]][coord[1]] = GOT_INFECTED
        total_infected += 1
        current_active_infected += 1
    total_infected_time.append(total_infected)
    current_infected_time.append(current_active_infected)

    # Simulate
    while (time < total_time_steps):
        #if (time % 200 == 0):
            #print(time)
        change_to_infected = []

        # Agents have a gathering at the start of each time step
        if (time % gathering_frequency == 0):
            g_set = _gathering(case, sqrt_population_size, gathering_size, gathering_probability)
            if not g_set:
                for ij in g_set:
                    if (population[ij[0]][ij[1]] > NOT_INFECTED):
                        population[ij[0]][ij[1]] += 1
                        # If duration of sickness exceeds the max time of sickness, change to WAS_INFECTED
                        if (population[i][j] > time_of_sickness):
                            population[i][j] = WAS_INFECTED
                            current_active_infected -= 1
                g_infected = _gathering_infected(g_set, population)
                for ij in g_set:
                    if (population[ij[0]][ij[1]] == NOT_INFECTED):
                        if (len(g_infected) > 0):
                            percent_local_infected = len(g_infected) / gathering_size
                            percent_current_infected = current_active_infected / (sqrt_population_size ** 2)

                            # We assume that the odds of susceptivity are exponentially distributed
                            susceptibility = 1 / (1 + np.exp(-1 * (percent_local_infected * local_factors[i][j] + percent_current_infected * global_factors[i][j])))
                            p_infected = np.random.random(len(g_infected))
                            infector = np.argmax(p_infected)
                            if (p_infected[infector] < infectivity * susceptibility):
                                change_to_infected.append((i,j))
                                infected_by[i][j] = g_infected[infector]
                                total_infected += 1
                                current_active_infected += 1


        for i in range(sqrt_population_size):
            for j in range(sqrt_population_size):
            
                # If infected, increase the duration of sickness
                if (population[i][j] > NOT_INFECTED):
                    if ((i,j) not in g_set):
                        population[i][j] += 1

                    # If duration of sickness exceeds the max time of sickness, change to WAS_INFECTED
                    if (population[i][j] > time_of_sickness):
                        population[i][j] = WAS_INFECTED
                        current_active_infected -= 1

        for i in range(sqrt_population_size):
            for j in range(sqrt_population_size):

                # If not infected, check the neighbors' status and determine whether infected
                if (population[i][j] == NOT_INFECTED):
                    infected_neighbors = _local_infected(i, j, population, sqrt_population_size, total_neighbors)
                    if (len(infected_neighbors) > 0):
                        percent_local_infected = len(infected_neighbors) / total_neighbors
                        percent_current_infected = current_active_infected / (sqrt_population_size ** 2)

                        # We assume that the odds of susceptivity are exponentially distributed
                        susceptibility = 1 / (1 + np.exp(-1 * (percent_local_infected * local_factors[i][j] + percent_current_infected * global_factors[i][j])))
                        p_infected = np.random.random(len(infected_neighbors))
                        infector = np.argmax(p_infected)
                        if (p_infected[infector] < infectivity * susceptibility):
                            change_to_infected.append((i,j))
                            infected_by[i][j] = infected_neighbors[infector]
                            total_infected += 1
                            current_active_infected += 1
        for xy in change_to_infected:
            population[xy[0]][xy[1]] = GOT_INFECTED
        total_infected_time.append(total_infected)
        current_infected_time.append(current_active_infected)
        time += 1
    return total_infected_time, current_infected_time, time_list, population

# Plot the simulation using the parameters
def plotSimulation(total_infected_time, current_infected_time, time_list, population):
    plt.scatter(time_list, current_infected_time)
    plt.scatter(time_list, total_infected_time)
    #plt.matshow(population, cmap=plt.cm.PuBu)
    plt.show()

# Simulate multiple runs
def simulate_multiple(epoches, case, infectivity=0.15, gathering_size=100):
    total_sum = np.array([])
    current_sum = np.array([])
    infected_maxes = []
    for k in range(epoches):
        total, current, time, population = simulate(case=case,
                                                sqrt_population_size=100, time_of_sickness=14,
                                                total_time_steps=400,
                                                infectivity=infectivity,
                                                global_susceptivity_mean=0.5, global_susceptivity_std=10,
                                                local_susceptivity_mean=0.5, local_susceptivity_std=10,
                                                initial_infected=0.05, 
                                                total_neighbors=4,
                                                gathering_size=gathering_size, gathering_probability=0.5,
                                                gathering_frequency=1, gathering_number=4)
        
        infected_maxes.append(np.argmax(total))
        
        if (len(total_sum) == 0):
            total_sum = np.array(total)
            current_sum = np.array(current)
        else:
            total_sum = np.array(total) + total_sum
            current_sum = np.array(current) + current_sum
    print("Summaries:")
    print(np.mean(infected_maxes))
    print(total_sum[-1]/epoches)
    return np.mean(infected_maxes), total_sum[-1]/epoches

# Vary the infectivity
def vary_infectivity(epoches, case=0):
    infectivity_array = [0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.8, 1]
    inf_max_arr = []
    inf_total_arr = []
    for value in infectivity_array:
        mx, tot= simulate_multiple(epoches, case=case, infectivity=value)
        inf_max_arr.append(mx)
        inf_total_arr.append(tot)

    plt.subplot(2, 1, 1)
    plt.scatter(infectivity_array, inf_max_arr)
    plt.title('Infectivity vs Duration and Total')
    plt.xlabel('Infectivity')
    plt.ylabel('Duration')

    plt.subplot(2, 1, 2)
    plt.scatter(infectivity_array, inf_total_arr)
    plt.xlabel('Infectivity')
    plt.ylabel('Total')  
    plt.show()

# Vary the gathering size
def vary_gathering_size(epoches, case=1):
    gathering_size_arr = [0, 100, 200, 500, 1000, 5000, 10000]
    inf_max_arr = []
    inf_total_arr = []
    for value in gathering_size_arr:
        mx, tot= simulate_multiple(epoches, case=case, gathering_size=value)
        inf_max_arr.append(mx)
        inf_total_arr.append(tot)

    plt.subplot(2, 1, 1)
    plt.scatter(gathering_size_arr, inf_max_arr)
    plt.title('Infectivity vs Duration and Total')
    plt.xlabel('Gathering Size')
    plt.ylabel('Duration')

    plt.subplot(2, 1, 2)
    plt.scatter(gathering_size_arr, inf_total_arr)
    plt.xlabel('Gathering Size')
    plt.ylabel('Total')  
    plt.show()

def main():
    epoches = 3
    random.seed(22)

    NO_GATHERING = 0
    SINGLE_REPEATED = 1
    MULTIPLE_REPEATED = 2
    MULTIPLE_RANDOM = 3

    # See how infectivity compares to pandemic duration and total number of cases
    # vary_infectivity(epoches)

    # See how gathering size compares to pandemic duration and total number of cases
    # at 1 gathering meeting at every 1 time step
    #vary_gathering_size(epoches)

    #simulate_multiple(epoches, case=NO_GATHERING)
    #simulate_multiple(epoches, case=SINGLE_REPEATED)
    #simulate_multiple(epoches, MULTIPLE_REPEATED)
    #simulate_multiple(epoches, MULTIPLE_RANDOM)
    
    #plotSimulation(total_infected_time=total_sum/epoches, current_infected_time=current_sum/epoches, time_list=time, population=population)

if __name__ == "__main__":
    main()