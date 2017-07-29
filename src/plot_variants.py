import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os, re
sns.set_style('darkgrid')

save_dest = 'figures'
os.system('mkdir -p {}'.format(save_dest))

df = pd.read_csv("data/fuck_variations.csv")
pattern = re.compile(r'[f][u](u+)[c][k]$')
idx = df.word.str.match(pattern)
df = df[idx]
df['u_count'] = df.word.str.count('u')
df = df.sort_values('u_count').set_index('u_count')

# Cutoff at a reasonable point
df = df[:15]
plt.plot(df.index, df["count"])
fs = 14
plt.xticks(df.index, df.word, rotation=75,fontsize=fs)
plt.ylabel("Observed fucks",fontsize=fs)
plt.title("F(u+)ck variants on twitter", fontsize=fs+2)
plt.tight_layout()
plt.savefig("figures/fuuuucks.png")
plt.show()
