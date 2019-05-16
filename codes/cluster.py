import igraph as ig
import leidenalg as la
import numpy as np
import pickle

import sys, getopt


def jaccard_sim(a, b):
    inter = len(a.intersection(b))
    uni = len(a.union(b))
    if inter == 0:
        return 0
    else:
        return inter / uni


def create_graph(cell_polyA_dict, similarity_func):
    g = ig.Graph()
    vertices = list(cell_polyA_dict.keys())
    g.add_vertices(vertices)
    edges = list()
    weights = list()
    for cell1 in cell_polyA_dict:
        for cell2 in cell_polyA_dict:
            if cell1 == cell2:
                continue
            similarity = similarity_func(cell_polyA_dict.get(cell1), cell_polyA_dict.get(cell2))
            edges.append((cell1, cell2))
            weights.append(similarity)
    g.add_edges(edges)
    g.es['weight'] = weights

    return g


def calc_cv_list(graph):
    cv_list = list()
    for v in ig.VertexSeq(graph):
        weights = list()
        for neighbour in v.neighbors():
            weights.append(graph.es[graph.get_eid(v.index, neighbour.index)]['weight'])
        weights = np.asarray(weights)
        if np.mean(weights) != 0:
            cv_list.append(np.sqrt(np.var(weights)) / np.mean(weights))
    return cv_list


def save_array(array, output, fmt=None):
    if fmt is None:
        fmt = '%d'
    array = np.asarray(array)
    np.savetxt(fname=output, X=array, fmt=fmt)


if __name__ == '__main__':
    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv, '-i:')
    file = None
    for opt, arg in opts:
        if opt == '-i':
            file = arg
    if file is None:
        raise FileNotFoundError

    cell_polyA_dict = pickle.load(open(file, mode='rb'))

    sizes = list()
    for cell in cell_polyA_dict:
        sizes.append(len(cell_polyA_dict.get(cell)))

    save_array(sizes, '../outputs/cell_polyA_size.txt')

    g = create_graph(cell_polyA_dict, jaccard_sim)

    save_array(calc_cv_list(g), '../outputs/similarity_coeff_var.txt', '%1.4f')
    partition = la.find_partition(g, la.ModularityVertexPartition)

    file = open('../outputs/partition_print.txt', mode='w')
    file.write(str(partition))
    file.close()
