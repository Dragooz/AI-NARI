# to use google earth engine
import ee

# Import the folium library.
import folium
from folium import plugins
from folium.plugins.draw import Draw
from folium import IFrame

#utils
from . import utils
import base64

class Markers:
  def __init__(self, latitude_list, longitude_list, marker_name_list, color_list, icon_color_list, popup):
    self.latitude_list = latitude_list
    self.longitude_list = longitude_list
    self.marker_name_list = marker_name_list
    self.color_list = color_list
    self.icon_color_list = icon_color_list
    self.popup = popup

# Authenticate to use Google Earth
def getAuth():
    ## Trigger the authentication flow. You only need to do this once
    ee.Authenticate()

    # Initialize the library.
    ee.Initialize()

def getBaseMap():
    # Add custom basemaps to folium
    basemaps = {
        'Google Maps': folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            attr='Google',
            name='Google Maps',
            overlay=True,
            control=True
        ),
        'Google Satellite': folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='Google',
            name='Google Satellite',
            overlay=True,
            control=True
        ),
        'Google Terrain': folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
            attr='Google',
            name='Google Terrain',
            overlay=True,
            control=True
        ),
        'Google Satellite Hybrid': folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
            attr='Google',
            name='Google Satellite',
            overlay=True,
            control=True
        ),
        'Esri Satellite': folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Esri Satellite',
            overlay=True,
            control=True
        )
    }
    return basemaps


# Define a method for displaying Earth Engine image tiles on a folium map.
def add_ee_layer(self, ee_object, vis_params, name):
    try:
        # display ee.Image()
        if isinstance(ee_object, ee.image.Image):
            map_id_dict = ee.Image(ee_object).getMapId(vis_params)
            folium.raster_layers.TileLayer(
                tiles=map_id_dict['tile_fetcher'].url_format,
                attr='Google Earth Engine',
                name=name,
                overlay=True,
                control=True
            ).add_to(self)
        # display ee.ImageCollection()
        elif isinstance(ee_object, ee.imagecollection.ImageCollection):
            ee_object_new = ee_object.mosaic()
            map_id_dict = ee.Image(ee_object_new).getMapId(vis_params)
            folium.raster_layers.TileLayer(
                tiles=map_id_dict['tile_fetcher'].url_format,
                attr='Google Earth Engine',
                name=name,
                overlay=True,
                control=True
            ).add_to(self)
        # display ee.Geometry()
        elif isinstance(ee_object, ee.geometry.Geometry):
            folium.GeoJson(
                data=ee_object.getInfo(),
                name=name,
                overlay=True,
                control=True
            ).add_to(self)
        # display ee.FeatureCollection()
        elif isinstance(ee_object, ee.featurecollection.FeatureCollection):
            ee_object_new = ee.Image().paint(ee_object, 0, 2)
            map_id_dict = ee.Image(ee_object_new).getMapId(vis_params)
            folium.raster_layers.TileLayer(
                tiles=map_id_dict['tile_fetcher'].url_format,
                attr='Google Earth Engine',
                name=name,
                overlay=True,
                control=True
            ).add_to(self)

    except:
        print("Could not display {}".format(name))

#-------------polygon----------------------------------

# Add drawing polygon method to folium.
def addDrawPolygonFunction():
    drawItem = Draw(
        export=True,
        filename="my_data.geojson",
        position="topleft",
        draw_options={
            "polyline": True,
            "rectangle": False,
            "circle": False,
            "circlemarker": False,
        },
        edit_options={"poly": {"allowIntersection": False}},
    )

    return drawItem

