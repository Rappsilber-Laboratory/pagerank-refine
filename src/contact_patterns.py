"""Author: Michael Schneider
""" 
import os 
import sys 
import random
sys.path.append("../src")
sys.path.append("/scratch/schneider/libs/lib/python2.7/site-packages")
sys.path.append("/scratch/schneider/projects/contact_prediction_git/src/contact_git_code/contact_prediction/features/")
sys.path.append("/scratch/schneider/projects/contact_prediction_git/src/contact_git_code/contact_prediction/structure/")
import networkx as nx
import InputOutput
import numpy
from optparse import OptionParser
import pdb
import ResidueFeatureSecStruct
import ResidueFeatureRelSasa
import StructureContainer
import numpy as np
import pickle
import cPickle
from sklearn import cluster, datasets
## @var parser
#  Global parser object used to call program options from anywhere in the program.
parser = OptionParser()

def add_options( parser ):
    """Generic options function to specify command line inputs
    """
    parser.add_option("-p", type="string", dest="pdb_id_list", help="An example")

    options, args = parser.parse_args()
    return options, args 

options, args  = add_options( parser )

def shift_matrix():
    matrix = []
    for i in xrange(-8,9):
        row = []
        for j in xrange(-8,9):
            if i == 0 and j == 0:
                pass
            else:
                row.append((i,j))
                matrix.append((i,j))
    #for i in matrix:
        #print i
    return matrix




def calculate_probabities( all_shifts ):

    shift_len = len(all_shifts[0])
    for i in xrange(0,shift_len):
        shift_val = 0.0
        contact_val = 0.0
        for vec in all_shifts:
            shift_val += 1.0
            if vec[i] ==1.0:
                contact_val += 1.0
        print contact_val / shift_val
            #shift_vec.append(vec[i])

def get_relative_sec_struct_pos(ss_dict, i):
    anchor = ss_dict[i]
    pos = 1
    #print pos
    for j in xrange(1,20):
        if ss_dict.has_key(i-j):
            if anchor == ss_dict[i-j]:
                pos +=1
            else:
                return pos
        else:
            return pos
    return pos

def get_contact_vectors(structure, sec_struct, shift_mat):
    all_contacts = []
    for i in xrange(9, structure.get_number_of_residues()+1-9):
        for j in xrange(i+1, structure.get_number_of_residues()+1-9):
            if abs(i-j) >= 12:
                distance = structure.get_contact_map().get_mapped_distance(i,j)
                if distance <= 8.0:
                    contact_vector = []
                    for i_shift, j_shift in shift_mat:
                        if abs((i+i_shift)-(j+j_shift)) >= 12:
                            dist_shift = structure.get_contact_map().get_mapped_distance(i+i_shift,j+j_shift)
                            if dist_shift <= 8.0:
                                contact_vector.append(1.0)
                            else:
                                contact_vector.append(0.0)
                        else:
                            contact_vector.append(0.0)

                    all_contacts.append(contact_vector)
    return np.array(all_contacts)




def add_contacts( structure,  sec_struct_pair_types, shift_mat, sec_struct,sol):
    all_contacts = 0
    for i in xrange(9, structure.get_number_of_residues()+1-9):
        for j in xrange(i+1, structure.get_number_of_residues()+1-9):
            if abs(i-j) >= 12:
                distance = structure.get_contact_map().get_mapped_distance(i,j)
                if distance <= 8.0:
                    sec_lower = sec_struct.ss_dict[i]
                    sec_upper = sec_struct.ss_dict[j]
                    all_shifts = sec_struct_pair_types[(sec_lower,sec_upper)][0]
                    for i_shift, j_shift in shift_mat:
                        if abs((i+i_shift)-(j+j_shift)) >= 12:
                            dist_shift = structure.get_contact_map().get_mapped_distance(i+i_shift,j+j_shift)
                            if dist_shift <= 9.0:
                                if all_shifts.has_key((i_shift, j_shift)):
                                    if dist_shift <= 8.0:
                                        all_shifts[(i_shift, j_shift)] = all_shifts[(i_shift, j_shift)] + 1.0
                                    elif dist_shift <= 9.0:
                                        all_shifts[(i_shift, j_shift)] = all_shifts[(i_shift, j_shift)] + np.exp(-1.0* ((dist_shift-8.0)**2/0.2))
                                else:
                                    all_shifts[(i_shift, j_shift)] = 1.0
                    all_contacts += 1
                    sec_struct_pair_types[(sec_lower,sec_upper)] = ( all_shifts, all_contacts )
    return all_contacts
    #return all_contacts

