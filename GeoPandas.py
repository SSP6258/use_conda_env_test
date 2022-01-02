import os.path
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import shape, Point
import streamlit as st


def fn_geo_test():
    path = r'D:\02_Project\proj_python\use_conda_env\mapdata202104280245'
    file = r'TOWN_MOI_1100415.shp'
    g = os.path.join(path, file)
    gis_d = gpd.read_file(g, encoding='utf-8')

    path = r'D:\02_Project\proj_python\use_conda_env\mapdata202112240331'
    file = r'VILLAGE_MOI_1101214.shp'
    g = os.path.join(path, file)
    gis_v = gpd.read_file(g, encoding='utf-8')

    gis = gis_v

    # gis.plot()
    # plt.show()
    print(gis.shape)
    print(gis.columns)
    shapes = {}
    properties = {}
    for idx in gis.index:
        county = gis.loc[idx, 'COUNTYNAME']
        town = gis.loc[idx, 'TOWNNAME']
        vill = gis.loc[idx, 'VILLNAME'] if 'VILLNAME' in gis.columns else 'NA'
        s = gis[gis.index==idx]

        if county == '臺北市':
            shapes[idx] = shape(gis.loc[idx, 'geometry'])
            properties[idx] = f'{county}, {town}, {vill}'

    return shapes, properties


def fn_search(x, y, shapes, properties):
    coor_2_vill = 'Uknown1'
    vill = 'Unknown'

    for k in shapes.keys():
        # print(k, properties[k])
        if shapes[k].contains(Point(x, y)):
            vill = properties[k]
            coor_2_vill = f'{x}, {y} is in {vill}'

            x, y = shapes[k].exterior.xy
            plt.plot(x, y, c="red")
            plt.show()
            break

    print(coor_2_vill)

    return vill


def fn_coor_2_vill(lon, lat):
    shapes, properties = fn_geo_test()

    '''
    兒童新樂園	25°05'50.1"N 121°30'53.8"E	台北市	士林區	25.097239, 121.514942
    台北奧萬大	25°08'32.1"N 121°34'10.8"E	台北市	士林區	25.142235, 121.569657
    芝山岩	25°06'07.8"N 121°31'51.7"E	台北市	士林區	25.102158, 121.531014
    '''

    print(len(shapes))
    # fn_search(121.514942, 25.097239, shapes, properties)
    # fn_search(121.569657, 25.142235, shapes, properties)
    fn_search(lon, lat, shapes, properties)


def fn_st_test():
    st.header('Test !')


def fn_main():
    # vill = fn_coor_2_vill(121.531014, 25.102158)
    fn_st_test()



if __name__ == '__main__':
    fn_main()
