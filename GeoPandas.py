import os.path
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import shape, Point
import streamlit as st


def fn_geo_test():
    path = r'./mapdata202104280245'
    file = r'TOWN_MOI_1100415.shp'
    g = os.path.join(path, file)
    gis_d = gpd.read_file(g, encoding='utf-8')

    path = r'./mapdata202112240331'
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


def fn_search(lon, lat, shapes, properties):
    coor_2_vill = 'Uknown1'
    vill = 'Unknown'

    for k in shapes.keys():
        # print(k, properties[k])
        if shapes[k].contains(Point(lon, lat)):
            vill = properties[k]
            coor_2_vill = f'{lon}, {lat} is in {vill}'

            x, y = shapes[k].exterior.xy
            fig = plt.figure()
            plt.plot(x, y, c="green")
            plt.plot(lon, lat, c="red", marker='X')
            break

    print(coor_2_vill)

    return vill, fig


def fn_coor_2_vill(lon, lat):
    shapes, properties = fn_geo_test()

    vill, fig = fn_search(lon, lat, shapes, properties)

    return vill, fig


def fn_st_test():
    st.header('應用: 利用座標查詢行政區!')
    lon = st.text_input('經度:', value="121.531014")
    lat = st.text_input('緯度:', value="25.102158")
    is_click = st.button('按我查詢')
    path = '.\\database'
    output = 'coor_2_vill.csv'
    file = os.path.join(path, output)
    if not os.path.exists(path):
        os.makedirs(path)
        print(f'{path} created !')

    if is_click:
        vill, fig = fn_coor_2_vill(float(lon), float(lat))
        st.write(' ')
        st.subheader(f'此座標的行政區是: {vill} !')
        st.write(' ')
        st.pyplot(fig)

        # check = f'{lon}_{lat}_{vill}'
        # dic_coor = dict(lon=[lon], lat=[lat], vill=[vill], check=[check])
        # df = pd.DataFrame(dic_coor, index=None)
        # df.to_csv(file)
        # print(f' {file} saved !')


def fn_main():
    fn_st_test()


if __name__ == '__main__':
    fn_main()
