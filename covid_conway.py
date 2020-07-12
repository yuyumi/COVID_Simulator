from simulator import *

# Plot the simulation using the parameters
def plot_simulation(total_infected_time, new_case_infected_time, time_list, population=None):
    plt.subplot(2, 1, 1)
    plt.scatter(time_list[:-1], new_case_infected_time)
    plt.title('Time vs Cases')
    plt.xlabel('Time')
    plt.ylabel('New Cases')

    plt.subplot(2, 1, 2)
    plt.scatter(time_list, total_infected_time)
    plt.xlabel('Time')
    plt.ylabel('Total Cases')
    #plt.matshow(population, cmap=plt.cm.PuBu)
    plt.show()

# Simulate multiple runs
def simulate_multiple(epoches, case=0, attack_rate=0.1, gathering_size=100, return_value=0):
    total_sum = np.array([])
    current_sum = np.array([])
    new_case_sum = np.array([])
    infected_maxes = []
    peak_indicies = []
    peaks = []
    for k in range(epoches):
        total, current, new_cases, time, population = simulate(case=case,
                                                sqrt_population_size=100, time_of_sickness=14,
                                                total_time_steps=300,
                                                attack_rate=attack_rate,
                                                global_susceptivity_mean=0, global_susceptivity_std=0,
                                                local_susceptivity_mean=0, local_susceptivity_std=0,
                                                initial_infected=0.002, 
                                                total_neighbors=4,
                                                gathering_size=gathering_size, gathering_probability=0.5,
                                                gathering_frequency=1, gathering_number=4)
        
        infected_maxes.append(np.argmax(total))
        peak_indicies.append(np.argmax(new_cases))
        peaks.append(max(new_cases))
        
        if (len(total_sum) == 0):
            total_sum = np.array(total)
            current_sum = np.array(current)
            new_case_sum = np.array(new_cases)
        else:
            total_sum = np.array(total) + total_sum
            current_sum = np.array(current) + current_sum
            new_case_sum = np.array(new_cases) + new_case_sum
    if (return_value==0):
        print("Summaries:")
        print(np.mean(infected_maxes))
        print(total_sum[-1]/epoches)
        return np.mean(infected_maxes), total_sum[-1]/epoches, np.mean(peaks), np.mean(peak_indicies)
    elif (return_value==1):
        print("Done")
        print(np.mean(peak_indicies))
        print(np.mean(peaks))
        return total_sum/epoches, new_case_sum/epoches, time
    return

# Vary the attack_rate
def vary_attack_rate(epoches, case=0):
    attack_rate_array = [0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.5, 0.8, 1]
    # attack_rate_array = [0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.8, 1]
    inf_max_arr = []
    inf_total_arr = []
    inf_peak_time_arr = []
    inf_peak_cases_arr = []
    for value in attack_rate_array:
        mx, tot, pk, pki = simulate_multiple(epoches, case=case, attack_rate=value)
        inf_max_arr.append(mx)
        inf_total_arr.append(tot)
        inf_peak_time_arr.append(pki)
        inf_peak_cases_arr.append(pk)

    plt.subplot(4, 1, 1)
    plt.scatter(attack_rate_array, inf_max_arr)
    plt.title('Attack Rate vs Duration and Total')
    plt.xlabel('Attack Rate')
    plt.ylabel('Duration')

    plt.subplot(4, 1, 2)
    plt.scatter(attack_rate_array, inf_total_arr)
    plt.xlabel('Attack Rate')
    plt.ylabel('Total')  

    plt.subplot(4, 1, 3)
    plt.scatter(attack_rate_array, inf_peak_time_arr)
    plt.xlabel('Attack Rate')
    plt.ylabel('Peak Times')

    plt.subplot(4, 1, 4)
    plt.scatter(attack_rate_array, inf_peak_cases_arr)
    plt.xlabel('Attack Rate')
    plt.ylabel('Peak Cases')
    plt.show()

# Vary the gathering size
########################
#
#
# TODO: Fix current cases to new cases
#
#
########################
def vary_gathering_size(epoches, case=1):
    gathering_size_arr = [0, 100, 200, 500, 1000, 5000, 10000]
    # inf_max_arr = []
    # inf_total_arr = []
    for value in gathering_size_arr:
        # mx, tot = simulate_multiple(epoches, case=case, gathering_size=value)
        total, current, time = simulate_multiple(epoches, case=case, gathering_size=value, return_value=1)
        plt.scatter(time, current)
        # inf_max_arr.append(mx)
        # inf_total_arr.append(tot)
    plt.show()

    # plt.subplot(2, 1, 1)
    # plt.scatter(gathering_size_arr, inf_max_arr)
    # plt.title('attack_rate vs Duration and Total')
    # plt.xlabel('Gathering Size')
    # plt.ylabel('Duration')

    # plt.subplot(2, 1, 2)
    # plt.scatter(gathering_size_arr, inf_total_arr)
    # plt.xlabel('Gathering Size')
    # plt.ylabel('Total')  
    # plt.show()

def main():
    epoches = 5
    random.seed(22)

    NO_GATHERING = 0
    SINGLE_REPEATED = 1
    MULTIPLE_REPEATED = 2
    MULTIPLE_RANDOM = 3

    # See how attack_rate compares to pandemic duration and total number of cases
    vary_attack_rate(epoches)

    # See how gathering size compares to pandemic duration and total number of cases
    # at 1 gathering meeting at every 1 time step
    #vary_gathering_size(epoches)

    # total, new_case, time = simulate_multiple(epoches, case=NO_GATHERING, attack_rate=0.1, return_value=1)
    # plot_simulation(total_infected_time=total, new_case_infected_time=new_case, time_list=time)

    #simulate_multiple(epoches, case=NO_GATHERING)
    #simulate_multiple(epoches, case=SINGLE_REPEATED)
    #simulate_multiple(epoches, MULTIPLE_REPEATED)
    #simulate_multiple(epoches, MULTIPLE_RANDOM)
    
    #plotSimulation(total_infected_time=total_sum/epoches, current_infected_time=current_sum/epoches, time_list=time, population=population)

if __name__ == "__main__":
    main()