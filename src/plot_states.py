from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import os
from matplotlib.patches import Polygon

cmap = sns.cubehelix_palette(as_cmap=True)
cmap = sns.diverging_palette(240, 10, n=6, as_cmap=True)

save_dest = 'figures'
os.system('mkdir -p {}'.format(save_dest))
df = pd.read_csv("data/fucks_to_give_geo_raw.csv")#.set_index('full_name')
df['state'] = df.full_name.str.split(', ').apply(lambda x:x[-1])
mean  = df['keyword'].sum()/float(df['_all'].sum())

dfx = pd.DataFrame()
dfx['_all'] = df.groupby("state")['_all'].sum()
dfx['keyword'] = df.groupby("state")['keyword'].sum()
dfx['average'] = dfx.keyword/dfx._all.astype(float)
dfx['delta'] = dfx.average - mean
dfx['frac'] = dfx.average / mean
dfx = dfx.sort_values('delta')

dfx.to_csv("data/fucks_to_give_geo_state.csv")

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


short_state_names = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}
short_state_names_inv = {v: k for k, v in short_state_names.iteritems()}

m.readshapefile('src/state_maps/st99_d00',
                name='states', drawbounds=False)

state_names = []
for shape_dict in m.states_info:
    abbr = short_state_names_inv[shape_dict["NAME"]]
    state_names.append(abbr)
state_names = pd.DataFrame(state_names,columns=['ABBR'])


def draw_map_background(m, ax):
    lw = 0.25
    ax.set_facecolor('#DDEAF0')
    m.fillcontinents(color='#FAFAFA', ax=ax, zorder=0)
    m.drawstates(ax=ax,linewidth=lw)
    m.drawcountries(ax=ax,linewidth=lw)
    m.drawcoastlines(ax=ax,linewidth=lw)

fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)


vmax = 1.5
vmin = 0.5

for abbr in dfx.index:
    idx = state_names.ABBR==abbr
    avg = dfx.ix[abbr, 'frac']

    color = cmap((np.clip(avg, vmin, vmax)-vmin) / (vmax-vmin))

    for i in np.where(idx)[0]:

        seg = m.states[i]
        poly = Polygon(seg, facecolor=color,edgecolor=None)
        ax.add_patch(poly)

draw_map_background(m, ax)

text = "National fucks given on a state level"
plt.title(text, fontsize=18)

plt.scatter([0,0],[0,0],c=[vmin,vmax],
            s=0,vmax=vmax,vmin=vmin,cmap=cmap)
cbar = plt.colorbar(fraction=0.03)

text = 'Fucks given per US baseline of {:d}/1000 tweets'.format(int(mean*1000))
cbar.ax.set_ylabel(text, rotation=90)


plt.tight_layout()
plt.savefig(os.path.join(save_dest,"fucks_given_national.png"))
plt.show()


