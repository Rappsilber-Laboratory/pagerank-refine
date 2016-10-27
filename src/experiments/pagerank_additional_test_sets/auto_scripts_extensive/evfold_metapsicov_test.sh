#!/bin/bash
#$ -cwd
#$ -j y
#$ -S /bin/bash
######################
#set dir = $1
export LD_LIBRARY_PATH=/scratch/fkamm/local/lib:$LD_LIBRARY_PATH
export PYTHONPATH="${PYTHONPATH}:/scratch/fkamm/development:/scratch/fkamm/local/lib/python2.7/site-packages/gtk-3.0:/scratch/fkamm/local/lib/python2.7/site-packages/gtk-3.0/gio:/scratch/fkamm/local/lib/python2.7/site-packages/gtk-3.0/gtk"
source /home/schneider/.bashrc
cd /scratch/schneider/projects/pagerank_refinement/src/experiments/pagerank_additional_test_sets/auto_scripts/

python ../compute_pagerank.py -t /scratch/schneider/projects/pagerank_refinement/data/predictor_results/metapsicov_test/evfold/ -a 0.8 -b 3.0 -l /scratch/schneider/projects/pagerank_refinement/data/predictor_results/metapsicov_test/metapsicov_test_lengths -s /scratch/schneider/projects/pagerank_refinement/data/predictor_results/metapsicov_test/psipred/ -o /scratch/schneider/projects/pagerank_refinement/results/pagerank_auto_eval/metapsicov_test/evfold/
python ../evaluate_PR.py -t /scratch/schneider/projects/pagerank_refinement/results/pagerank_auto_eval/metapsicov_test/evfold/ -a 0.8 -b 3.0 -p /scratch/schneider/projects/pagerank_refinement/data/predictor_results/metapsicov_test/ -o /scratch/schneider/projects/pagerank_refinement/results/pagerank_auto_eval/metapsicov_test_evfold_PR.txt -l /scratch/schneider/projects/pagerank_refinement/data/predictor_results/metapsicov_test/metapsicov_test_lengths