# script for testing

import electoral_calculus as ec

p1 = ec.provincia("barcelona", 1, 85)
p2 = ec.provincia("girona", 2, 17)
p3 = ec.provincia("tarragona", 3, 15)
p4 = ec.provincia("lleida", 4, 18)

d_frame = ec.import_votes_simple(p4, 2017)
print(d_frame)
