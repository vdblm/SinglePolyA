import sys, getopt, glob, os, re
import pickle

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 'd:o:')
polyA_files_dir = None
output_path = None
for opt, arg in opts:
    if opt == '-d':
        polyA_files_dir = arg
    if opt == '-o':
        output_path = arg
if polyA_files_dir is None or output_path is None:
    raise NotADirectoryError

# {cell: set of polyA sites}
cell_polyA_dict = {}

# set of all polyA sites
all_polyA = set()
for file_name in glob.glob(os.path.join(polyA_files_dir, '*_polyA.txt')):
    # print(file_name)
    cell_polyA = set()
    file = open(file_name, mode='r')
    file_name = file_name.split('/')[-1]
    file_name = file_name.split('_')[0]
    lines = file.readlines()
    for line in lines:
        # TODO check if it is tab separated
        chr = re.split(r'\t+', line)[1]
        polyA = re.split(r'\t+', line)[3].split(sep=',')
        for p in polyA:
            cell_polyA.add(str(chr) + ':' + str(p))
            all_polyA.add(str(chr) + ':' + str(p))
    cell_polyA_dict[file_name] = cell_polyA
    file.close()

sorted_all_polyA = sorted(all_polyA)
# {cell: indices of 1s in the vector of 0-1 polyA position}
cell_one_index = {}
for cell in cell_polyA_dict:
    # print(cell)
    cell_polyA_set = cell_polyA_dict.get(cell)
    indices = set()
    for polyA in cell_polyA_set:
        indices.add(sorted_all_polyA.index(polyA))
    cell_one_index[cell] = indices

pickle.dump(cell_one_index, open(output_path, mode='wb'), protocol=pickle.HIGHEST_PROTOCOL)
