import BioSimSpace as BSS
from BioSimSpace import _Exceptions
import sys
import csv
import os
import numpy as np 

print ("%s %s %s" % (sys.argv[0], sys.argv[1], sys.argv[2]))
results_file_path = "./outputs/summary.csv"


# simply load the FEP directory of the corresponding ligand using BSS.
# this function computes the binding free energy as well.

engine = sys.argv[3]
path_to_dir = f"./outputs/{engine}/{sys.argv[1]}~{sys.argv[2]}"

try:
    pmf_0, pmf_1, freenrg, overlap_matrix_bound, overlap_matrix_free = BSS.FreeEnergy.analyse(path_to_dir, "binding")
    freenrg_val = round(freenrg[0].magnitude(), 4)
    freenrg_err = round(freenrg[1].magnitude(), 4)
except _Exceptions.AnalysisError:
    freenrg_val = freenrg_err = "Fail"
    overlap_matrix_bound = overlap_matrix_free = None


data_point = [sys.argv[1], sys.argv[2], str(freenrg_val), str(freenrg_err), engine]

####### WRITING DATA

# use csv to open the results file.
with open(results_file_path, "a") as freenrg_writefile:
    writer = csv.writer(freenrg_writefile)
    
    # first, write a header if the file is created for the first time.
    if os.path.getsize(results_file_path) == 0:
        print(f"Starting {results_file_path} file.")
        writer.writerow(["lig_1", "lig_2", "freenrg", "error", "engine"])

    
with open(results_file_path, "r") as freenrg_readfile:
    # then, grab all of the data that is already in the file.
    reader = csv.reader(freenrg_readfile)
    data_entries = [ row for row in reader ]

# check if our data entry is not already in the results file. Raise an error if is.
if data_point in data_entries:
    raise Exception(f"Results for this run are already in {results_file_path}. Exiting.")

# at this point we know that we are writing a new entry in the results file. Append the line to the file.
# use csv to open the results file.
with open(results_file_path, "a") as freenrg_writefile:
    writer = csv.writer(freenrg_writefile)

    print("Writing MBAR results. Free energy of binding and error are (rsp.):")
    print(freenrg)
    writer.writerow(data_point)


# in case of SOMD, we will also have overlap matrices for both legs. These are helpful for troubleshooting, so store 
# them in ./logs/
if overlap_matrix_bound:
    np.save(f"logs/overlap_bound_{sys.argv[1]}~{sys.argv[2]}", np.matrix(overlap_matrix_bound))
else:
    print("Failed to write overlap matrix for bound leg.")
if overlap_matrix_free:
    np.save(f"logs/overlap_free_{sys.argv[1]}~{sys.argv[2]}", np.matrix(overlap_matrix_free))
else:
    print("Failed to write overlap matrix for free leg.")


