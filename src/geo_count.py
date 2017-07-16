import json, joblib, glob, collections, codecs, os
import numpy as np
from unidecode import unidecode
from tqdm import tqdm
import pandas as pd

def filter_pattern(f, keyword):
    with codecs.open(f,'r','utf-8') as FIN:
        for line in FIN:
            js = json.loads(line)
            text = js["text"].lower()

            if keyword in text:
                yield js, True
            else:
                yield js, False
            

def read_pattern(f, keyword):
    C = collections.defaultdict(collections.Counter)
    info = {}

    for (js, FLAG) in filter_pattern(f, keyword):

        loc = unidecode(js["place"]['full_name'])

        if loc not in info:
                    
            info[loc] = js["place"]
            del info[loc]["id"]
            del info[loc]["attributes"]
            del info[loc]["country"]

            # Get the center of the bounding box
            bb = np.array(info[loc]["bounding_box"]["coordinates"])
            x,y = bb.mean(axis=1).ravel()
            info[loc]["x"] = x
            info[loc]["y"] = y
            del info[loc]["bounding_box"]
            
        C[loc]["_all"] += 1

        if not FLAG:
            continue
                                
        C[loc]['keyword'] += 1

    data = []
    for key in C:
        item = {"location":key,}
        for key2,val in C[key].items():
            item[key2] = val
        data.append(item)
        
    df = pd.DataFrame(data).set_index("location").fillna(0)
    
    return df, info


if __name__ == "__main__":
    keyword = "fuck"
    df = pd.DataFrame()

    F_RAW = glob.glob("raw_firehose/*")
    debug_cutoff = 10**20

    func = joblib.delayed(read_pattern)
    ITR = tqdm(F_RAW[:debug_cutoff])
    info = {}

    save_dest = 'data'
    os.system('mkdir -p {}'.format(save_dest))

    with joblib.Parallel(-1) as MP:
        for dfx,infox in MP(func(x, keyword) for x in ITR):
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
    df['average'] = df.keyword/df["_all"].astype('float')

    global_mean = df.keyword.sum() / df["_all"].sum()
    print global_mean
    df['delta'] = df.average - global_mean

    df = df.sort_values("average")

    # Estimate standard error with global mean
    df['standard_error'] = np.sqrt((global_mean*(1-global_mean))/df._all)
    df.to_csv("{}/fucks_to_give_geo_raw.csv".format(save_dest))

    # Filter for reasonable values
    # Require at least one positive and negative example
    df = df[(df.keyword > 0)&(df._all - df.keyword > 0)]

    # Require that the standard_error < epsilon
    df = df[df.standard_error < 0.005]
    df.to_csv("{}/fucks_to_give_geo.csv".format(save_dest))

    print df
