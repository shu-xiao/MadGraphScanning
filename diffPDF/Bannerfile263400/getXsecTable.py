#! /usr/bin/env python
#-------------------------------------------------------------
# File: getXsecTable.py
# Created: 15 July 2016 Fang-Ying Tsai
# Modified 15 Dec 2016 Shu-Xiao Liu
#-------------------------------------------------------------  
import glob
import errno
from ROOT import TGraph, TFile, TCanvas, TH2F, gStyle
from ROOT import TGraph2D, TGaxis
from array import array
import os
class GetValue():
    def __init__(self):
    	self.fileNum = []
    	self.zpMass = []
    	self.ma0Mass = []
    	self.mdmMass = []
    	self.weight = []
    	self.tanbeta = []

hAList = []
hApath = 'run_*.txt'  
hA_files = glob.glob(hApath) 

def getFile(fileName):
		num = str(fileName).split("_")[1].split(".")[0]
		global s
		s = GetValue()
		s.fileNum = int(num)
		return s

def getMZpValue(readLine):
	mzpValue = float(readLine.strip().split(' # ')[0].split('32 ')[1])
	return mzpValue

def getMA0Value(readLine):
	ma0Value = float(readLine.strip().split(' # ')[0].split('28 ')[1])
	return ma0Value

def getMDMValue(readLine):
	mdmValue = float(readLine.strip().split(' # ')[0].split('18 ')[1])
	return mdmValue

def getWeightValue(readLine):
	weightValue = float(readLine.split(' : ')[1])
	return weightValue	

def getTanBeta(readLine):
	tbValue  = float(readLine.split(' # ')[0].split()[1])
	return tbValue 

def gethAList(lhefile):
	for name in lhefile: 
		s = getFile(name)
	    	try:
	    	    with open(name) as f: 
	    	    	for lheFile in f:
	    	    		if lheFile.find('mzp') > 0 and lheFile.find('32') > 0:
	    	    			s.zpMass = getMZpValue(lheFile)
	    	    		elif lheFile.find('ma0') > 0 and lheFile.find('output') < 0:
	    	    			s.ma0Mass = getMA0Value(lheFile)
	    	    		elif lheFile.find('mx') > 0:
	    	    			s.mdmMass = getMDMValue(lheFile)
	    	    		elif lheFile.find('Integrated weight') > 0:
	    	    			s.weight = getWeightValue(lheFile)
	    	    		elif lheFile.find('tb') > 0 and lheFile.find('#') > 0:
	    	    			s.tanbeta = getTanBeta(lheFile)
					hAList.append(s)
	    	except IOError as exc:
	    	    if exc.errno != errno.EISDIR: 
	    	        raise 
	return hAList

def main():
	f = TFile("ScanXsec.root","recreate")
	c1 = TCanvas( 'c1', 'A Simple Graph', 200, 10, 700, 500 )
	c1.SetGrid(0)

	hAList = gethAList(hA_files)
        
        xmassP = array('d',[600.,800.,1000.,1200.,1400.,1700.,2000.,2500.,2750.,3000.,3500.,4000.])
        #yAxis = array('d',[300.,400.,500.,600.,700.,800.])
        xAxis = array('d',[500.,700.,900.,1100.,1300.,1550.,1750.,2250.,2600.,2900.,3200.,3750.,4200.])
        yAxis = array('d',[250.,350.,450.,550.,650.,750.,850.])
	histo_hA0 = TH2F('xsec1','Xsec(gz=0.8, tb=1.0) pdf setting 263400', len(xAxis)-1, xAxis, len(yAxis)-1, yAxis)
	histo_hA0.SetXTitle("M_{Zp} (GeV)")
	histo_hA0.SetYTitle("M_{A0} (GeV)")
	histo_hA0.SetStats(0)
	for a in hAList:
		histo_hA0.Fill(a.zpMass,a.ma0Mass,a.weight)
	gStyle.SetPalette(1)
        histo_hA0.SetNdivisions(520, "X")
        #for i in range(19):
            #a=0
            #histo_hA0.GetXaxis().ChangeLabel(i,)
        histo_hA0.GetXaxis().SetTickLength(0.)
        histo_hA0.GetYaxis().SetTickLength(0.)
        histo_hA0.GetXaxis().ChangeLabel(5,-1,-1,-1,-1,-1,"T")
        histo_hA0.GetXaxis().ChangeLabel(-1,45,-1,-1,-1,-1,"T")
        c1.Update()
	f.Write()
	f.Close()
	print 'path of root file'
        print os.getcwd()+'/*.root'
if __name__ == "__main__":
   main()
