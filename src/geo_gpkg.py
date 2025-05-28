import pandas as pd
import geopandas as gpd

""" CBS geopackage Layers
'cbs_arrondissementsgebied_2022_gegeneraliseerd', 'cbs_buurt_2022_gegeneraliseerd', 
'cbs_buurt_2022_labelpoint', 'cbs_coropgebied_2022_gegeneraliseerd', 
'cbs_coropplusgebied_2022_gegeneraliseerd', 'cbs_coropsubgebied_2022_gegeneraliseerd', 
'cbs_gemeente_2022_gegeneraliseerd', 'cbs_ggdregio_2022_gegeneraliseerd', 
'cbs_jeugdregio_2022_gegeneraliseerd', 'cbs_kamervankoophandelregio_2022_gegeneraliseerd', 
'cbs_landbouwgebied_2022_gegeneraliseerd', 'cbs_landbouwgroep_2022_gegeneraliseerd', 
'cbs_landsdeel_2022_gegeneraliseerd', 'cbs_provincie_2022_gegeneraliseerd', 
'cbs_regionaalmeld_coordinatiepunt_2022_gegeneraliseerd', 
'cbs_regionale_energiestrategie_2022_gegeneraliseerd', 
'cbs_regioplus_arbeidsmarktregio_2022_gegeneraliseerd', 'cbs_ressort_2022_gegeneraliseerd', 
'cbs_subres_regio_2022_gegeneraliseerd', 'cbs_toeristengebied_2022_gegeneraliseerd', 
'cbs_toeristengroep_2022_gegeneraliseerd', 'cbs_veiligheidsregio_2022_gegeneraliseerd', 
'cbs_veiligthuisregio_2022_gegeneraliseerd', 'cbs_wijk_2022_gegeneraliseerd', 
'cbs_wijk_2022_labelpoint', 'cbs_zorgkantoorregio_2022_gegeneraliseerd', 
'cbs_buurt_2022_niet_gegeneraliseerd', 'cbs_gemeente_2022_niet_gegeneraliseerd', 
'cbs_wijk_2022_niet_gegeneraliseerd', 'cbs_arbeidsmarktregio_2022_labelpoint', 
'cbs_arrondissementsgebied_2022_labelpoint', 'cbs_coropgebied_2022_labelpoint', 
'cbs_coropplusgebied_2022_labelpoint', 'cbs_coropsubgebied_2022_labelpoint', 
'cbs_gemeente_2022_labelpoint', 'cbs_ggdregio_2022_labelpoint', 
'cbs_jeugdregio_2022_labelpoint', 'cbs_kamervankoophandelregio_2022_labelpoint', 
'cbs_landbouwgebied_2022_labelpoint', 'cbs_landbouwgroep_2022_labelpoint', 
'cbs_landsdeel_2022_labelpoint', 'cbs_provincie_2022_labelpoint', 
'cbs_regionaalmeld_coordinatiepunt_2022_labelpoint', 
'cbs_regionale_energiestrategie_2022_labelpoint', 
'cbs_regioplus_arbeidsmarktregio_2022_labelpoint', 
'cbs_ressort_2022_labelpoint', 'cbs_subres_regio_2022_labelpoint', 
'cbs_toeristengebied_2022_labelpoint', 'cbs_toeristengroep_2022_labelpoint', 
'cbs_veiligheidsregio_2022_labelpoint', 'cbs_veiligthuisregio_2022_labelpoint', 
'cbs_zorgkantoorregio_2022_labelpoint'
"""

geo_pkg = '/media/i-files/data/geo_nl_cbs/gebieden-gpkg/cbsgebiedsindelingen2022.gpkg'
gemeenten = gpd.read_file(geo_pkg, layer = 'cbs_gemeente_2022_gegeneraliseerd')

print(gemeenten.columns)
# print(data.loc[1])

gemeente = gemeenten.loc[gemeenten['statnaam'] == 'Bronckhorst']
print(gemeente.iloc[0, [0,1,2,3,4]])
borders = gemeente['geometry']

