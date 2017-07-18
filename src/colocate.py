import glob, json, collections
import joblib
from tqdm import tqdm
import pandas as pd

F_TXT = glob.glob("raw_firehose/*.txt")

# List takens from: 
# http://www.slate.com/blogs/lexicon_valley/2013/09/11/top_swear_words_most_popular_curse_words_on_facebook.html
keywords = set([
    'fuck',
    'shit',
    'damn',
    'bitch',
    'crap',
    'dick',
    'piss',
    'pussy',
    'fag',
    'asshole',
    'cock',
    'bastard',
    'darn',
    'douche',
    'slut',
    'bastard',
])

def keep_tweet(text):
    for key in keywords:
        if key in text:
            return True
    return False

def count_tweet(text):
    c = collections.Counter()
    for key in keywords:
        c[key] = text.count(key)
    return c


def compute(f):
    print "starting", f
    data = []
    with open(f) as FIN:
        for line in FIN:
            try:
                js = json.loads(line)
                text = js['text']
                tokens = [x for x in text.split() if x[0] != '@']
                text = ' '.join(tokens)
            except:
                continue

            if not keep_tweet(text):
                continue

            data.append(count_tweet(text))

    return data


func = joblib.delayed(compute)
data = []

ITR = tqdm(F_TXT[:])

with joblib.Parallel(-1) as MP:
    for res in MP(func(x) for x in ITR):
        data.extend(res)

print "Building dataframe"
df = pd.DataFrame(data)
df.to_csv("data/collected_curse.csv",index=False)
print df

