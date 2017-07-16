from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

save_dest = 'figures'
os.system('mkdir -p {}'.format(save_dest))

df = pd.read_csv("data/fucks_to_give_geo.csv").set_index('full_name')
min_tweets = 2000
df = df[df["_all"]>min_tweets]
true_avg = ((df.keyword/df._all)-df.delta).mean()
#df['frac'] = (true_avg-df.delta)/true_avg
df['frac'] = (df.keyword/df._all) / true_avg

# Lambert Conformal map of lower 48 states.
resolution = ['c','l','i','h','f'][2] # Higher is better but takes longer

m = Basemap(
    llcrnrlon=-119,
    llcrnrlat=22,
    urcrnrlon=-64,
    urcrnrlat=49,
    projection='lcc',lat_1=33,lat_2=45,lon_0=-95,
    resolution = resolution,
    area_thresh=1000,
)


def draw_map_background(m, ax):
    lw = 0.25
    ax.set_facecolor('#DDEAF0')
    m.fillcontinents(color='#FAFAFA', ax=ax, zorder=0)
    #m.drawcounties(ax=ax)
    m.drawstates(ax=ax,linewidth=lw)
    m.drawcountries(ax=ax,linewidth=lw)
    m.drawcoastlines(ax=ax,linewidth=lw)

fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)
draw_map_background(m, ax)

print df
cmap = sns.cubehelix_palette(as_cmap=True)
cmap = sns.diverging_palette(240, 10, n=6, as_cmap=True)


m.scatter(
    df.x.values,
    df.y.values,
    #c=df.delta,
    c=df.frac,
    cmap=cmap,
    alpha=0.90,
    s=45,
    lw=0,
    edgecolors='none',
    latlon=True,
    vmax=0,
    vmin=2,
)

cbar = plt.colorbar(fraction=0.03)
text = 'Fucks given per US baseline of {:d}/1000 tweets'.format(int(true_avg*1000))
cbar.ax.set_ylabel(text, rotation=90)

text = "Fucks given: Cities with >{} tweets".format(min_tweets)
plt.title(text, fontsize=18)
plt.tight_layout()

plt.savefig(os.path.join(save_dest,"fucks_given_per_city.png"))

plt.show()
