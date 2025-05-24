## PDPTW-SISRs

This repo provides a SISRs to solve PDPTW (Pickup and Delivery Problem with Time Windows),
which is NP-hard. We implement the SISRs (Slack Induction by String Removals) technique 
in Jan Christiaens, Greet Vanden Berghe (2020) Slack Induction by String Removals for 
Vehicle Routing Problems. Transportation Science, **which is proved to be a 
simple yet powerful heuristic for variants of VRP**. Experiments analysis can be found below.

## Numerical Experience

We provide a brief report of the numerical experiments. 
The results are obtained by running our code on instances provided by Carlo S. Sartori(Carlo S. Sartori, Luciana S. Buriol,
A study on the pickup and delivery problem with time windows: Matheuristics and new instances,
Computers & Operations Research). And the github is here(https://github.com/cssartori/pdptw-instances.git).

Column `Obj` indicates the objective value of our algorithm (which is measured by total distance),
`#.T` shows the number of vehicles used in our solution, `CPU(s)` denotes the CPU time in seconds, 
`Gap BKS(%)` is the gap to the Best-Known Solution (BKS), 
`BKS #.T` is the number of vehicles used in the BKS.

We may test our algorithm on more benchmarks in the future. 
As it's coded in pure Python, performance (running time) is somewhat terrible.
Total iteration Num is 20,000. Due to time limit, the table display the best solution of just one-run, but we may run more time
in the future.

|    Inst    |  Obj  | #.Truck | CPU (min) | Gap to BKS | BKS #. Trucks |
|:----------:|:-----:|:-------:|:---------:| :--------: | :-----------: |
| bar-n100-1 |  764  |    6    |   13.13   | 4.23 | 6 |
| bar-n100-2 |  588  |    5    |   10.35   | 6.14 | 5 |
| bar-n100-3 |  770  |    6    |   11.5    | 3.22 | 6 |
| bar-n100-4 | 1162  |   14    |   20.03   | 0.69 | 12 |
| bar-n100-5 |  863  |    6    |   11.21   | 2.98 | 6 |
| bar-n100-6 |  801  |    4    |   9.39    | 1.65 | 3 |
| ber-n100-1 | 1913  |   14    |   19.77   | 3.02 | 13 |
| ber-n100-2 | 1545  |    7    |   11.91   | 3.62 | 6 |
| ber-n100-3 |  714  |    3    |   6.87    | 0.14 | 3 |
| ber-n100-4 |  494  |    3    |   6.91    | 0.0 | 3 |
| ber-n100-5 |  959  |    5    |   8.81    | 1.59 | 5 |
| ber-n100-6 | 2152  |   15    |   18.42   | 0.23 | 14 |
| ber-n100-7 | 1948  |    7    |   10.79   | 0.67 | 7 |
| nyc-n100-1 |  644  |    6    |   10.59   | 1.58 | 6 |
| nyc-n100-2 |  586  |    4    |   9.21    | 3.35 | 4 |
| nyc-n100-3 |  461  |    4    |   9.31    | -6.3 | 3 |
| nyc-n100-4 |  558  |    3    |   8.57    | 4.3 | 2 |
| nyc-n100-5 |  653  |    3    |   9.13    | -2.68 | 2 |
| poa-n100-1 | 1605  |   13    |   16.28   | 1.01 | 12 |
| poa-n100-2 | 1599  |   16    |   19.08   | 3.9 | 15 |
| poa-n100-3 | 1285  |   12    |   15.89   | -1.23 | 10 |
| poa-n100-4 | 1544  |    9    |   12.55   | -7.43 | 7 |
| poa-n100-5 |  626  |    6    |   9.65    | 0.32 | 6 |
| poa-n100-6 |  572  |    3    |   6.57    | 1.78 | 3 |
| poa-n100-7 |  741  |    6    |   9.89    | -4.88 | 5 |
| **Total**  | 25547 |   180   |  295.81   |21.9|164|

It is normal that cause the first target is minimizing the number of vehicles, we find solutions with less objection in some instance.
For the 25 instance, we use 16 vehicles more than the BKS solutions, which means we use **no more than one vehicle** on average.

