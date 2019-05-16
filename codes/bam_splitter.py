import pysam, sys, getopt

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 'i:o:t:f:')
input_file = None
output_directory = None
tag = None
names = None
for opt, arg in opts:
    if opt == '-i':
        input_file = arg
    elif opt == '-o':
        output_directory = arg
    elif opt == '-t':
        tag = arg
    elif opt == '-f':
        names = arg
if input_file is None or output_directory is None or tag is None:
    print('arguments wrong')
    sys.exit(2)

pure_bam = pysam.AlignmentFile(input_file)
memory_read_arrays = {}
uniq_names = None
if names is not None:
    uniq_names = set()
    names = open(names, mode='r')
    for line in names.readlines():
        uniq_names.add(line[0:len(line)-1])

for read in pure_bam:
    try:
        key = read.get_tag(tag)
    except:
        continue
    if uniq_names is not None:
        if key not in uniq_names:
            continue
    if memory_read_arrays.get(key) is None:
        read_array = list()
    else:
        read_array = memory_read_arrays.get(key)
    read_array.append(read)
    memory_read_arrays[key] = read_array

for key in memory_read_arrays:
    f = pysam.AlignmentFile(output_directory + key + '.bam', 'wb', template=pure_bam)
    for read in memory_read_arrays.get(key):
        f.write(read)
    f.close()
pure_bam.close()
