#!/usr/bin env python
#---------------------------------------------------------------
# File: diffCrossSection.py
# Created: 12 May 2017 Shu-Xiao Liu
#--------------------------------------------------------------

import csv
def getCSVcontent(fName, deli="\t"):
    data = []
    with open(fName,"r") as f:
        content = csv.reader(f, delimiter=deli)
        for row in content:
            data.append(row)
    return data
def diff(a=1.0,b=1.0):
    return (a-b)/b
def main():
    shuCrossSection = getCSVcontent("madGraph20170527.txt")
    samCrossSection = getCSVcontent("GatheredCrossSections_pdf263400_mFixedToMA.txt")
    
    compareResult = []
    # ["LHAID","mzp","ma","mhp","mh2","mDM","tanBeta","gZ" ,"Sigma[pb]"]
    #    0       1    2     3     4     5   --> int
    #                                float <--  6       7        8
    
    # transform the number from Samuel's text file
    for i in range(len(samCrossSection)):
        samCrossSection[i] = samCrossSection[i][0].split("     ")
        if ("pdf" in samCrossSection[i][0]): continue
        for j in range(len(samCrossSection[1])):
            if (j in range(5)): samCrossSection[i][j] = int(float(samCrossSection[i][j]))
            else: samCrossSection[i][j] = float(samCrossSection[i][j])
    
    # transform the number from ShuXiao's text file
    for i in range(len(shuCrossSection)):
        if ("LHAID" in shuCrossSection[i][0]): continue
        for j in range(len(shuCrossSection[1])):
            if (j in range(6)): shuCrossSection[i][j] = int(float(shuCrossSection[i][j]))
            else: shuCrossSection[i][j] = float(shuCrossSection[i][j])
    
    # compare 2 files
    for point in range(len(shuCrossSection)):
        for i in range(len(samCrossSection)):
            #print shuCrossSection[point][1], samCrossSection[point][1], "\t", shuCrossSection[point][2], samCrossSection[point][2]
            if (shuCrossSection[point][1] == samCrossSection[i][1] and shuCrossSection[point][2] == samCrossSection[i][2]):
                diffCrossSection = abs(diff(shuCrossSection[point][8],samCrossSection[i][7]))
                content = []
                content.append(shuCrossSection[point][1])
                content.append(shuCrossSection[point][2])
                content.append(format(shuCrossSection[point][8],".8f"))
                content.append(format(samCrossSection[i][7],".8f"))
                content.append(format(diffCrossSection,".8f"))
                compareResult.append(content)
    for i in range(len(compareResult)): 
        for j in range(len(compareResult[0])):
            print compareResult[i][j], "\t",
        print
    title=["MZp","MA0","shuxiaoResult","samuelResult","Difference"]
    with open("compareCrossSection.txt","w") as f:
        wr = csv.writer(f,delimiter="\t")
        wr.writerow(title)
        wr.writerows(compareResult)

if __name__ == "__main__":
    main()
