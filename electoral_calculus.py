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

import os
import pretty_errors
import pandas as pd
# to check: https://geopandas.org/
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


# nice standard XY plot
def nice_plot(xx, yy, x_label, y_label, plot_title, device):
    # Initial checks/allocations
    # Check if folder where img is going to be exists
    if not os.path.exists(os.path.expanduser("~/poll_forecast/plots")):
        # if not, create it
        os.makedirs(os.path.expanduser("~/poll_forecast/plots"))
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
    # Show plot
    plt.show()
    # Save plot
    fig0.savefig(os.path.expanduser("~/poll_forecast/plots/" + device +
                                    ".svg"), format="svg")
    return


# Party color definitions
def party_color(parties):
    dict_color_party = {
        "C's": "orangered",
        "ERC": "orange",
        "JUNTSxCAT": "darkblue",
        "PSOE": "red",
        "CatComú-Podem": "violet",
        "CUP": "yellow",
        "PP": "deepskyblue",
        "PACMA": "yellowgreen",
        "RECORTES CERO-ELS VERDS": "forestgreen",
        "Por un Mundo más Justo": "grey"
    }
    return dict_color_party


# Custom function to plot parliament charts
def parliament_chart(parties, seats, plot_title):
    # Initial checks/allocations
    # Check if folder where img is going to be exists
    if not os.path.exists(os.path.expanduser("~/poll_forecast/plots")):
        # if not, create it
        os.makedirs(os.path.expanduser("~/poll_forecast/plots"))
        print("Created /plots folder.")
    # delete parties with zero seats from plot
    total_seats = sum(seats)
    index_zero = np.argwhere(seats < 1)
    parties = np.delete(parties, index_zero)
    seats = np.delete(seats, index_zero)
    # rescale seats to reduce the pie to parliament size (i.e. half pie)
    seats = seats/(2*total_seats)
    # Figure
    fig0, ax = plt.subplots()
    plt.title(plot_title, fontsize=18)
    # Get party colors
    dict_color = party_color(parties)
    color_pie = [dict_color.get(key) for key in parties]
    # Plot
    plt.pie(seats, counterclock=False, labels=parties, colors=color_pie, autopct=lambda p: '{:.0f}'.format(p*2*total_seats/100),
            wedgeprops=dict(width=0.7), shadow=False, startangle=180)
    plt.axis('equal')
    # Show plot
    plt.show()
    # Save plot
    fig0.savefig(os.path.expanduser("~/poll_forecast/plots/fig0.svg"), format="svg")
    return


# import election results of district from a .txt file in ./electoral_data
def import_votes_simple(provincia, year):
    d_frame = pd.read_csv(os.path.expanduser("~/poll_forecast/electoral_data/" +
                                             provincia.name + "_" + str(year) + ".txt"))
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


# filter parties below threshold (i.e. they get no seats)
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
    # electoral threshold (below this % you get no seats)
    threshold = 0.03
    # define provincies
    p1 = provincia("barcelona", 0, 85)
    p2 = provincia("girona", 1, 17)
    p3 = provincia("lleida", 2, 15)
    p4 = provincia("tarragona", 3, 18)
    prov_list = [p1, p2, p3, p4]

    # IMPORT VOTES
    # get data from txt file
    df_1 = import_votes_simple(p1, 2017)
    df_2 = import_votes_simple(p2, 2017)
    df_3 = import_votes_simple(p3, 2017)
    df_4 = import_votes_simple(p4, 2017)
    # merge vote dataframes
    df_all = merge_multiple_df([df_1, df_2, df_3, df_4], "party")
    # extract votes column as np array
    ar_votes = df_all.loc[:, df_all.columns != 'party'].to_numpy()
    n_parties = len(ar_votes)
    df_parties = df_all.loc[:, df_all.columns == 'party'].values

    # CALCULATE SEATS
    filter_parties_threshold(threshold, ar_votes)
    total_seats = np.zeros(n_parties)
    for p_i in prov_list:
        dhondt_table = create_dhondt_table(n_seats, p_i, ar_votes)
        ar_seats = assign_seats(p_i.n_seats, dhondt_table)
        total_seats = total_seats + ar_seats

    # PLOT RESULTS
    # In parliament chart
    parliament_chart(df_parties, total_seats, "Eleccions parlament 2017")
    return
