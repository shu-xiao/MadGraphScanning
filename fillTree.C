
// include all necessary files

#include <TTree.h>
#include <fstream>
#include <TFile.h>

using namespace std;

// in this example, the inputFileName = "test.dat"
void fillTree(std::string inputFileName)
{
  // read data from input files
  ifstream fin;
  fin.open(inputFileName.data());

  // assuming that there are two physical variables, pt and eta

  float pt=-999, eta=-999;
  TFile* hfile = new TFile("Event.root","RECREATE");
  
  TTree* tree = new TTree("tree","a tree that save two physical variables");
  // declare two branches that are float variables
  tree->Branch("pt",   &pt,  "pt/F");
  tree->Branch("eta", &eta, "eta/F");

  // start reading input files
  fin >> pt >> eta;
  while(!fin.eof()){

    tree->Fill();
    pt=-999; eta=-999;
    fin >> pt >> eta;
    
  }
  
  tree->Write();
  hfile->Close();
  


}
