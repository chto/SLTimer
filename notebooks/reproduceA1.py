
# coding: utf-8

# # PyCS Tutorial
# 
# In this notebook we work through the `PyCS` "demo1" tutorial, to show how the `PyCS` package enables the estimation of a lens time delay from example light curve data. The original tutorial is in the form of a set of 6 scripts, that can be viewed on the `PyCS` website [here](http://pycs.readthedocs.io/en/latest/tutorial/demo1.html). The demo1 code itself can be browsed in the `PyCS` GitHub repository [here](https://github.com/COSMOGRAIL/PyCS/tree/master/demo/demo1).

# ## 1. Obtaining PyCS and its Sample Data 
# 
# The "demo1" tutorial uses a 4-image light curve dataset that comes with the `PyCS` repository. Let's download this and use `PyCS` to analyze it. If you haven't yet followed the [`SLTimer` installation instructions](https://github.com/DarkEnergyScienceCollaboration/SLTimer/blob/master/INSTALL.md) you should do that before attempting to `import pycs`. 

# In[ ]:

from __future__ import print_function
import os, urllib
import pycs
import numpy as np
import corner
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')

# We need to grab `rdbfile` (the demo1 dataset) from `webdir` (the appropriate `PyCS` GitHub folder). We only need to download `rdbfile` if it doesn't already exist.

# In[ ]:

webdir = 'https://raw.githubusercontent.com/COSMOGRAIL/PyCS/master/demo/demo1/data/'
rdbfile = 'trialcurves.txt'
    
url = os.path.join(webdir, rdbfile)
if not os.path.isfile(rdbfile):
    urllib.urlretrieve(url, rdbfile)
    

# ## 2. Displaying the Light Curve Data

# First lets read in the data from the rdbfile, in this case from a simple text file with a one-line header. (Other formats are supported as well.)

# In[ ]:

lcs = [
        pycs.gen.lc.rdbimport(rdbfile, 'A', 'mag_A', 'magerr_A', "Trial"),
        pycs.gen.lc.rdbimport(rdbfile, 'B', 'mag_B', 'magerr_B', "Trial"),
        pycs.gen.lc.rdbimport(rdbfile, 'C', 'mag_C', 'magerr_C', "Trial"),
        pycs.gen.lc.rdbimport(rdbfile, 'D', 'mag_D', 'magerr_D', "Trial")
]


# In[ ]:

pycs.gen.mrg.colourise(lcs) 


# In[ ]:


def spl(lcs):
   spline = pycs.spl.topopt.opt_rough(lcs, nit=5, knotstep=50,verbose=False,shifttime=False)
   spline = pycs.spl.topopt.opt_rough(lcs, nit=5, knotstep=30,verbose=False,shifttime=False)
   spline = pycs.spl.topopt.opt_fine(lcs, nit=10, knotstep=20,verbose=False,shifttime=False)
   return spline


# In[ ]:


ndim, nsamples = 3, 10000
sample=np.random.rand(ndim*nsamples).reshape(nsamples,ndim)*200-100



# In[ ]:

def getWeight(delay):
    for l in lcs:
        l.resetshifts()
        l.resetml()
    for index, l in enumerate(lcs):
        pycs.gen.splml.addtolc(l,knotstep=150)
        if index!=0:
            l.timeshift=delay[index-1]
    spline = spl(lcs)
    return spline.lastr2nostab


# In[ ]:

from multiprocessing import Pool
p = Pool(processes=7)
result=np.array(p.map(getWeight,sample))

np.save("sample-100-100.npy",sample)
np.save("chisquare-100-100.npy",result)
