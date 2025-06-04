import sys
import shapely
import warnings
# warnings.filterwarnings('ignore')

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

from grid_viewer import GridViewMatrix
from grid_generators import GridMatrix

class DrawPolygons(object):
    def __init__(self, rows, cols):

        self.rows = rows
        self.cols = cols

        self.matrix =         # create a grid with appropriate number of columns and rows
        grid = generator.generate(
            grid_size = (self.rows, self.cols), 
            res_path = self.res_path, 
            icon_style = self.icon_style,
            config = self.config_model,
            generator_function = self.generator_function,
        )

        # define a grid viewer for the grid
        self.grid_viewer = GridViewMatrix(
            grid = self.matrix, 
            definitions = None, #Thing.definitions, 
            screen_size = (self.rows, self.cols),
        )
        

        return
    
    ### __Init__ ###

    def analyse_polygon(self, df: pd.DataFrame):
        cell = df.loc[0, 'geometry']
        print(type(cell))
        print(dir(cell))
        print(cell.length)
        print(cell.centroid)
        # print(cell.boundary)

        poly = list(cell.geoms)
        print(len(poly))

        points = shapely.points(poly[0].exterior.coords)
        # print(int(points.length))
        for point in points:
            print(f'{point.x:12.5f} - {point.y:12.5f}')


        return
    
    ### analyse_polygon ###


    def count_polygons(self, geo_gems):
        for idx in geo_gems.index:
            gem = geo_gems.loc[idx]
            # print(gem)
            cell = gem['geometry']
            poly = list(cell.geoms)
            # print(gem.index)
            if len(poly) > 2:
                print(gem['statnaam'], len(poly), cell.centroid)
                for polygon in poly:
                    print(polygon.length, polygon.centroid)

            # if
        # for

        return
    
    ### count_polygons ###


    def display(self):
        # create a grid with appropriate number of columns and rows
        grid = generator.generate(
            grid_size = (self.rows, self.cols), 
            res_path = self.res_path, 
            icon_style = self.icon_style,
            config = self.config_model,
            generator_function = self.generator_function,
        )
        self.initial_seed(grid, 'I')

        grid.create_recorder(Thing.definitions, self.epochs)
    
        # define a grid viewer for the grid
        grid_viewer = GridViewMatrix(
            grid = grid, 
            definitions = Thing.definitions, 
            screen_size = (self.screen_width, self.screen_height),
        )
        
        grid_viewer.update_screen(pars)

        return
    
### Class: DrawPolygon ###


geo_pkg = '/media/i-files/data/geo_nl_cbs/gebieden-gpkg/cbsgebiedsindelingen2022.gpkg'
geo_gems = gpd.read_file(geo_pkg, layer = 'cbs_gemeente_2022_gegeneraliseerd')

dp = DrawPolygons(1000, 1000)

print('\nBounding box', geo_gems.total_bounds)


geo_gems['area'] = geo_gems.area

# print(geo_gems.head())
# print(geo_gems.crs)
count_polygons(geo_gems)

sys.exit()

"""
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
"""