import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import time # troubleshooting
sns.set_theme(style = 'ticks')

# helper function for search space strategy guesser
def search_space(lower_bound, upper_bound, focus_point):
    # take floored midpoint M of discretized closed interval [lower_bound, upper bound]
    # determine where M is relative to focus_point
    # return updated lower and upper bounds and M (as a tuple)
    M = (lower_bound + upper_bound)/2
    M = np.floor(M)
    if M < focus_point:
        new_lower_bound = M
        return new_lower_bound, upper_bound, M
    elif M > focus_point:
        new_upper_bound = M
        return lower_bound, new_upper_bound, M
    elif M == focus_point: # answer "guessed" correctly
        return lower_bound, upper_bound, M

# search space strategy guesser
def better_guess_numbers_game():
    # no input
    # simulate guess the numbers game with an actual strategy (not blind guessing) implemented
    answer = np.random.randint(1,101)
    initial_guess = np.random.randint(1,101)
    attempts = 0
    
    # define lower and upper bounds
    while True:
        # Case 1
        if initial_guess < answer:

            # start while loop
            current_guess = initial_guess
            while current_guess < answer:
                # update attempts
                attempts += 1

                # update new guess as midpoint between current guess and 100
                previous_guess = current_guess
                new_guess = (current_guess + 100)/2
                new_guess = np.floor(new_guess)
                current_guess = new_guess
        
            # check if current guess is answer before proceeding with search
            if current_guess == answer:
                return attempts
            # otherwise start by defining initial lower and upper bounds
            initial_lower_bound = previous_guess
            initial_upper_bound = current_guess
            break 
        # Case 2
        elif initial_guess > answer:
    
            # start while loop
            current_guess = initial_guess
            while current_guess > answer:
                # update attempts
                attempts += 1
        
                # update new guess as midpoint between current guess and 0
                previous_guess = current_guess
                new_guess = current_guess/2
                new_guess = np.floor(new_guess)
                current_guess = new_guess
        
            # check if current guess is answer before proceeding with search
            if current_guess == answer:
                return attempts
            # otherwise start by defining initial lower and upper bounds
            initial_lower_bound = current_guess
            initial_upper_bound = previous_guess
            break
        # Case 3
        elif initial_guess == answer:

            attempts = 1
            return attempts
        
    # search space until answer is "guessed" correctly
    current_lower_bound, current_upper_bound, current_guess = search_space(initial_lower_bound, initial_upper_bound, answer)

    # check whether the initial search gave a correct guess
    if current_guess == answer:
        attempts += 1
        return attempts
    # otherwise keep searching until answer is guessed correctly
    else:
        while current_guess != answer:
            # update attempts
            attempts += 1

            previous_lower_bound, previous_upper_bound, previous_guess = current_lower_bound, current_upper_bound, current_guess
            new_lower_bound, new_upper_bound, new_guess = search_space(current_lower_bound, current_upper_bound, answer)
            current_lower_bound, current_upper_bound, current_guess = new_lower_bound, new_upper_bound, new_guess
     
    return attempts
    
# simulate search space strategy guesser
# store attempt counts in a list
attempt_counts = []
for i in range(0,100):
    attempt_count = better_guess_numbers_game()
    attempt_count = int(attempt_count)
    print(f"Adding attempt count {i}")
    attempt_counts.append(attempt_count)
    
# plot attempt counts
f, ax = plt.subplots(figsize = (7,5))
sns.despine(f)
sns.histplot(attempt_counts, bins = 6, kde = True)
plt.xlabel('Number of attempts')
plt.ylabel('Frequency')
plt.title('Distribution of number of attempts to guess the correct number (search space guesser)')
plt.show()

# typically takes about 5 guesses to win w/ search space method
# need to fix the case where answer == 100
