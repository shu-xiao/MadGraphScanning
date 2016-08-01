#! /usr/bin/env python
#-------------------------------------------------------------
# File: scanParam.py
# Created: 12 July 2016 Fang-Ying Tsai
#-------------------------------------------------------------  

import sys
import os
import glob
import fileinput
import subprocess


fileName = 'param_card.dat'
paramCard = glob.glob(fileName)


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def replaceTb(searchExp,replaceExp):
    for line in fileinput.input(fileName, inplace=1):
        if line.lower().find('tb')>0:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

def replaceGz(searchExp,replaceExp):
    for line in fileinput.input(fileName, inplace=1):
        if line.lower().find('gz')>0:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)


def getA0AutoWidth():
    for line in fileinput.input(paramCard, inplace=1):
        if line.find("ECAY  28")>0:
            A0Width = line.split("28 ")[1].split(" #")[0]
            line = line.replace(A0Width,"Auto")
        sys.stdout.write(line)

def getZpAutoWidth():
    for line in fileinput.input(paramCard, inplace=1):
        if line.find("ECAY  32")>0:
            ZpWidth = line.split("32 ")[1].split(" #")[0]
            line = line.replace(ZpWidth,"Auto")
        sys.stdout.write(line)

def generateEvent():
    s = subprocess.Popen('./bin/generate_events -f', shell=True)
    s.wait()
    return s.returncode

def main():
    GzList=["8.000000e-01","4.000000e-01","6.000000e-01","8.000000e-01","1.000000e+00","1.200000e+00","1.400000e+00"]
    TbList=["1.000000e+00","4.000000e-01","7.000000e-01","1.300000e+00","1.600000e+00","1.900000e+00","2.200000e+00","2.500000e+00","2.800000e+00","1.000000e+00"] #the 1st and the lastest must be same
    for i in range(len(GzList)-1):
        replaceGz(GzList[i],GzList[i+1])
        for j in range(len(TbList)-1):
            getZpAutoWidth()
            getA0AutoWidth()
            replaceTb(TbList[j],TbList[j+1])
            with cd(".."):
                generateEvent()


if __name__ == "__main__":
   main()

