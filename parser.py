from functools import reduce
import operator
import os
import collections

def load_ft_vecs(filename):
    f = open(filename, "r")
    lines = f.readlines()
    vecs = []
    for line in lines:
        if "SIOA: True" in line:
            # print("break case")
            break
        if line.startswith('\tFeature vector:'):
            open_brace = line.index("[")
            close_brace = line.index("]", open_brace)
            vec = line[open_brace+1:close_brace]
            vec = vec.replace(' ', '')  
            vec = vec.split(",")    
            vecs.append([int(val) for val in vec])
    return vecs

def flatten(l):
    return reduce(operator.concat, l)
    
def compute_avg_ft_val(filename):
    vecs = load_ft_vecs(filename)
    flat_vec = flatten(vecs)
    return sum(flat_vec)/len(flat_vec)


def compute_num_uniq_cultures(filename):
    vecs = load_ft_vecs(filename)
    cultures = set()
    for vec in vecs:
        key = tuple(vec)
        cultures.add(key)
    # print(cultures)
    return len(cultures)

def parse(out_file, operations):
    walk = os.walk("exports")
    fil_out = open(out_file, "w")
    for w in walk:
        if "Phase" not in w[0]:
            # print(w)
            for fil in w[2]:
                if fil.startswith("id"):
                    path = w[0] + "/" + fil
                    val_string = ""
                    for operation in operations:
                        val = operation(path)
                        val_string += str(val) + ", "
                    fil_out.write(fil + ", " + val_string + "\n")


if __name__ == "__main__":
    parse("avgs5.txt", [compute_avg_ft_val, compute_num_uniq_cultures])
    # print(compute_num_uniq_cultures("exports/nF10nT10nS_min1max1PAO0.7AOV0.3/id2_nF10nT10nS_min1max1PAO0.7AOV0.3.txt"))