import warnings
# warnings.filterwarnings('ignore')

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium

def analyse_polygon(df: pd.DataFrame):
    cell = df.loc[0, 'geometry']
    print(type(cell))
    print(dir(cell))
    print(cell.length)
    print(cell.centroid)
    print(cell.length)
    # print(cell.boundary)

    poly = list(cell.geoms)

    print(len(poly))

    return

geo_pkg = '/media/i-files/data/geo_nl_cbs/gebieden-gpkg/cbsgebiedsindelingen2022.gpkg'
geo_gems = gpd.read_file(geo_pkg, layer = 'cbs_gemeente_2022_gegeneraliseerd')

# print(type(geo_gems))
# print(geo_gems.columns)
# print(geo_gems['statnaam'])
# print(geo_gems)

geo_gems['area'] = geo_gems.area

# print(geo_gems.head())
# print(geo_gems.crs)
analyse_polygon(geo_gems)

fig, ax = plt.subplots(figsize=(8,8))

geo_gems.plot(ax=ax, facecolor='none', edgecolor='gray')
# plt.show()

file_path = 'data/kvk2020-wb2023.csv'
df_inkomen = pd.read_csv(file_path, sep=';')
df_inkomen = df_inkomen.loc[df_inkomen['Wijkcode'] == 'Totaal']
print(df_inkomen.shape)

selectie_col = 'Gemiddeld persoonlijk inkomen'
df_inkomen[selectie_col] = df_inkomen[selectie_col].astype(float)
df_inkomen.loc[:, selectie_col] *= 1000 # df_inkomen[selectie_col] * 1000

geo_gems = pd.merge(geo_gems, df_inkomen, 
                    left_on='statnaam', 
                    right_on='Regionaam', 
                    how='left',
                   )

print('==>', geo_gems.head())

fig, ax = plt.subplots(figsize=(8,8))

geo_gems.plot(ax=ax, edgecolor='gray', column=selectie_col, legend=True);
# plt.show()

fig, ax = plt.subplots(figsize=(8,8))

geo_gems.plot(column=selectie_col, scheme='Quantiles', k=5, edgecolor='gray', 
              cmap='Blues', legend=True, ax=ax);

plt.show()

gdf_gem_choro = geo_gems.copy()

gdf_gem_choro['geoid'] = gdf_gem_choro.index.astype(str)
gdf_gem_choro = gdf_gem_choro[['geoid', selectie_col, 'statnaam', 'geometry']]

print(gdf_gem_choro.head(3))

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
folium.Choropleth(geo_data=gdf_gem_choro,
                  data=gdf_gem_choro,
                  columns=['geoid', selectie_col],
                  key_on='feature.id',
                  fill_color='Blues',                  
                  legend_name='Gemiddeld persoonlijk inkomen in Nederland'
                 ).add_to(map_nld)
# Toon resultaat
 
# Voeg tooltips toe
folium.features.GeoJson(data=gdf_gem_choro,                        
                        style_function=lambda x: {'color':'transparent','fillColor':'transparent','weight':0},
                        tooltip=folium.features.GeoJsonTooltip(fields=['statnaam', selectie_col],
                                                               aliases=['Gemeente', 'Inkomen'],
                                                               labels=True)
                       ).add_to(map_nld)

# Toon resultaat
map_nld.save('map.html')