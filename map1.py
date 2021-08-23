import folium
import pandas


def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'


def main():
    data = pandas.read_csv("Volcanoes.txt")
    lat_list = list(data["LAT"])
    long_list = list(data["LON"])
    elev_list = list(data["ELEV"])

    # Adjust popup text with html
    html = """<h4>Volcano information:</h4>
    <li>Height: %sm</li>
    """

    # Set starting location on load
    map = folium.Map(location=[38.58, -99.09],
                     zoom_start=6, tiles="Stamen Terrain")

    fgv = folium.FeatureGroup(name="Volcanoes")

    # Pin the volcanoes on the map
    for lt, ln, el in zip(lat_list, long_list, elev_list):
        iframe = folium.IFrame(html=html % str(el), width=200, height=100)
        fgv.add_child(folium.CircleMarker(
            location=[lt, ln], popup=folium.Popup(iframe), color='gray',
            fill_color=color_producer(el), radius=6, fill_opacity=0.7))

    fgp = folium.FeatureGroup(name="Population")

    # Set the population of each country and also set the country name
    fgp.add_child(folium.GeoJson(
        data=open("world.json", "r", encoding="utf-8-sig").read(), style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000 else 'orange'
                                                                                             if x['properties']['POP2005'] < 20000000 else 'red'}))

    map.add_child(fgv)
    map.add_child(fgp)
    map.add_child(folium.LayerControl())
    map.save("Map1.html")


if __name__ == "__main__":
    main()
