#! /usr/bin/env python
#-------------------------------------------------------------
# File: genText.py
# Created: 12 May 2017 Shu-Xiao Liu
#-------------------------------------------------------------  
import glob
import errno
from ROOT import TGraph, TFile, TCanvas, TH2F, gStyle
from ROOT import TGraph2D, TGaxis
from array import array
import os
import csv
class GetValue():
    def __init__(self):
    	self.fileNum = []
    	self.zpMass = []
    	self.ma0Mass = []
    	self.mdmMass = []
    	self.weight = []
    	self.tanbeta = []

hAList = []
hApath = '../diffPDF/Bannerfile263400/*.txt'  
hApath2 = '../SamBannerfile3/*.txt'  
hA_files = glob.glob(hApath) 
hA_files2 = glob.glob(hApath2) 

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
        hAList = []
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

	hAList = gethAList(hA_files)
	hAList2 = gethAList(hA_files2)
        textLine = []
        title=["LHAID","mzp","ma","mhp","mh2","mDM","tanBeta","gZ" ,"Sigma[pb]"]
        xmassP = array('d',[600.,800.,1000.,1200.,1400.,1700.,2000.,2500.,2750.,3000.,3500.,4000.])
        #yAxis = array('d',[300.,400.,500.,600.,700.,800.])
        xAxis = array('d',[500.,700.,900.,1100.,1300.,1550.,1750.,2250.,2600.,2900.,3200.,3750.,4200.])
        yAxis = array('d',[250.,350.,450.,550.,650.,750.,850.])
        for a in hAList:
	    repeat = False
            for b in textLine:
                if (int(a.zpMass)==int(b[1]) and int(a.ma0Mass)==int(b[2])): repeat = True
            if (not repeat): textLine.append([263400, a.zpMass, a.ma0Mass, a.ma0Mass, a.ma0Mass, 100, a.tanbeta, 0.8, a.weight])
        for a in hAList2:
	    repeat = False
            for b in textLine:
                if (int(a.zpMass)==int(b[1]) and int(a.ma0Mass)==int(b[2])): repeat = True
            if (not repeat): textLine.append([263400, a.zpMass, a.ma0Mass, a.ma0Mass, a.ma0Mass, 100, a.tanbeta, 0.8, a.weight])
        textLine.sort()
        with open("madGraph20170527.txt", "w") as f:
            wr = csv.writer(f,delimiter="\t")
            wr.writerow(title)
            wr.writerows(textLine)

if __name__ == "__main__":
   main()
