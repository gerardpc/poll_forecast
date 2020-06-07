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
import numpy.matlib
from matplotlib import rcParams
rcParams['text.usetex'] = True
rcParams['text.latex.preamble'] = [r'\usepackage[cm]{sfmath}']
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'cm'


# CLASS DEFINITIONS
# provincia
class provincia:
    def __init__(self, name, district_id, n_seats):
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
                                             provincia.name + "_" + str(year) + ".txt"))
    # parties = ar_votes[:, 0]
    # num_votes = np.asarray(trace[:, 1])
    # print("Imported votes from " + provincia.name + ", year " + str(year))
    return d_frame


# import and join all electoral results from Catalunya
def import_votes_catalunya():
    return


# merge more than 2 pandas dataframes by "key"
def merge_multiple_df(df_list, key):
    current_df = df_list[0]
    for i in range(0, len(df_list)-1):
        current_df = pd.merge(current_df, df_list[i+1], on=key)
    return current_df


# ar_votes = votes/(party*district),
#           matrix of size n_parties x m, where m = number of districts (v)
def filter_parties_threshold(threshold, ar_votes):
    n_parties = len(ar_votes)
    total_votes_district = np.sum(ar_votes, axis=0)
    total_vd_expanded = np.matlib.repmat(total_votes_district, n_parties, 1)
    vote_fraction = ar_votes/total_vd_expanded
    ar_votes[vote_fraction < threshold] = 0
    return


# Calculate the d'Hondt table to distribute seats
def create_dhondt_table(n_seats, provincia, ar_votes):
    n_parties = len(ar_votes)
    district_votes = ar_votes[:, provincia.district_id]
    district_votes.shape = (n_parties, 1)
    vots_1 = np.tile(district_votes, (1, n_seats))
    dhondt_factor = np.tile(np.linspace(1, n_seats, n_seats), (n_parties, 1))
    dhondt_table = vots_1/dhondt_factor
    return dhondt_table


# Assign seats given a d'Hondt table
def assign_seats(n_seats, dhondt_table):
    n_parties = len(dhondt_table)
    ar_seats = np.zeros(n_parties)
    for seat in range(0, n_seats):
        max_val = np.amax(dhondt_table)
        # print(max_val)
        max_indices = np.argwhere(dhondt_table == max_val)
        seat_index = max_indices[0]
        dhondt_table[seat_index[0], seat_index[1]] = 0
        ar_seats[seat_index[0]] = ar_seats[seat_index[0]] + 1
    return ar_seats


# n_parties = number of n_parties
# ar_votes = votes/(party*district),
#           matrix of size n_parties x m, where m = number of districts (v)
def seats_catalunya():
    # INITIAL DEFINITIONS
    # number of sits in parliament
    n_seats = 135
    # electoral threshold
    threshold = 0.03
    # define provincies
    p1 = provincia("barcelona", 0, 85)
    p2 = provincia("girona", 1, 17)
    p3 = provincia("tarragona", 2, 15)
    p4 = provincia("lleida", 3, 18)
    # import votes from txt file
    df_1 = import_votes_simple(p1, 2017)
    df_2 = import_votes_simple(p2, 2017)
    df_3 = import_votes_simple(p3, 2017)
    df_4 = import_votes_simple(p4, 2017)
    # merge vote dataframes
    df_all = merge_multiple_df([df_1, df_2, df_3, df_4], "party")
    # extract votes column as np array
    ar_votes = df_all.loc[:, df_all.columns != 'party'].to_numpy()

    # CALCULATE SEATS .to_numpy()
    filter_parties_threshold(threshold, ar_votes)
    dhondt_table = create_dhondt_table(n_seats, p2, ar_votes)
    ar_seats = assign_seats(p2.n_seats, dhondt_table)
    print(ar_seats)
    #
    # # Dibuixa els resultats en un grafic circular
    # pie(v_diputats)
    return
