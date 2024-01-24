import csv
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import floor, ceil
from sys import argv

# Usage: 
# python game_simulation.py                     Runs the simulation with a random seed and graphs the results
# python game_simulation.py -s SEED_NUMBER      Runs the simulation with a chosen seed generating a predictable but random result
# python game_simulation.py -v                  Runs the validation of the simulation (simulation must've been run at least once)
def main():
    seed = random.randint(0, 2**32 - 1)
    if len(argv) > 1 :
        # Use seed
        if argv[1] == "-s":   
            # Use command-line argument for seed; if no seed provided in cli then create a 32 bit integer seed for later reference
            seed = int(argv[2])
            random.seed(seed)
        # Run validation instead of simulation
        elif argv[1] == "-v":
            validate()
            return
        else:
            print("Invalid arguments")
            return
    # Run sim if seed is provided or no cl-args are provided
    sim_all(seed)
    

def sim_all(seed, ppa=50):
    # Matplotlib window setup
    fig = plt.figure(figsize=(15, 8))
    ax_scatter = fig.add_subplot(121, projection="3d")
    ax_surface = fig.add_subplot(122, projection="3d")
    
    # Based on the declared points per axis (ppa), create a list of equally spaced points between 0 and 1
    # This is used to be able to cover a large range of possibilities essentially covering every game scenario with a higher ppa
    step = int(100 / ppa)
    axis_points = list(range(0, 100+step, step))
    
    # Scatter plot coords
    pts_num = len(axis_points)
    x_odds, y_win, z_bet, col_growth = [], [], [], []
    
    # Surface plot requires 2d arrays for mesh
    x_odds_s = np.zeros((pts_num, pts_num))
    y_win_s = np.zeros((pts_num, pts_num))
    z_bet_s = np.zeros((pts_num, pts_num))
    
    # Go over each possible game scenario (i, j are just for counting steps for a loading bar)
    for i, odds in enumerate(axis_points):
        for j, win in enumerate(axis_points):
            # Loading bar is useful because the simulation can take 3+ hours to run
            print_progress(i * pts_num**2 + j * pts_num, pts_num**3 - pts_num)
            
            # For each game scenario this finds the fractional bet with the highest growth rate in a given game scenario to make sure only the 
            # optimal fractional bet is added per game scenario (i.e. there is one z-value per xy point)
            max_growth, best_bet = 0, 0
            for bet in axis_points:
                curr_growth = sim_point(odds, win, bet)
                if curr_growth > max_growth:
                    best_bet = bet
                    max_growth = curr_growth
            
            # Add scatter plot point
            x_odds.append(odds)
            y_win.append(win)
            z_bet.append(best_bet)
            col_growth.append(max_growth)
            
            # Add surface plot mesh
            x_odds_s[i, j] = odds
            y_win_s[i, j] = win
            z_bet_s[i, j] = best_bet
    
    # Scatter plot labels + colour bar key
    scatter = ax_scatter.scatter(x_odds, y_win, z_bet, c=col_growth, cmap="viridis")
    ax_scatter.set_title(f"Gambling Game Fairness Scatter ({seed})")
    ax_scatter.set_xlabel("Winning Odds %")
    ax_scatter.set_ylabel("Percent Gain from Win %")
    ax_scatter.set_zlabel("Optimal Fractional Bet %")
    growth_ckey = plt.colorbar(scatter, ax=ax_scatter)
    growth_ckey.set_label("Growth Factor %")
    
    # Surface plot labels
    ax_surface.plot_surface(x_odds_s, y_win_s, z_bet_s, cmap="jet")
    ax_surface.set_title(f"Gambling Game Fairness Surface ({seed})")
    ax_surface.set_xlabel("Winning Odds %")
    ax_surface.set_ylabel("Percent Gain from Win %")
    ax_surface.set_zlabel("Optimal Fractional Bet %")
    
    plt.show()
    
    # Create file to store the simualtion vairables to later validate the data
    with open("sim_results.csv", "w") as file:
        file.write("Winning Odds,Percent Gain from Win,Optimal Fractional Bet\n")
        for x, y, z in zip(x_odds, y_win, z_bet):
            file.write(f'{x},{y},{z}\n')
            
  
# A point constitutes of multiple games, where each game constitutes of multiple rounds, but not all points are plotted
def sim_point(odds, win, bet, games=5000):
    results = sorted([sim_game(odds, win, bet) for _ in range(games)])
    growth_median = (results[floor((len(results)-1) / 2)] + results[ceil((len(results)-1) / 2)]) / 2
    
    # Returning an average would cause lucky games to serve as outliers due to the exponential growth
    return growth_median


def sim_game(odds, win, bet, rounds=12):
    wealth = 100
    for _ in range(rounds):
        if wealth <= 0:
            return -100
        elif random.uniform(0, 100) <= odds:
            wealth += wealth * bet * win / 10_000
        else:
            wealth -= wealth * bet / 100
    
    # Returns growth rate for game as %
    return wealth - 100


def print_progress(steps_taken, total_steps):
    progress = steps_taken / total_steps * 100
    bar = ["=" if i <= progress else "-" for i in range(10, 110, 10)]
    print(f"<{''.join(bar)}> {progress:.2f}%")
    
    
def validate():
    # Matplotlib window setup
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection="3d")
    
    # Scatterplot points
    x, y, z_sim, z_real = [], [], [], []
    
    # Total mean percent error variables
    avg_error, num = 0, 0
    
    with open("sim_results.csv", mode='r') as file:
        reader = csv.reader(file)
        # Skip headers row
        next(reader)
        
        for row in reader:
            win = float(row[0]) / 100
            gain = float(row[1]) / 100
            sim_bet = float(row[2]) / 100
            
            num += 1
            kc_bet = 0
            # If statement to avoid dividing by 0
            if gain != 0:
                # Kelly's Criterion Formula
                kc_bet = win - ((1 - win) / gain)
                # Betting a negative fraction or more than one's whole wealth isn't possible so is is here to avoid that
                kc_bet = 0 if kc_bet < 0 else kc_bet
                kc_bet = 1 if kc_bet > 1 else kc_bet
                avg_error += abs(kc_bet - sim_bet)
            
            x.append(win)
            y.append(gain)
            z_sim.append(sim_bet)
            z_real.append(kc_bet)
        
        avg_error = avg_error * 100 / num
    
    # Plot and label graph with simulated and calculated optimal bets
    ax.scatter(x, y, z_sim, color="blue", label="Simulated Bet")
    ax.scatter(x, y, z_real, color="red", label="Calculated Bet")
    ax.set_title(f"Simulation Optimal Bet and Calculated Optimal bet ({avg_error:.2f}% Error)")
    ax.set_xlabel("Winning Odds %")
    ax.set_ylabel("Percent Gain from Win %")
    ax.set_zlabel("Optimal Fractional Bet %")
    
    plt.legend()
    plt.show()
    
    
main()