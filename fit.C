#include <TFile.h>
#include <TTree.h>
#include <TMacro.h>
#include <fstream>
#include <iostream>
using namespace std;

void fit() {
  // Input macro
  TFile *f = new TFile("Event.root");

  // take the tree from macro
  TTree *t = (TTree*)f->Get("tree"); 
  t->Draw("pt>>hpt");
  t->Draw("eta>>heta");
  TH1F *hpt = (TH1F*)gDirectory->Get("hpt");
  TH1F *heta = (TH1F*)gDirectory->Get("heta");

  // fitting
  TCanvas *c1 = new TCanvas("c1","eta & pt",800,1000);
  c1->Divide(1,2);
  c1->cd(1);
  heta->Fit("gaus");
  c1->cd(2);
  hpt->Fit("gaus");
  c1->cd();

  // output
  TFile* outFile = new TFile("eta&pt.root","RECREATE");
  c1->Write();
  outFile->Close();
}
