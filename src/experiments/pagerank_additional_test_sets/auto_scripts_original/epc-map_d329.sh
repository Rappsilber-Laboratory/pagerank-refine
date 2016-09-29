#!/bin/bash
#$ -cwd
#$ -j y
#$ -S /bin/bash
######################
#set dir = $1
export LD_LIBRARY_PATH=/scratch/fkamm/local/lib:$LD_LIBRARY_PATH
export PYTHONPATH="${PYTHONPATH}:/scratch/fkamm/development:/scratch/fkamm/local/lib/python2.7/site-packages/gtk-2.5:/scratch/fkamm/local/lib/python2.7/site-packages/gtk-2.5/gio:/scratch/fkamm/local/lib/python2.7/site-packages/gtk-2.5/gtk"
source /home/schneider/.bashrc
cd /scratch/schneider/projects/pagerank_refinement/src/experiments/pagerank_additional_test_sets/auto_scripts_original/

#python ../compute_pagerank.py -t /scratch/schneider/projects/pagerank_refinement/data/predictor_results/d329/epc-map/ -a 0.35 -b 2.5 -l /scratch/schneider/projects/pagerank_refinement/data/predictor_results/d329/d329_lengths -s /scratch/schneider/projects/pagerank_refinement/data/predictor_results/d329/psipred/ -o /scratch/schneider/projects/pagerank_refinement/data/predictor_results/d329/epc-map/
python ../evaluate_predictions.py -t /scratch/schneider/projects/pagerank_refinement/data/predictor_results/d329/epc-map/ -a 0.35 -b 2.5 -p /scratch/schneider/projects/pagerank_refinement/data/predictor_results/d329/ -o /scratch/schneider/projects/pagerank_refinement/data/predictor_results/d329_epc-map_PR.txt -l /scratch/schneider/projects/pagerank_refinement/data/predictor_results/d329/d329_lengths
