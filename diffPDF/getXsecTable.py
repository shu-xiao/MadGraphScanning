#! /usr/bin/env python
#-------------------------------------------------------------
# File: getXsecTable.py
# Created: 15 July 2016 Fang-Ying Tsai
# Modified 15 Dec 2016 Shu-Xiao Liu
#-------------------------------------------------------------  
import glob
import errno
from ROOT import TGraph, TFile, TCanvas, TH2F, gStyle
from ROOT import TGraph2D, TLatex, TBox, TPad, TPaveText
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
        self.rate = []

hApath30 = 'Bannerfile263000/run_*.txt'  
hApath34 = 'Bannerfile263400/run_*.txt'  
hA_files30 = glob.glob(hApath30) 
hA_files34 = glob.glob(hApath34) 

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
	f = TFile("ScanXsec.root","recreate")
	c1 = TCanvas( 'c1', 'A Simple Graph', 200, 10, 1600, 900 )
	c1.SetGrid(0,0)
        gStyle.SetPaintTextFormat(".2e")
        gStyle.SetOptStat(0)
	gStyle.SetMarkerSize(0.9)
        hAList30 = gethAList(hA_files30)
	hAList34 = gethAList(hA_files34)
        #xAxis1 = array('d',[600.,800.,1000.,1200.,1400.,1700.,2000.,2500.,2750.,3000.,3500.,4000.])
        #yAxis1 = array('d',[300.,400.,500.,600.,700.,800.])
        #xAxis2 = array('d',[500.,700.,900.,1100.,1300.,1550.,1750.,2250.,2600.,2900.,3200.,3750.,4200.])
        #yAxis2 = array('d',[250.,350.,450.,550.,650.,750.,850.])
	#histo_hA030 = TH2F('xsec1','Xsec(gz=0.8, tb=1.0) pdf setting 263000', len(xAxis)-1, xAxis, len(yAxis)-1, yAxis)
	#histo_hA034 = TH2F('xsec2','Xsec(gz=0.8, tb=1.0) pdf setting 263400/263000/diff', len(xAxis)-1, xAxis, len(yAxis)-1, yAxis)
	#histo_hA0Rate = TH2F('xsec3','Xsec(gz=0.8, tb=1.0) Rate', len(xAxis)-1, xAxis, len(yAxis)-1, yAxis)
	histo_hA030 = TH2F('xsec1','Xsec(gz=0.8, tb=1.0) pdf setting 263000',17,500,4100,6,250,850)
        histo_hA034 = TH2F('xsec2','Cross-Section (GZ=0.8, TB=1.0) with PDF Setting: 263400, 263000 and #DeltaCS',17,500,4100,6,250,850)
	histo_hA0Rate = TH2F('xsec3','Xsec(gz=0.8, tb=1.0) Rate',17,500,4100,6,250,850)

	histo_hA034.SetXTitle("M_{Zp} (GeV)")
	histo_hA034.SetYTitle("M_{A0} (GeV)")

	for a in hAList30:
	    histo_hA030.Fill(a.zpMass,a.ma0Mass,a.weight)
	    for b in hAList34:
                if (a.zpMass==b.zpMass and a.ma0Mass==b.ma0Mass):
	            histo_hA034.Fill(b.zpMass,b.ma0Mass,b.weight)
                    a.rate = a.weight/b.weight
                    b.rate = b.weight/a.weight
	            histo_hA0Rate.Fill(b.zpMass,b.ma0Mass,abs(b.rate-1))
                    #print b.zpMass, b.ma0Mass, b.weight, a.weight, "{:.2f}".format(abs(a.rate-1))
                    if abs(b.rate-1)>=0.07: print "problem"

        histo_hA034.SetBarOffset(0.2)
        histo_hA0Rate.SetBarOffset(-0.2)
        histo_hA034.GetYaxis().SetTickLength(0.)
	histo_hA034.Draw("colztext")
	histo_hA030.Draw("textsame")
	histo_hA0Rate.Draw("textsame")
        
        p = TPad("p","p",0.,0.,1.,1.)
        p.SetFillStyle(0)
        p.Draw("same")
        p.cd()
        pt1 = TPaveText(0.578,0.55,0.8,0.75)
        pt2 = TPaveText(0.795,0.55,0.897,0.75)
        pt1.SetTextSize(0.02)
        pt1.AddText("Each bin contains 3 values,")
        pt1.AddText("they are the cross-section (CS)")
        pt1.AddText("with pdf = 263400, 263000 and")
        pt1.AddText("the difference between 2 pdf settings,")
        pt1.AddText(" #DeltaCS = (CS_{263400} - CS_{263000})/CS_{263000}")
        pt2.SetTextSize(0.02)
        pt2.AddText("#scale[1.3]{CS_{263400}}")
        pt2.AddText("#scale[1.3]{CS_{263000}}")
        pt2.AddText("#scale[1.3]{#DeltaCS}")
        pt2.AddText("( 2% < #DeltaCS < 7.5% )")
        pt1.Draw()
        pt2.Draw()
        

	c1.SaveAs("pdfDiff.png")
	c1.Print("pdfDiff.pdf")
        f.Write()
	f.Close()
	c1.Update()

if __name__ == "__main__":
   main()
