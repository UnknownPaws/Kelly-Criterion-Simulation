# Project Overview

This project involves a simulation of a series of gambling games with a focus on finding the optimal betting strategy based on the Kelly Criterion. The primary objective is to determine the fraction of the player's wealth to be bet in various game scenarios, ranging from 0% to 100% chance of winning and from 0% to 100% gain per bet.

## Key Features

Simulation of Various Gambling Scenarios: Games with varying probabilities of winning and different potential gains are simulated.  
Application of the Kelly Criterion: Utilizes this criterion to identify the optimal fraction of wealth to bet in each game scenario.  
Comprehensive Data Analysis: Includes an extensive analysis of the relationship between the fractional bet and median growth rate.  
Extensive Data Set: Simulates over 663 million games, each consisting of 12 rounds, to ensure robust results.  

## Technical Details

Simulation Rules  
Winning Chances: Set percent chance for the player to win each round.  
Winning Gains: Potential gain ranges from 0 to 100% per win.  
Betting Strategy: Players bet a fixed fraction of their total wealth, determined at the start and maintained throughout the game.  
Losses: All amounts bet are lost in the event of a loss.  

## Data Analysis

Optimal Fractional Bet: The simulation identifies the optimal fractional bet that leads to the highest growth rate.  
Strategic Insights: The simulation suggests not playing if odds of winning are below 50% and increasing bets with higher odds of winning.  
Exponential Growth Impact: Games with 100% chance of winning show significant exponential growth, influencing the optimal betting strategy.  
![left three dimensional scatter plot with simulated obtimal bet values and right is a surface plot of the same data](images/sim.jpg)  

## Validation

Mean Percent Error: The simulation demonstrated a mean percent error of 2.39%, validating its accuracy. The error percent per point is calculated using the [Kelly Bet Gambling Formula](https://en.wikipedia.org/wiki/Kelly_criterion) as expected value.  
Comparison of Calculated and Simulated Optimal Bets: Graphical representation shows close alignment between these values across different game scenarios.  
![three dimensional scatter plot of simulated and calculated optimal bet values with 2.39% as mean error percent](images/error.jpg)  

## How to Run the Simulation

Runs the simulation with a random seed and graphs the results (the seed used is shown in graph title).  
```python game_simulation.py```  
Runs the simulation with a chosen seed generating a predictable but random result.  
```python game_simulation.py -s SEED_NUMBER```  
Runs the validation of the simulation (simulation must've been run at least once).  
```python game_simulation.py -v```  

## Topics

Probability and statistics applications in gambling  
Computational simulations and data analysis  
Mathematical modeling using the Kelly Criterion  
