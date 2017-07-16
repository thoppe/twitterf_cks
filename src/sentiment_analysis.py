from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import json, joblib, glob, collections
from unidecode import unidecode
from tqdm import tqdm
import nlpre

def tweet_iterator(cutoff):
    with open("collected_keywords.json",'r') as FIN:
        for k,line in enumerate(FIN):
            js = json.loads(line)
            yield js['text']

            if cutoff and k>cutoff:
                raise StopIteration

parser = nlpre.url_replacement()
analyzer = SentimentIntensityAnalyzer()
def process(tweet):
    item = {"_text":parser(tweet)}
    item.update( analyzer.polarity_scores(item['_text']) )
    return item

ITR = tqdm(tweet_iterator(0))
func = joblib.delayed(process)

with joblib.Parallel(-1) as MP:
    df = pd.DataFrame(MP(func(x) for x in ITR))
print len(df)
df = df.sort_values("compound").drop_duplicates(subset=('_text'))
df.to_csv("data/fucking_sentiment.csv", encoding='utf-8', index=False)
print len(df)
