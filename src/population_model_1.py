import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


def deriv(y, t, N, beta, gamma):
    # The SIR model differential equations.
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I

    return dSdt, dIdt, dRdt


def plot(t, S, I, R):
    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
    ax.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='Susceptible')
    ax.plot(t, I/1000, 'r', alpha=0.5, lw=2, label='Infected')
    ax.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
    ax.set_xlabel('Time /days')
    ax.set_ylabel('Number (1000s)')
    ax.set_ylim(0,1.2)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    plt.show()

    return


# Model parameters
N = 1000 # Total population, N.
I0 = 1 # Total number of infected individuals
R0 = 0 # Total number of recovered individuals
beta = 0.2 # Contact rate
gamma = 1 / 10  # Mean revovery rate (1 / days)
d = 200 # Number of simulation days

# Everyone else, S0, is susceptible to infection initially.
S0 = N - I0 - R0

# A grid of time points (in days)
t = np.linspace(0, d, d)

# Initial conditions vector
y0 = S0, I0, R0

# Integrate the SIR equations over the time grid, t.
results = odeint(deriv, y0, t, args=(N, beta, gamma))
S, I, R = results.T

# Plot results
plot(t, S, I, R)
