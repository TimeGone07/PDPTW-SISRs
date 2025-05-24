import math
class Parameters:
    randomSeed = 1
    avgCusRmved = 15  # bar c in 2020 T.S. Paper, indicate the avg number of customers removed
    maxStringLen = 20  # L_max in T.S. Paper, indicate the max length of a string
    itertimes=20000
    initial_temper=100
    final_temper=1
    c=math.pow(final_temper/initial_temper,itertimes)
    fleetminratio=0.20
    blinkrate=0.10