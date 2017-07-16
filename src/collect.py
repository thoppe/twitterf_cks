import json, joblib, glob, collections, codecs, os
import numpy as np
from unidecode import unidecode
from tqdm import tqdm
import pandas as pd
from geo_count import filter_pattern

keyword = 'fuck'
F_RAW = glob.glob("raw_firehose/*")

debug_cutoff = 10**20

def process(f):
    return [json.dumps(js) for (js,FLAG)
            in filter_pattern(F_RAW[0], keyword)
            if FLAG]

func = joblib.delayed(process)
ITR = tqdm(F_RAW[:debug_cutoff])

FOUT = open("collected_keywords.json",'w')

with joblib.Parallel(-1) as MP:
    for data in MP(func(x) for x in ITR):
        for line in data:
            FOUT.write(line+'\n')
