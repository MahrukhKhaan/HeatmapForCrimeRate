#Setup
import pandas as pd
import geopandas as gpd
import branca.colormap as cm
import folium
from folium.plugins import TimeSliderChoropleth

#Dataset
#Reading Map file for Karachi sub-divisons/towns
map_df = gpd.read_file('../input/aiproject-database/karachi_towns.json')
map_df.head()

#Reading Data file for Karachi town Crime Rate
data_df = pd.read_csv('../input/aiproject-database/townwise_dummydata.csv')
data_df.head()

#Merging both files
map_df.rename(columns={'title': 'Town'},inplace=True)
data_df.rename(columns={'District': 'Town'},inplace=True)
merged_df= map_df.merge(data_df, on = 'Town', how = 'left')
merged_df.head()#Keeping only data of districts where crime rate data is given
merged_df = merged_df[merged_df['Date'].notna()]

#Dropping extra columns
final_df=merged_df.drop(['wikimapia_id','description','wikipedia_url'], axis = 1) 
final_df['date_sec'] = pd.to_datetime(final_df['Date']).astype(int) / 10**9
final_df['date_sec'] = final_df['date_sec'].astype(int).astype(str)
final_df.head()

#Color-bar
max_colour = max(final_df['Total'])
min_colour = min(final_df['Total'])
colour_bar = cm.linear.YlOrRd_09.scale(min_colour, max_colour)
final_df['colour'] = final_df['Total'].map(colour_bar)
print("maximum value of Colour bar:",max_colour)
print("minimum value of Colour bar:",min_colour)
final_df.head()

#Slider
##styledict
town_list = final_df['Town'].unique().tolist()
town_index = range(len(town_list))
style_dict = {}
for i in town_index:
    town_name = town_list[i]
    result = final_df[final_df['Town'] == town_name]
    inner_dict = {}
    for row_index, row in result.iterrows():
        inner_dict[row['date_sec']] = {'color': row['colour'], 'opacity': 0.7}
    style_dict[str(i)] = inner_dict

print(style_dict)

##data
towngeometry_df = final_df[['geometry']]
towngeometry_gdf = gpd.GeoDataFrame(towngeometry_df)
towngeometry_gdf = towngeometry_gdf.drop_duplicates().reset_index()
towngeometry_gdf

slider_map = folium.Map(location=[25.2207, 67.1411], min_zoom=2,zoom_start=8.5, max_bounds=True,tiles='cartodbpositron')
TimeSliderChoropleth(data=towngeometry_gdf.to_json(),styledict=style_dict,).add_to(slider_map)
colour_bar.add_to(slider_map)
colour_bar.caption = "Number  of  Crime  Cases"
slider_map

#Reading Map file for Karachi Districts
map_df2 = gpd.read_file('../input/aiproject-database/pakistan-districts.json')
map_df2.head()

#Reading Data file for Karachi district Crime Rate
data_df2 = pd.read_csv('../input/aiproject-database/districtwise_data.csv')
data_df2.head()

#Merging both files
map_df2.rename(columns={'NAME_3': 'District'},inplace=True)
merged_df2= map_df2.merge(data_df2, on = 'District', how = 'left')
merged_df2.head()

#Keeping only data of districts where crime rate data is given
final_df2 = merged_df2[merged_df2['Date'].notna()]
#Dropping extra columns
final_df2=final_df2.drop(['id', 'ID_0','ISO','NAME_0','NAME_1','NAME_2','ID_1','ID_2','ID_3','TYPE_3','ENGTYPE_3','NL_NAME_3','VARNAME_3'], axis = 1) 

final_df2['date_sec'] = pd.to_datetime(final_df2['Date']).astype(int) / 10**9
final_df2['date_sec'] = final_df2['date_sec'].astype(int).astype(str)
final_df2.head()

#Color-bar
max_colour2 = max(final_df2['Total'])
min_colour2 = min(final_df2['Total'])
colour_bar2 = cm.linear.YlOrRd_09.scale(min_colour2, max_colour2)
final_df2['colour'] = final_df2['Total'].map(colour_bar)
print("maximum value of Colour bar:",max_colour)
print("minimum value of Colour bar:",min_colour)
final_df2.head()

#Slider
##style_dict
district_list = final_df2['District'].unique().tolist()
district_index = range(len(district_list))
style_dict2 = {}
for i in district_index:
    district_name = district_list[i]
    result2 = final_df2[final_df2['District'] == district_name]
    inner_dict2 = {}
    for row_index2, row2 in result2.iterrows():
        inner_dict2[row2['date_sec']] = {'color': row2['colour'], 'opacity': 0.7}
    style_dict2[str(i)] = inner_dict2
print(style_dict2)

##data
distgeometry_df = final_df2[['geometry']]
distgeometry_gdf = gpd.GeoDataFrame(distgeometry_df)
distgeometry_gdf = distgeometry_gdf.drop_duplicates().reset_index()
distgeometry_gdf.head()

slider_map2 = folium.Map(location=[25.0007, 67.0011], min_zoom=2, max_bounds=True,tiles='cartodbpositron')
TimeSliderChoropleth(data=distgeometry_gdf.to_json(),styledict=style_dict2,).add_to(slider_map2)
colour_bar2.add_to(slider_map2)
colour_bar2.caption = "Number  of  Crime  Cases"

#Markers
div1 = folium.DivIcon(html=('<svg height="50" width="50">'
    '<text x="10" y="10" fill="black">East</text>'
    '</svg>'))
div2 = folium.DivIcon(html=('<svg height="50" width="50">'
    '<text x="10" y="10" fill="black">West</text>'
    '</svg>'))
div3 = folium.DivIcon(html=('<svg height="50" width="50">'
    '<text x="10" y="10" fill="black">South</text>'
    '</svg>'))
div4 = folium.DivIcon(html=('<svg height="50" width="50">'
    '<text x="10" y="10" fill="black">Central</text>'
    '</svg>'))
folium.Marker((24.8832, 67.1060), icon=div1).add_to(slider_map2)
folium.Marker([24.9713, 66.9511], icon=div2).add_to(slider_map2) 
folium.Marker([24.8625, 67.0046], icon=div3).add_to(slider_map2) 
folium.Marker([24.9551, 67.0044], icon=div4).add_to(slider_map2) 

slider_map2
