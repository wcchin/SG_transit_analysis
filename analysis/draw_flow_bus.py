import os
import pandas as pd
import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import json

import warnings
warnings.filterwarnings('ignore')

with open(os.path.join("../data", 'subzone_centroid_pos.json'), 'r') as fread:
    pos = json.load(fread)

region = gpd.read_file("../data/region-2014/MP14_REGION_WEB_PL.shp")

data_dir = "../data/OD_bus"
fs = os.listdir(data_dir)
fs = sorted([ f for f in fs if "weekday" in f ])

def draw_fig(dg, hr):
    weights = []
    for u,v,d in dg.edges(data=True):
        weights.append((d["weight"], u, v))
    weights = sorted(weights, reverse=True)
    
    fig, ax = plt.subplots(figsize=(20,10))
    nx.draw_networkx_nodes(dg, node_size=10, node_color='grey', pos=pos, ax=ax)
    
    threshold = 3000
    if len(weights)>threshold:
        break_val = int(float(threshold)/3.)
    else:
        break_val = int(float(len(weights))/3.)
    edges1 = [ (u,v) for w,u,v in weights[0:break_val] ]
    edges2 = [ (u,v) for w,u,v in weights[break_val:break_val*2] ]
    edges3 = [ (u,v) for w,u,v in weights[break_val*2:break_val*3] ]
    nx.draw_networkx_edges(dg, edgelist=edges1, width=1., edge_color="red", pos=pos, ax=ax)
    nx.draw_networkx_edges(dg, edgelist=edges2, width=0.5, edge_color="blue", pos=pos, ax=ax)
    nx.draw_networkx_edges(dg, edgelist=edges3, width=0.1, edge_color="green", pos=pos, ax=ax)
    
    ax.set_aspect("equal")
    region.plot(ax=ax, color="grey", edgecolor="k", alpha=0.1)
    ax.set_xlim([5000,50000])
    ax.set_ylim([25000,50000])
    #ax.set_xticks([])
    #ax.set_yticks([])
    ax.set_title("bus flow, weekday, hour: {}, count edges: {}".format(hr, str(len(weights))))
    plt.tight_layout()
    figout = os.path.join("bus_flow_fig", "fig_bus_weekday_3000_{}.png".format(hr))
    plt.savefig(figout, dpi=300, bbox_inches="tight")
    plt.close()

for f in fs[:]:
    print(f)
    hr = f[-6:-4]
    fp = os.path.join(data_dir, f)
    df = pd.read_csv(fp, index_col=0)
    df = df.dropna(subset=["origin", "destination"])
    recs = []
    for i in range(len(df)):
        row = df.iloc[i]
        o = row["origin"]
        d = row['destination']
        f = row['flow']
        recs.append((o,d,{"weight":f}))
    dg = nx.DiGraph()
    dg.add_nodes_from(list(pos.keys()))
    dg.add_edges_from(recs)
    draw_fig(dg, hr)
    print(hr, dg.number_of_nodes(), dg.number_of_edges())
    #break
print("done")
