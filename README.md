# SUSY

```python
from AnalysisTools import *

cutObj = Cuts()
chainObj = Chain()
histObj = Hist(chain)

cutList = cutObj.getBinningCuts()
hist = histObj.getHistFromList(cutList)

hist.Draw('ep')

```