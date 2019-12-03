DISCLAIMER: This repository is under development, with only some parts of
it fully working.


Description:

Suite of Python and MATLAB files for analysis and forecasting of catalan
and spanish elections. Automatically retrieves election results and polls
from the internet (with e.g. Pandas), combines them and performs predictions
on the expected evolution and number of sits each party will get. 

Different techniques are or will be implemented:

- Correcting for bias and scaling.
- Hidden Markov model (polls result/actual voting)
- Kalman filter (assuming a sort of Wiener process)
- Vector ARMA models.

Includes number of sits/province and d'Hondt's law, which is applied in 
Spain and Catalonia.
