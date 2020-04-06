import os
from collections import defaultdict
import pandas as pd
import geopandas as gpd


def process_an_hour(df_temp, hr):
    dirty_work = { "DT16": "DT16-CE1", "CE1": "DT16-CE1", "NE1": "NE1-CC29", "CC29": "NE1-CC29" }
    flows = defaultdict(int)
    for i in range(len(df_temp)):
        this_row = df_temp.iloc[i]
        o = this_row["ORIGIN_PT_CODE"]
        d = this_row["DESTINATION_PT_CODE"]
        t = this_row["TOTAL_TRIPS"]
        if o in dirty_work.keys(): 
            o = dirty_work[o]
        if d in dirty_work.keys(): 
            d = dirty_work[d]
        if "-" in o:
            o = o.split("-")[0]
        if "-" in d:
            d = d.split("-")[0]
        try:
            o2 = bus_stop_loc[str(o)]
            d2 = bus_stop_loc[str(d)]
            flows[(o2, d2)]+=t
            #print(i, (o2, d2))
        except:
            if not(str(o) in bus_stop_loc):
                print(str(o) +" not found")
            if not(str(d) in bus_stop_loc):
                print(str(d) +" not found")
            print("skip this {} - {}".format(o, d))
    
    flows2 = []
    print(len(flows))
    for k,v in flows.items():
        i,j = k
        d = {"origin":i, "destination":j, "hour":hr, "flow": v}
        flows2.append(d)
    df2 = pd.DataFrame.from_dict(flows2)
    df2 = df2[["origin", "destination", "hour", "flow"]]
    return df2

def process_df(df, month_str):
    df_wday = df[df["DAY_TYPE"]=="WEEKDAY"]
    for hr in range(24):
        temp = df_wday[df_wday["TIME_PER_HOUR"]==hr]
        if len(temp)>0:
            temp2 = process_an_hour(temp, hr)
            fout = os.path.join(data_dir, "OD_train", "OD_{}_weekday_{}.csv".format(month_str, str(hr).zfill(2)))
            temp2.to_csv(fout, index_label="ind")
            print(hr, len(temp), len(temp2))
            #break
    print("holiday")
    df_wend = df[df["DAY_TYPE"]=="WEEKENDS/HOLIDAY"]
    for hr in range(24):
        temp = df_wend[df_wend["TIME_PER_HOUR"]==hr]
        if len(temp)>0:
            temp2 = process_an_hour(temp, hr)
            fout = os.path.join(data_dir, "OD_train", "OD_{}_weekend_{}.csv".format(month_str, str(hr).zfill(2)))
            temp2.to_csv(fout, index_label="ind")
            print(hr, len(temp), len(temp2))
            #break




data_dir = "../data"

gdf = gpd.read_file(os.path.join(data_dir, 'train_station_wszone.shp'))
bus_stop_loc = {}
for i,s in zip(gdf["PT_CODE1"].tolist(), gdf["SUBZONE_N"].tolist()):
    bus_stop_loc[i] = s
#print(len(bus_stop_loc))

fs = [ f for f in os.listdir(data_dir) if ".csv.xz" in f ]
fs = [ f for f in fs if "origin_destination_train" in f ] 

fs = [ 'origin_destination_train_201911.csv.xz' ]

for f in fs:
    month_str = f.replace("origin_destination_train_", "").replace(".csv.xz", "")
    print(month_str)
    df = pd.read_csv(os.path.join(data_dir, f))
    process_df(df, month_str)
