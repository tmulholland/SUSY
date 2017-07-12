import ROOT
import numpy as np

class Cuts(object):

    ## default constructor
    def __init__(self, sample='ZJetsToNuNu'):

        self.doLumi = 35.9

        self.removeKfactor = False
        if 'ZJetsToNuNu' in sample or 'DYJets' in sample:
            self.removeKfactor = True

        ## baseline selection
        self.baseCuts = ROOT.TCut("")

        self.baseCuts+='NJets>=2'
        self.baseCuts+='HT>=300'
        self.baseCuts+='MHT>=300'
            
        ## dictionaries define binning selection
        self.NjetCuts = {
            1: "NJets==2",
            2: "NJets>=3 && NJets<=4",
            3: "NJets>=5 && NJets<=6",
            4: "NJets>=7 && NJets<=8",
            5: "NJets>=9",
        }
        self.NbjetCuts = {
            0:  'BTags==0',
            1:  'BTags==1',
            2:  'BTags==2',
            3:  'BTags>=3',
        }
        self.kinCuts = {
            1:  "HT>=300  && HT<500  && MHT>=300  && MHT<350",
            2:  "HT>=500  && HT<1000 && MHT>=300  && MHT<350",
            3:  "HT>=1000 &&            MHT>=300  && MHT<350",
            4:  "HT>=350  && HT<500  && MHT>=350  && MHT<500",
            5:  "HT>=500  && HT<1000 && MHT>=350  && MHT<500",
            6:  "HT>=1000 &&            MHT>=350  && MHT<500",
            7:  "HT>=500  && HT<1000 && MHT>=500  && MHT<750",
            8:  "HT>=1000 &&            MHT>=500  && MHT<750",
            9:  "HT>=750  && HT<1500 && MHT>=750",
            10: "HT>=1500 &&            MHT>=750",
        }

        ## Removed bins [njet, nb, kin]
        self.removedBins  = [[1, 3, kin] for kin in self.kinCuts] # NJ>NB
        self.removedBins += [[4, nb, 1] for nb in self.NbjetCuts] # NJ:7-8
        self.removedBins += [[4, nb, 4] for nb in self.NbjetCuts] # NJ:7-8
        self.removedBins += [[5, nb, 1] for nb in self.NbjetCuts] # NJ>=9
        self.removedBins += [[5, nb, 4] for nb in self.NbjetCuts] # NJ>=9



    def getBaselineCuts(self, extraCuts=''):
        """ Add extraCuts=cutString to return baseline with 
        additional cuts applied. E.g.:
        getBaselineCuts('BTags>=1')
        returns TCut
        """

        baseline = self.baseCuts
        baseline+=extraCuts

        return baseline

    def getWeight(self, PU=False):

        weight = str(self.doLumi)+'*Weight'

        return weight

    def getBinningCuts(self,):
        """ Returns list of TCuts corresponding to your binning """

        cutList = []

        ## loop over bins adding bin cuts to array
        for nj in self.NjetCuts:
            for nb in self.NbjetCuts:
                for kin in self.kinCuts:

                    ## skip removed bins
                    if [nj, nb, kin] in self.removedBins:
                        continue

                    binCuts =  ROOT.TCut(self.NjetCuts[nj])
                    binCuts += ROOT.TCut(self.NbjetCuts[nb])
                    binCuts += ROOT.TCut(self.kinCuts[kin])
                    cutList.append(self.baseCuts+binCuts)

        return cutList
                    

class Chain(object):

    ## default constructor 
    def __init__(self, sample='ZJetsToNuNu', dphi='signal'):

        ## decide which dphi skims to use
        if 'signal' in dphi.lower():
            self.prefix = ['/tree_signal/']
        elif 'ldp' in dphi.lower():
            self.prefix = ['/tree_LDP/']
        else:
            self.prefix = ['/tree_signal/','/tree_LDP/']


        ## strip sample files from file list
        self.files = [f for f in 
                      np.genfromtxt('files.txt', delimiter='',dtype='str')
                      if sample in f]

        self.treeLoc = "/nfs/data38/cms/mulholland/lpcTrees/Skims/Run2ProductionV12/"
        self.treeName = "tree"

    def getChain(self,):
        """ returns a chain of ttrees from RA2b skims"""

        chain = ROOT.TChain(self.treeName)

        for f in self.files:
            for pref in self.prefix:
                chain.Add(self.treeLoc+pref+f)
        
        return chain

class Hist(object):

    def __init__(self,chain):

        self.chain = chain
        
    def getHistFromList(self, cutList):
        
        nBins = len(cutList)

        histlabel = "hist"    
        hIter = 1
        while(type(ROOT.gROOT.FindObject(histlabel+"_"+str(hIter)))==ROOT.TH1D):
            hIter+=1
        
        histlabel+="_"+str(hIter)
  

        EventCount = ROOT.TH1D('ec'+histlabel,'ec'+histlabel,1,-1,1000)
        hist = ROOT.TH1D(histlabel,histlabel,nBins,0.5,0.5+nBins)

        Bin = 1
        for cut in cutList:

            self.chain.Project('ec'+histlabel,"nAllVertices",str(cut))

            hist.Fill(Bin, EventCount.GetBinContent(1))
            hist.SetBinError(Bin, EventCount.GetBinError(1))
            Bin+=1


        return hist
