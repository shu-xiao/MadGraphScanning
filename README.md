## Compare Different PDF Setting
CMS people use 263400 PDF setting
ATLAS people use 263000 PDF setting and 5 flavors which includes b quarks and sets mb=0
Default setting: 4 flavors, dynamic scale, using default fixed value

---

| Directory  Name |                              comparison                                    |
| :-------------- | :------------------------------------------------------------------------: |
|     5flavor     |                   compare CMS and ATLAS pdf setting                        |
| 5flavorAndScale |     compare CMS setting and 5 flavors + fixed scale (fixed value = MZp)    |
|     diffPDF     |           compare different PDF setting, pdf = 263000, 263400              |
|      runOpt     | compare different PDF setting with fixed scale (using default fixed value) |
| fixAndDyn263400 |   pdf=263400, compare fixed scale (fixed value = MZp) and dynamic scale    |
| fixAndDyn263000 |   pdf=263000, compare fixed scale (fixed value = MZp) and dynamic scale    |

---
## TbGz Distribution
The code to gernerate tb and gz distribution was modified by Fang-Ying's code on [Twiki](https://twiki.cern.ch/twiki/bin/viewauth/CMS/InstructionOfGettingCrossSection).
After doing following command, you can see the figure in gzTbTable.pdf.
```
root -l gzTbTable.root
xsec1->Draw("textcolz")
```
To transform TH2F to CSV text file, use [ma0mzp/TH2FtoCSV.py](ma0mzp/TH2FtoCSV.py).
```python
python TH2FtoCSV.py yourRootFile
```
