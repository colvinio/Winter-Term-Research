# Winter-Term-Research
EXPLANATION OF PROJECT: Over my winter term in ‘23 at Oberlin College, I completed a similar project where looked to see if there were any differences in galaxy metallicity gradients between the DR17 and a former release, the DR15. We expected (and hoped!) to find that the two datasets were very similar, given the only differences were a larger amount of data in the DR17 and very small tweaks in metallicity calculation methods. Using MySQL, I accessed data calculated using 22 different metallicity calculation methods and used Python to calculate the 166,000 galaxy gradients. I graphed those gradients using Matplotlib. At the end of the winter term, we found that any differences between the two data releases were inconsequential, matching out hypothesis.


EXPLANATION OF PYTHON FILES IN FOLDER "Python files":
- dataFromSQL.py -- the file I used to download all of the relevant data from SQL

- fileWork.py -- a helper file where I stored helper functions to assist me in the other files where I needed to access data files

- getVertLimes.py -- file was used to calculate the maximum and minimum vertical bounds, to be used when graphing

- mathComp.py -- a file I used to check my math that I was doing on the data, to see if everything I was doing fit our expectations or not and to check that nothing was going wrong with my math

- plottingData -- the file where I made and saved all the graphs

- singleGalMathCheck.py -- a helper file where I stored helper functions to do with singular galaxies to be used in my mathComp.py file


EXPLANATION OF FIGURES: Each folder is for one type of metallicity calculation (for example, C17_N2_smc is the name of one way that metallicity in a galaxy can be calculated), and there are 3 figures in each folder. One is a comparison between the two data sets with the average gradient. The other two figures show the gradients for each galaxy in the DR17 and DR15 (the DR17 is a more more recent dataset and thus has more galaxies in it).
