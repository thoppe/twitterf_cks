from tqdm import tqdm
import itertools, collections
import pandas as pd
df = pd.read_csv("data/collected_curse.csv",nrows=10**20)

total = df.sum(axis=0)
total = (total/total.sum()).sort_values(ascending=False)
print total

C = collections.defaultdict(int)
for w0,w1 in itertools.combinations(df.columns,r=2):
    val = ((df[w0]>0) & (df[w1]>0)).sum()
    C[(w0,w1)] = val
    C[(w1,w0)] = val

for w0 in df.columns:
    C[(w0,w0)] = (df[w0]>1).sum()
    
keys = set([x[0] for x in C.keys()])
df = pd.DataFrame(0, index=total.index,columns=total.index)
for (k0,k1),v in C.iteritems():
    df[k0][k1] = v

df /= df.sum(axis=0)
df = df.T

import seaborn as sns
import pylab as plt
sns.heatmap(df,vmin=0,vmax=0.5)
plt.xticks(rotation=90)
plt.yticks(rotation=0) 
plt.tight_layout()
plt.savefig("figures/curse_colocation.png")
plt.show()



    