# Method to create a custom polygon area with pop up
# TODO pending modification
def addCustomPolygon():
    # Create feature group to add to folium.Map object
    layer = folium.FeatureGroup(name='your layer name', show=False)

    # load GEOJSON, but don't add it to anything
    temp_geojson = folium.GeoJson('map.geojson')

    # iterate over GEOJSON, style individual features, and add them to FeatureGroup
    for feature in temp_geojson.data['features']:
        # GEOJSON layer consisting of a single feature
        temp_layer = folium.GeoJson(feature
                                    )
        # lambda to add HTML
        foo = lambda name, source: f"""
            <iframe id="popupIFrame"
                title="{name}"
                width="600"
                height="500"
                align="center"
                src="{source}">
            </iframe>
            """
        # create Popup and add it to our lone feature
        # this example embeds a .png
        folium.Popup(
            html=foo('name of your IFrame',
                     f'https://www.extremetech.com/wp-content/uploads/2019/12/SONATA-hero-option1-764A5360-edit.jpg')
        ).add_to(temp_layer)

        # folium.Popup(
        #     html="Html here"
        # ).add_to(temp_layer)

        # consolidate individual features back into the main layer
        temp_layer.add_to(layer)

    # add main layer to folium.Map object
    # layer.add_to(my_map)


    # folium.Marker(
    #     location=[2.226888, 103.169322], # coordinates for the marker (Earth Lab at CU Boulder)
    #     popup='Earth Lab at CU Boulder', # pop-up label for the marker
    #     icon=folium.Icon()
    # ).add_to(my_map)

    # my_map.add_child(folium.Marker(
    #     location=[2.226888, 102.166440], # coordinates for the marker (Earth Lab at CU Boulder)
    #     popup='Earth Lab at CU Boulder', # pop-up label for the marker
    #     icon=folium.Icon()
    # ))

    # Set visualization parameters.
    # vis_params = {
    #     'min': 0,
    #     'max': 4000,
    #     'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}

#map


def getMap(paddy_area_info=None, colour=None, ee=False):
    if ee:
        # Authenticate to use google earth
        getAuth()

        # Get the google earth base maps
        basemaps = getBaseMap()

        # Add EE drawing method to folium.
        folium.Map.add_ee_layer = add_ee_layer

    # Create a folium map object.
    my_map = folium.Map(location=[paddy_area_info[0].paddy_area.latitude, 
                                paddy_area_info[0].paddy_area.longitude], 
                        zoom_start=20)

    # no pre-defined markers - Default
    if paddy_area_info == None:
        lat_lst = [2.226888, 2.226888, 2.226888]
        lng_lst = [102.166600, 102.166440, 102.166200]
        name_lst = ['aa', 'bb', 'cc']
        color_lst = ['green', 'orange', 'red']
        color_lst2 = ['purple', '#FFFF00', 'red']
        feature_group = folium.FeatureGroup("Paddy Areas")

        for lat, lng, name, col, col2 in zip(lat_lst, lng_lst, name_lst, color_lst, color_lst2):
            mark = folium.Marker(location=[lat, lng], popup=name, icon=folium.Icon(color=col, icon_color=col2))
            feature_group.add_child(mark)
    else:
        feature_group = folium.FeatureGroup("Paddy Areas")

        #declaring markers
        for i, c in zip(paddy_area_info, colour):
            
            my_image_path = utils.get_image_directory(i.paddy_images.url)
            encoded = base64.b64encode(open(my_image_path, 'rb').read())
            html = '<img src="data:image/png;base64,{}" width="200" height="200">'.format
            iframe = IFrame(html(encoded.decode('UTF-8')), width=220, height=220)
            popup = folium.Popup(iframe, max_width=300)

            mark = folium.Marker(location=[i.paddy_area.latitude, i.paddy_area.longitude], 
                                 popup=popup,
                                 tooltip=i.paddy_area.name,
                                 icon=folium.Icon(color=c, icon_color=None),
                                 )
            feature_group.add_child(mark)

    # add markers as folium layer
    my_map.add_child(feature_group)

    # Add a layer control panel to the map.
    my_map.add_child(folium.LayerControl(position='topleft'))
    plugins.Fullscreen().add_to(my_map)

    # add draw custom polygon function
    addDrawPolygonFunction().add_to(my_map)

    return my_map._repr_html_()