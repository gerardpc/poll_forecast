###########################################################################
# electoral_calculus.py
###########################################################################
# Electoral calculus library.
# Mostly designed for catalan and spanish elections, with plans to expand
# to further countries.
#
# Observations:
# Uses Python 3
###########################################################################
# GP Conangla, 06.2020
###########################################################################

import subprocess
import os
import pretty_errors
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
rcParams['text.usetex'] = True
rcParams['text.latex.preamble'] = [r'\usepackage[cm]{sfmath}']
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'cm'


# CLASS DEFINITIONS
# provincia
class provincia:
    def __init__(self, name, n_seats, district_id):
        self.name = name
        self.district_id = district_id
        self.n_seats = n_seats


# nice plot
def nice_plot(xx, yy, x_label, y_label, plot_title, device):
    # Initial checks/allocations
    # Check if folder where img is going to be exists
    if not os.path.exists(os.path.expanduser("~/home_status_web/plots")):
        # if not, create it
        os.makedirs(os.path.expanduser("~/home_status_web/plots"))
        print("Created /plots folder.")
    # Print information
    print("Plotting data from " + device)
    # Figure
    fig0, ax = plt.subplots()
    # Plot data
    ax.plot(xx, yy)
    # Add grid, labels, title, make pretty
    ax.grid(True)
    plt.xlabel(x_label, fontsize=18)
    plt.ylabel(y_label, fontsize=18)
    plt.title(plot_title, fontsize=18)
    ax.set_xlim([min(xx), max(xx)])
    delta_y = max(yy) - min(yy)
    ax.set_ylim([min(yy) - delta_y*0.5, max(yy) + delta_y*0.5])
    plt.ticklabel_format(style='plain', axis='x', scilimits=(0, 0))
    plt.ticklabel_format(style='plain', axis='y', scilimits=(0, 0))
    # Save plot as png
    fig0.savefig(os.path.expanduser("~/home_status_web/plots/" + device +
                                    ".svg"), format="svg")
    return


# import election results of a district from a .txt file in ./electoral_data
def import_votes_simple(provincia, year):
    d_frame = pd.read_csv(os.path.expanduser("~/poll_forecast/electoral_data/" +
                                          provincia.name + "_" + str(year) + ".txt"), header=None)
    # parties = ar_votes[:, 0]
    # num_votes = np.asarray(trace[:, 1])
    # print("Imported votes from " + provincia.name + ", year " + str(year))
    return d_frame


# import and join all electoral results from Catalunya
def import_votes_catalunya():
    return


# ar_votes = votes/(party*district),
#           matrix of size n_parties x m, where m = number of districts (v)
def filter_parties_threshold(threshold, n_parties, n_districts, ar_votes):
    total_votes_district = sum(ar_votes, axis=0)
    total_vd_expanded = np.matlib.repmat(total_votes_district, n_parties, 1)
    vote_fraction = ar_votes/total_vd_expanded
    ar_votes[vote_fraction < threshold] = 0
    return


# Calculate the d'Hondt table to distribute seats
def create_dhondt_table(n_parties, district_number, n_seats, ar_votes):
    district_votes = ar_votes[:, district_number]
    vots_1 = np.matlib.repmat(district_votes, 1, n_seats)
    dhondt_factor = np.matlib.repmat(np.linspace(1, n_seats, n_seats), n_parties, 1)
    dhondt_table = vots_1/dhondt_factor
    return dhondt_table


# Assign seats given a d'Hondt table
def assign_seats(n_parties, n_seats, dhondt_table):
    ar_seats = np.zeros(n_parties)
    for seat in range(1, n_seats):
        max_val = np.amax(dhondt_table)
        all_max_indices = np.argwhere(dhondt_table == max_val)
        sit_index = all_max_indices[0, :]
        dhondt_table[sit_index] = 0
        ar_seats[sit_index[0]] = ar_seats[sit_index[0]] + 1
    return


# n_parties = number of n_parties
# ar_votes = votes/(party*district),
#           matrix of size n_parties x m, where m = number of districts (v)
def seats_catalunya(n_parties, ar_votes):
    # initial defs.
    threshold = 0.03  # electoral threshold
    ar_votes_original = np.copy(ar_votes)
    import_votes_simple()
    filter_parties_threshold(threshold, n_parties, n_districts, ar_votes)
    dhondt_table = create_dhondt_table(n_parties, district_number, n_seats, ar_votes)
    assign_seats(n_parties, n_seats, dhondt_table)

    # define provincies
    p1 = provincia("barcelona", 1, 85)
    p2 = provincia("girona", 2, 17)
    p3 = provincia("tarragona", 3, 15)
    p4 = provincia("lleida", 4, 18)

    # Dibuixa els resultats en un grafic circular
    pie(v_diputats)
    return
