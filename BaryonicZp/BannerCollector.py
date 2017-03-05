#!/usr/bin/env python
import sys
import glob
import csv
import operator
from ROOT import TFile, TH1F, TCanvas, gStyle

class GetValue():
    def __init__(self):
    	self.proc = []
    	self.zpMass = []
    	self.gq = []
    	self.mdmMass = []
    	self.weight = []
    	self.model = []

bannerList = []
bannerPath = 'ZpBaryonic_bb_bannerDir/*_banner.txt'
banner_files = glob.glob(bannerPath)

def getFile(fileName):
    model = str(fileName).split("/")[1].split("_")[0]
    proc = str(fileName).split("/")[1].split("_")[1]
    global s
    s = GetValue()
    s.model = model
    s.proc = proc
    return s

def getMZpValue(readLine):
    mzpValue = float(readLine.strip().split(' # ')[0].split('9000001 ')[1])
    return mzpValue

def getMDMValue(readLine):
    mdmValue = float(readLine.strip().split(' # ')[0].split('9000007 ')[1])
    return mdmValue

def getWeightValue(readLine):
    weightValue = float(readLine.split(' : ')[1])
    return weightValue	

def getGqValue(readLine):
    gqValue = float(readLine.split(' # ')[0].split(' 3 ')[1])
    return gqValue

def getBannerList(f_banner):
    for name in f_banner: 
        s = getFile(name)
    	try:
            with open(name) as f: 
	    	for line in f:
		    if line.find('mzp') > 0:
	    	    	s.zpMass = getMZpValue(line)
	    	    elif line.find('mdm') > 0:
	    	    	s.mdmMass = getMDMValue(line)
	    	    elif line.find('Integrated weight') > 0:
	    	    	s.weight = getWeightValue(line)
	    	    elif line.find('gq') > 0 and line.find('output') < 0:
                        s.gq = getGqValue(line)
		        bannerList.append(s)
	except IOError as exc:
      	    if exc.errno != errno.EISDIR: 
    	        raise 
    return bannerList
def main():
    ## write into text file
    bannerList = getBannerList(banner_files)
    sortList = sorted(bannerList, key=operator.attrgetter('gq','zpMass'))
    n = 1
    with open("ZpBaryonic_bb.txt","wb") as textfile:
        writer = csv.writer(textfile, delimiter='\t')
        writer.writerow(['gq','Mmed','cross-section'])
        for a in sortList:
            writer.writerow([format(a.gq,'.2f'),format(a.zpMass,'.0f'),a.weight])
            print format(a.gq,'.2f'),format(a.zpMass,'.0f'),a.weight, '\t', n
            n+=1
    ## draw as histogram
    rootfile = TFile("ScangqMmed.root","recreate")
    c1 = TCanvas('c1','',1600,1200) 
    h_gq = [TH1F(), TH1F(), TH1F()]
    for a in sortList:
        h_gq[int(a.gq//0.25-1)].Fill(a.zpMass,a.weight)
    for i in range(3):
        h_gq[i].SetXTitle("Mmed (GeV)")
        h_gq[i].SetYTitle("cross-section (pb)")
        h_gq[i].SetStats(0)
        h_gq[i].Draw("hist")
        h_gq[i].Write()
    gStyle.SetPalette(1)

    rootfile.Write()
    rootfile.Close()
    c1.Update()
if __name__ == "__main__":
    main()
