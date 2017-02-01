The code to gernerate tb and gz table just modifies Fang-Ying's code on [Twiki](https://twiki.cern.ch/twiki/bin/viewauth/CMS/InstructionOfGettingCrossSection).
After doing following command, you can see the figure like gzTbTable.pdf.
```
root -l gzTbTable.root
xsec1->Draw("textcolz")
```
To transform TH2F to CSV text file, use [ma0mzp/TH2FtoCSV.py](ma0mzp/TH2FtoCSV.py).
```python
python TH2FtoCSV.py yourRootFile
```
