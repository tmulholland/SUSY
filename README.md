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