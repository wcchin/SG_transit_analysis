
from collections import defaultdict
import numpy as np
import networkx as nx
from tqdm import tqdm


def normalize_edges(dg_temp, weight="weight", by_median=True):
    # default by median, else by mean
    all_weights = []
    for u,v,d in dg_temp.edges(data=True):
        all_weights.append(d[weight])
    if by_median:
        m_weight = np.median(all_weights)
    else:
        m_weight = np.mean(all_weights)
    min_weight = min([ w/m_weight for w in all_weights ])
    dg_tempb = nx.DiGraph()
    for u,v,d in dg_temp.edges(data=True):
        w = (d["weight"]/m_weight)/min_weight
        dg_tempb.add_edge(u, v, weight=w)
    return dg_tempb


def calculate_ki_prime(dg_temp, weight="weight", direction="in", alpha=1., beta=1):
    #dg_temp = normalize_edges(dg_temp, weight=weight, by_median=normalize_edges_by_median)
    if direction=="in":
        wdegs = dict(dg_temp.in_degree(weight=weight))
        ndegs = dict(dg_temp.in_degree(weight=None))
    else:
        wdegs = dict(dg_temp.out_degree(weight=weight))
        ndegs = dict(dg_temp.out_degree(weight=None))
    com_degs = {}
    for n in dg_temp.nodes():
        cd = (ndegs[n]**alpha * wdegs[n]**beta)**(1./(alpha+beta))
        cd = int(round(cd, 0))
        com_degs[n] = cd
    return com_degs


def prune_graph(dg_temp, weight="weight", direction="in", alpha=1., beta=1.):
    ki_prime = calculate_ki_prime(dg_temp, weight=weight, direction=direction, alpha=alpha, beta=beta)
    min_ki = min(list(ki_prime.values()))
    prune_nodes = [ n for n,v in ki_prime.items() if v<=min_ki ]
    dg_temp.remove_nodes_from(prune_nodes)
    done = False
    while not(done):
        ki_prime = calculate_ki_prime(dg_temp, weight=weight, direction=direction, alpha=alpha, beta=beta)
        cur_min_ki = min(list(ki_prime.values()))
        if cur_min_ki<=min_ki:
            cur_prune_nodes = [ n for n,v in ki_prime.items() if v<=min_ki ]
            dg_temp.remove_nodes_from(cur_prune_nodes)
            prune_nodes.extend(cur_prune_nodes)
            if dg_temp.number_of_nodes()<=0:
                done = True
        else:
            done = True
    return dg_temp, min_ki, prune_nodes


def filtering_edge_weight(dg_temp, weight="weight", filter_edge_weight=0):
    edges = defaultdict(int)
    for u,v,d in dg_temp.edges(data=True):
        w = d[weight]
        if w>filter_edge_weight:
            edges[(u, v)]+=w
    dg_temp2 = nx.DiGraph()
    dg_temp2.add_nodes_from(dg_temp.nodes())
    dg_temp2.add_edges_from([ (k[0], k[1], {weight: v} ) for k,v in edges.items() ])
    return dg_temp2



def wkshell_decomposition(dg_temp, weight="weight", direction="in", alpha=1., beta=1., filter_edge_weight=None, group_k_by=1, normalize_edges_by_median=True):
    if not(filter_edge_weight is None):
        dg_temp = filtering_edge_weight(dg_temp, weight=weight, filter_edge_weight=filter_edge_weight)
    dg_temp = normalize_edges(dg_temp, weight=weight, by_median=normalize_edges_by_median)
    
    kshell = {}
    kshell_val = {}
    ks = 1
    pbar = tqdm(total=dg_temp.number_of_nodes())
    while dg_temp.number_of_nodes()>0:
        dg_temp, min_ki, prune_nodes = prune_graph(dg_temp, weight=weight, direction=direction, alpha=alpha, beta=beta)
        kshell[ks] = prune_nodes
        kshell_val[ks] = min_ki
        #print("done for ks={}, value={}".format(ks, min_ki))
        pbar.update(len(prune_nodes))
        ks+=1
    pbar.close()
    node_ks = {}
    for k,vs in kshell.items():
        for n in vs:
            node_ks[n] = int(kshell_val[k]/group_k_by)
    return node_ks