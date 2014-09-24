import os 
import git_tag

file = open("../../data/datasets/ciss_set.txt")

#alphas = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]
#lens = [1,1.5,2]
lens = [2.0]
alphas = [0.4]
if os.path.exists("../../results/29-08-14/%s/"%git_tag.get_branch()):
    pass
else:
    os.mkdir("../../results/29-08-14/%s/"%git_tag.get_branch())
for line in file:
    strline = str(line).strip().split()
    pdb = strline[0]
    l = strline[1]
    for t in lens:
        for a in alphas:
            print strline
            cmd = " ".join(["/scratch/fkamm/local/bin/python2.7",
                            "../contact_page_rank.py",
                            "-c /scratch/schneider/results/graph_kernel_svm/bin_features/psicov_1/gamma_0.001/mi_mid_test/filtered_results/verify_test/%sRRNone_1"%(pdb),
                            #"-c ../../../rbocon_2.0/results/phy_cm_results/%sRRPCM_1"%(pdb), 
                            "-l %s"%l,
                            "-p %s"%pdb,
                            "-f /scratch/schneider/pdb_select_dataset/%s/%s.pdb"%(pdb[0:4],pdb),
                            "-s /scratch/schneider/projects/rbocon_2.0/data/rbo_test/sec_struct/%s.psipred"%pdb,
                            "-t %s"%t,
                            "-a %s"%a,
                            "-o ../../results/29-08-14/%s/"%git_tag.get_branch()])

            os.system(cmd)
    #break
file.close()
