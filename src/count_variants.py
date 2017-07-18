import json, joblib, glob, collections, os
from unidecode import unidecode
from tqdm import tqdm
import pandas as pd
import re

F_RAW = glob.glob("raw_firehose/*")
save_dest = "collected_variants"
os.system('mkdir -p {}'.format(save_dest))

def read_pattern(f, keywords=[]):
    C = collections.Counter()
    f_out = os.path.join(save_dest,os.path.basename(f)).replace('.txt','.csv')

    data = []
    center = re.escape("aeioyvu!@#$%^&*+-_")
    print center
    exit()
    pattern = re.compile(r'(f+)([%s]+)(c+k+)'%center, re.IGNORECASE)
    
    with open(f) as FIN:
        for line in FIN:
            js = json.loads(line)
            text = unidecode(js["text"])
            for m in pattern.findall(text):
                word = ''.join(m).lower()
                C[word] += 1
    return C



func = joblib.delayed(read_pattern)
ITR = tqdm(F_RAW[:])

C = collections.Counter()
with joblib.Parallel(-1) as MP:
    for c in MP(func(x) for x in ITR):
        C.update(c)

df = pd.Series(C).sort_values(ascending=False).reset_index()
df = pd.DataFrame(df)
df.columns = ['word','count']
df.set_index('word').to_csv("fucking_variants.csv")
