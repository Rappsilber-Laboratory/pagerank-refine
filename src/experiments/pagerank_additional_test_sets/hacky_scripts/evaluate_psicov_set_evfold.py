import os 
import sys

from evaluation_helper import load_pdb_ids, evaluate_contact_file

def main():
    contact_script_folder="/scratch/schneider/Software/epc-map/rbocon/release/analysis/"
    test_set_folder="/scratch/kstahl/test_sets/psicovsupp/"
    protein_data = load_pdb_ids(test_set_folder + "psicov_lengths")

    os.chdir(contact_script_folder)    

    for pdb_id, length in protein_data:
        pdb_file = "".join([test_set_folder,
                             "pdb/",
                             pdb_id,
                             ".pdb"])

        contact_file= "".join(["/scratch/schneider/projects/pagerank_refinement/data/predictor_results/psicov/evfold/",
                             pdb_id,
                             ".prediction"])

        dom_ass = "1-%s" % length
        
        evaluate_contact_file(pdb_file, pdb_id, contact_file, length, dom_ass, "/scratch/schneider/projects/pagerank_refinement/src/experiments/pagerank_additional_test_sets/psicov_evfold_new.txt")

main()
