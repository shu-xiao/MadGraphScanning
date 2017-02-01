#!/usr/bin/env python
import sys
import csv
from ROOT import TFile, TH2, TCanvas
def readRootFile():
    return  sys.argv[1]
def test_readhis(his,drawOption=''): 
    Canvas1 = TCanvas('','',800,600)
    his.Draw(drawOption)
    Canvas1.Print('test.pdf')
    return 'test import ROOT file'
def writetoCSV(fname, dataList, deli='\t'):
    with open(fname, 'wb') as f:
        wr = csv.writer(f, delimiter=deli)
        wr.writerows(dataList)
    return None
def
def main():
    Ma0List = [300,400,500,600,700,800]
    MzpList = [600,800,1000,1200,1400,1700,2000,2500]
    fname = readRootFile()
    print 'import ROOT file ' + fname
    f_root = TFile(fname)
    
    c1 = TCanvas('','',800,600)
    xsec1 = f_root.Get("xsec1")
    test_readhis(xsec1,'textcolz')  ## test

    print 'Ma0\tMzp\tCross-section'
    data = []
    data.append(['Ma0','Mzp','Cross-section'])
    
    for Ma0 in Ma0List:
        for Mzp in MzpList:
            xBin = xsec1.GetXaxis().FindBin(Mzp)
            yBin = xsec1.GetYaxis().FindBin(Ma0)
            crossSection = xsec1.GetBinContent(xBin,yBin)
            
            data.append([Ma0,Mzp,crossSection])
            print str(Ma0) + '\t' + str(Mzp) + '\t' + str(crossSection)
    csvfName = fname[0:len(fname)-len('.root')] + '.txt'       
    writetoCSV(csvfName,data)

if __name__ == "__main__":
    main()
