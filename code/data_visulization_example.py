#this script creates maps of average daily PM2.5 and its chemical components
#for each county across years (2006-2017)

import geopandas as gpd
import pandas as pd

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

path = "/Users/dariaageikina/Downloads"

#load geospatial data on counties
counties = gpd.read_file(path+'/gz_2010_us_050_00_20m/gz_2010_us_050_00_20m.shp')
counties['fips'] = counties['STATE']+counties['COUNTY']
counties['fips'] = counties['fips'].astype(float)

#load data on PM2.5 components
alldata = pd.read_stata(path+'/main_data.dta')
#get summaries for the variables in each county (fips) across all years
variables = ['PM25', 'BC_p', 'OM_p', 'NH4_p', 'NIT_p', 'SO4_p', 'SS_p', 'SOIL_p']
alldata_avg = alldata.groupby('fips')[variables].mean().reset_index()

#merge two datasets
merged = counties.merge(alldata_avg, on='fips')

#plot the graphs
labels = ['PM2.5', 'BC%', 'OM%', 'NH4%', 'NIT%', 'SO4%', 'SS%', 'SOIL%']

fig, axs = plt.subplots(4, 2, figsize=(20, 22))
fig.subplots_adjust(hspace=0.01, wspace=0.05)  #spacing between plots

for ax, var, label in zip(axs.flatten(), variables, labels):
    cax = merged.plot(column=var,
                        cmap='viridis', 
                        linewidth=0.1,
                        edgecolor='black',
                        ax=ax)

    #colorbar
    divider = make_axes_locatable(ax)
    cax2 = divider.append_axes("right", size="3%", pad=0.1)
    sm = plt.cm.ScalarMappable(cmap='viridis', 
                               norm=plt.Normalize(vmin=merged[var].min(), 
                                                  vmax=merged[var].max()))
    sm._A = []
    cbar = fig.colorbar(sm, cax=cax2)
    cbar.ax.tick_params(labelsize=14)
    
    ax.set_title(label, fontsize=20)
    ax.set_axis_off()  # Hide the axes

#title
plt.suptitle("Average PM2.5 and its components for U.S. counties (2006-2017)", fontsize=30, fontweight='bold', y=0.9, x=0.55)  # Adjust y for vertical positioning

plt.savefig(path+"/PM25_maps.png", bbox_inches='tight', dpi=300)
plt.show()