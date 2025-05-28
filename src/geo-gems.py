import warnings
# warnings.filterwarnings('ignore')

import folium
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

geo_pkg = '/media/i-files/data/geo_nl_cbs/gebieden-gpkg/cbsgebiedsindelingen2022.gpkg'
geo_gems = gpd.read_file(geo_pkg, layer = 'cbs_gemeente_2022_gegeneraliseerd')

print(type(geo_gems))
print(geo_gems.columns)
print(geo_gems['statnaam'])
print(geo_gems)

geo_gems['area'] = geo_gems.area
print(geo_gems.head())

print(geo_gems.crs)

fig, ax = plt.subplots(figsize=(8,8))

geo_gems.plot(ax=ax, facecolor='none', edgecolor='gray')
# plt.show()

file_path = 'data/kvk2020-wb2023.csv'
df_inkomen = pd.read_csv(file_path, sep=';')
df_inkomen = df_inkomen.loc[df_inkomen['Wijkcode'] == 'Totaal']
print(df_inkomen.shape)

selectie_col = 'Gemiddeld persoonlijk inkomen'
df_inkomen.loc[:,selectie_col] = 1000 * df_inkomen.loc[:,selectie_col]
print(df_inkomen.head())

geo_gems = pd.merge(geo_gems, df_inkomen, 
                    left_on='statnaam', 
                    right_on='Regionaam', 
                    how='left',
                   )

print(geo_gems)

fig, ax = plt.subplots(figsize=(8,8))

geo_gems.plot(ax=ax, edgecolor='gray', column=selectie_col, legend=True);
plt.show()

fig, ax = plt.subplots(figsize=(8,8))

geo_gems.plot(column=selectie_col, scheme='Quantiles', k=5, edgecolor='gray', 
              cmap='Blues', legend=True, ax=ax);

# plt.show()

gdf_prov_choro = geo_gems.copy()

gdf_prov_choro['geoid'] = gdf_prov_choro.index.astype(str)
gdf_prov_choro = gdf_prov_choro[['geoid', 'Gemiddeld bruto huishoudensinkomen', 
                                 'PROVINCIEN', 'geometry']]

print(gdf_prov_choro.head(3))

nld_lat = 52.2130
nld_lon = 5.2794

nld_coordinates = (nld_lat, nld_lon)

# Maak kaart van Nederland
map_nld = folium.Map(location=nld_coordinates, 
                     tiles='cartodbpositron', 
                     zoom_start=7, 
                     control_scale=True,
                    )

# Voeg inkomensdata toe
folium.Choropleth(geo_data=gdf_prov_choro,
                  data=gdf_prov_choro,
                  columns=['geoid', 'Gemiddeld bruto huishoudensinkomen'],
                  key_on='feature.id',
                  fill_color='Blues',                  
                  legend_name='Gemiddeld bruto huishoudensinkomen in Nederland'
                 ).add_to(map_nld)
# Toon resultaat
 
# Voeg tooltips toe
folium.features.GeoJson(data=gdf_prov_choro,                        
                        style_function=lambda x: {'color':'transparent','fillColor':'transparent','weight':0},
                        tooltip=folium.features.GeoJsonTooltip(fields=['PROVINCIEN', 'Gemiddeld bruto huishoudensinkomen'],
                                                               aliases=['Provincie', 'Inkomen'],
                                                               labels=True)
                       ).add_to(map_nld)

# Toon resultaat
map_nld.save('map.html')