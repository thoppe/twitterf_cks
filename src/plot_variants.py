import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os, re

save_dest = 'figures'
os.system('mkdir -p {}'.format(save_dest))

df = pd.read_csv("data/fuck_variations.csv")#.set_index('word')
pattern = re.compile(r'[f][u](u+)[c][k]$')
idx = df.word.str.match(pattern)
df = df[idx]
df['u_count'] = df.word.str.count('u')
df = df.sort_values('u_count').set_index('u_count')

# Cutoff at a reasonable point
df = df[:15]
plt.plot(df.index, df["count"])
plt.xticks(df.index, df.word, rotation=75,fontsize=18)
plt.ylabel("Observed fucks",fontsize=18)
plt.tight_layout()
plt.savefig("figures/fuuuucks.png")
plt.show()