def main():
    
    """Generic main function. Executes main functionality of program
    """


    #print bur_dict
    shift_mat = shift_matrix()
    #
    sec_struct_types = ["C","H","E"]
    bur_types = ["B","A"]
    seq_sep_types = [(12,24),(24,9999)]
    sec_struct_pair_types = {}
    for i in xrange(0,len(sec_struct_types)):
        for j in xrange(0,len(sec_struct_types)):
            #for k in xrange(0,len(seq_sep_types)):
                #for l in xrange(0,len(seq_sep_types)):
            all_shifts = {}
            all_contacts = 0
            sec_struct_pair_types[(sec_struct_types[i],sec_struct_types[j])] = (all_shifts,all_contacts)

    print sec_struct_pair_types
    #return 0


    all_c = []
    file = open(options.pdb_id_list)
    all_contacts = 0
    #sec_struct_pair_types#
    for line in file:
        pdb_id = str(line).strip().split()[0][0:5]

        pdb_file = "/scratch/schneider/pdb_select_dataset/%s/%s.pdb"%(pdb_id[0:4],pdb_id)
        tmp_struct = StructureContainer.StructureContainer()
        sec_struct = ResidueFeatureSecStruct.ResidueFeatureSecStruct(pdb_file)

        print pdb_id
        try:
            tmp_struct.load_structure('xxxx', pdb_id[-1],pdb_file, seqsep =1)
        except:
            tmp_struct.load_structure('xxxx', ' ',pdb_file, seqsep =1)

        """Buried features"""
        #bur_dict = {}
        #buried_features = ResidueFeatureRelSasa.ResidueFeatureRelSasa(pdb_file)
        #for i in xrange(1,tmp_struct.get_number_of_residues()+1):
        #    buried_features.calculate_feature(i,pdb_file)
        #    bur_dict[i] = buried_features.get_feature()
        #all_contacts += add_contacts(tmp_struct, sec_struct_pair_types, shift_mat, sec_struct, bur_dict)
        #print get_contact_vectors(tmp_struct, sec_struct, shift_mat)
        c = get_contact_vectors(tmp_struct, sec_struct, shift_mat)
        for i in c:
            all_c.append(i)
    c = numpy.array(all_c)
    #for i in c:
    #    print len(i)
    all_contacts = c.shape[0]
    print c.shape[1]
    k_means = cluster.KMeans(n_clusters=20)
    k_means.fit(c)
    #print k_means.labels_
    #print len(k_means.labels_)
    #sys.exit()
    true = []
    false = []
    for label in xrange(0,20):
        i_0 = numpy.array([0]*c.shape[1])
        for i in c:
            if k_means.predict(i)[0] == label:
                i_0 = i_0 + numpy.array(i)
                #print numpy.dot(i_0,i)
            #if k_means.predict(i)[0] == label:
        a =  numpy.array(i_0)
        a = a / float(all_contacts)#float(list(k_means.labels_).count(label))
        sum_prob = numpy.sum([i for i in a])
        a = a / float(sum_prob)
        #print a
        for i in c:
            if k_means.predict(i)[0] == label:
                true.append(numpy.dot(i,a))
            else:
                false.append( numpy.dot(i,a))
        #sec_struct_pair_types[0] = a
        all_values = {}
        for shift, val in zip(shift_mat, a):
            all_values[shift] = val
        sec_struct_pair_types[label] = all_values
    print sec_struct_pair_types
    print numpy.mean(true)
    print numpy.mean(false)
    cPickle.dump(sec_struct_pair_types, open( "shifts.p", "wb" ),protocol=2 )
    sys.exit()

    for keys, values in sec_struct_pair_types.iteritems():
        all_shifts = values[0]

        sum_prob = 0
        for shifts, counts in all_shifts.iteritems():
            all_shifts[shifts] = counts / float(all_contacts)
            sum_prob += counts / float(all_contacts)

        for shifts, counts in all_shifts.iteritems():
            all_shifts[shifts] = counts / float(sum_prob)
            #sum_prob += counts / float(all_contacts)
        sec_struct_pair_types[keys] = all_shifts


    for keys, values in sec_struct_pair_types.iteritems():
        print keys, values


    """
    for keys, values in all_shifts.iteritems():
        all_shifts[keys] = values / float(all_contacts)
    for keys, values in all_shifts.iteritems():
        print keys, values
    #calculate_probabities(all_shifts)
   # print all_shifts
                        #print tmp_struct.get_contact_map().get_mapped_distance(i+i_shift,j+j_shift)
                    #print
                #distance = tmp_struct.get_contact_map().get_mapped_distance(i,j)
                #print distance
    pickle.dump(all_shifts, open( "shifts.p", "wb" ) )
    """
    cPickle.dump(sec_struct_pair_types, open( "shifts.p", "wb" ),protocol=2 )
if __name__ == '__main__':
    sys.exit(main())
else:
    print("Loaded as a module!")  
