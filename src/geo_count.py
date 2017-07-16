import json, joblib, glob, collections, codecs, os
import numpy as np
from unidecode import unidecode
from tqdm import tqdm
import pandas as pd

save_dest = 'data'
os.system('mkdir -p {}'.format(save_dest))

F_RAW = glob.glob("raw_firehose/*")
debug_cutoff = 10

def read_pattern(f, keywords=[]):
    C = collections.defaultdict(collections.Counter)
    info = {}
    
    with codecs.open(f,'r','utf-8') as FIN:
        for line in FIN:
            js = json.loads(line)
            loc = unidecode(js["place"]['full_name'])

            C[loc]["_all"] += 1

            text = js["text"].lower()
            for key in keywords:

                # Touch the value
                #C[loc][key]
                if loc not in info:
                    
                    info[loc] = js["place"]
                    del info[loc]["id"]
                    del info[loc]["attributes"]
                    del info[loc]["country"]

                    # Get the center of the bounding box
                    bb = np.array(info[loc]["bounding_box"]["coordinates"])
                    x,y = bb.mean(axis=1).ravel()
                    #info[loc]["bounding_box"] = bb
                    info[loc]["x"] = x
                    info[loc]["y"] = y
                    
                    del info[loc]["bounding_box"]
                                        
                
                if key in text:
                    C[loc][key] += 1

    data = []
    for key in C:
        item = {"location":key,}
        for key2,val in C[key].items():
            item[key2] = val
            
        data.append(item)
    df = pd.DataFrame(data).set_index("location").fillna(0)
    return df, info


word = "fuck"
keywords = [word]
df = pd.DataFrame()

func = joblib.delayed(read_pattern)
ITR = tqdm(F_RAW[:debug_cutoff])
info = {}

with joblib.Parallel(-1) as MP:
    for dfx,infox in MP(func(x, keywords) for x in ITR):
        info.update(infox)
        df = df.add(dfx, fill_value=0).sort_values("_all")

info = pd.DataFrame(info.values()).set_index("full_name")
df = df.merge(info, left_index=True,right_index=True)
print "Total locations", len(df)

idx = df.country_code=="US"
df = df[idx]
print "Total locations inside the US", len(df)

# Drop non-cities
idx = df.place_type=="city"
df = df[idx]
print "Total locations that are US cities", len(df)

df.index.name = "full_name"   
df['average'] = df[word]/df["_all"].astype('float')

global_mean = df[word].sum() / df["_all"].sum()
print global_mean
df['delta'] = df.average - global_mean

df = df.sort_values("average")
df['standard_error'] = np.sqrt((df.average*(1-df.average))/df._all)
df.to_csv("{}/fucks_to_give_geo_raw.csv".format(save_dest))

# Filter for reasonable values
# Require at least one fuck and non-fuck
df = df[(df[word] > 0)&(df._all - df[word] > 0)]

# Require at least one normal tweet
df = df[df[word] > 0]

# Require that the standard_error < epsilon
df = df[df.standard_error < 0.01]
df.to_csv("{}/fucks_to_give_geo.csv".format(save_dest))

print df
