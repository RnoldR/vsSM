import warnings
# warnings.filterwarnings('ignore')

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

file_path = '/media/i-files/data/geo_nl_cbs/provincies/GRS_1000_PROV_NL_V.shp'
gdf_prov = gpd.read_file(file_path)

print(type(gdf_prov))
print(gdf_prov.columns)
print(gdf_prov['PROVINCIEN'])
print(gdf_prov)

gdf_prov['area'] = gdf_prov.area
print(gdf_prov.head())

print(gdf_prov.crs)

fig, ax = plt.subplots(figsize=(8,8))

gdf_prov.plot(ax=ax, facecolor='none', edgecolor='gray')
# plt.show()

file_path = 'data/inkomen-per-provincie.csv'
df_inkomen = pd.read_csv(file_path, sep=';')

print(df_inkomen)

gdf_prov = pd.merge(gdf_prov, df_inkomen, left_on='PROVINCIEN', right_on='Provincie', how='left')

print(type(gdf_prov))
print(gdf_prov)

fig, ax = plt.subplots(figsize=(8,8))

column = 'Gemiddeld bruto huishoudensinkomen'
gdf_prov.plot(ax=ax, edgecolor='gray', column=column, legend=True);
# plt.show()

column = 'Gemiddeld bruto huishoudensinkomen'

fig, ax = plt.subplots(figsize=(8,8))

gdf_prov.plot(column=column, scheme='Quantiles', k=5, edgecolor='gray', 
              cmap='Blues', legend=True, ax=ax);

plt.show()
