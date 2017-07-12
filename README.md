# SUSY

```python
from AnalysisTools import *

cutObj = Cuts()
cutList = cutObj.getBinningCuts()

chainObj = Chain()
chain = chainObj.getChain()

histObj = Hist(chain)
hist = histObj.getHistFromList(cutList)

hist.Draw('ep')

```

![plot](http://www-hep.colorado.edu/~mulholland/plot1.png " ")


# To Do List
* Double ratio plots with uncertainties
* Z mass fit with purity
* Extrapolation?