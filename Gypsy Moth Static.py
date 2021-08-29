import plotly.graph_objects as go
import pandas as pd
import numpy as np
from mapbox import Geocoder

geocoder = Geocoder(access_token=".mapbox_tokenN")


def zoom_center(lons: tuple = None, lats: tuple = None, lonlats: tuple = None,
                format: str = 'lonlat', projection: str = 'mercator',
                width_to_height: float = 2.0) -> (float, dict):
    """Finds optimal zoom and centering for a plotly mapbox.
    Must be passed (lons & lats) or lonlats.
    Temporary solution awaiting official implementation, see:
    https://github.com/plotly/plotly.js/issues/3434

    Parameters
    --------
    lons: tuple, optional, longitude component of each location
    lats: tuple, optional, latitude component of each location
    lonlats: tuple, optional, gps locations
    format: str, specifying the order of longitud and latitude dimensions,
        expected values: 'lonlat' or 'latlon', only used if passed lonlats
    projection: str, only accepting 'mercator' at the moment,
        raises `NotImplementedError` if other is passed
    width_to_height: float, expected ratio of final graph's with to height,
        used to select the constrained axis.

    Returns
    --------
    zoom: float, from 1 to 20
    center: dict, gps position with 'lon' and 'lat' keys

#    >>> print(zoom_center((-109.031387, -103.385460),
    ...     (25.587101, 31.784620)))
    (5.75, {'lon': -106.208423, 'lat': 28.685861})
    """
    if lons is None and lats is None:
        if isinstance(lonlats, tuple):
            lons, lats = zip(*lonlats)
        else:
            raise ValueError(
                'Must pass lons & lats or lonlats'
            )

    maxlon, minlon = max(lons), min(lons)
    maxlat, minlat = max(lats), min(lats)
    center = {
        'lon': round((maxlon + minlon) / 2, 6),
        'lat': round((maxlat + minlat) / 2, 6)
    }

    # longitudinal range by zoom level (20 to 1)
    # in degrees, if centered at equator
    lon_zoom_range = np.array([
        0.0007, 0.0014, 0.003, 0.006, 0.012, 0.024, 0.048, 0.096,
        0.192, 0.3712, 0.768, 1.536, 3.072, 6.144, 11.8784, 23.7568,
        47.5136, 98.304, 190.0544, 360.0
    ])

    if projection == 'mercator':
        margin = 1.2
        height = (maxlat - minlat) * margin * width_to_height
        width = (maxlon - minlon) * margin
        lon_zoom = np.interp(width, lon_zoom_range, range(20, 0, -1))
        lat_zoom = np.interp(height, lon_zoom_range, range(20, 0, -1))
        zoom = round(min(lon_zoom, lat_zoom), 2)
    else:
        raise NotImplementedError(
            f'{projection} projection is not implemented'
        )

    return zoom, center


df = pd.read_csv('combined_csv.csv')
df.head()
# limit the geographical distribution of samples
# selecting rows based on condition, slice of data in the southeast.
# df = df[df['POINT_X'] >= -83.7662048]
# df = df[df['POINT_X'] <= -78.2827988]
# df = df[df['POINT_Y'] <= 38.2089691]
# df = df[df['POINT_Y'] >= 34.3790474]

# selecting rows based on condition, slice of data in the midwest.
# df = df[df['POINT_X'] >= -94.36]
# df = df[df['POINT_X'] <= -83.18]
# df = df[df['POINT_Y'] <= 45.22]
# df = df[df['POINT_Y'] >= 40.6]
df = df[df['year'] == 2016]
min_x = df['POINT_X'].min()
max_x = df['POINT_X'].max()
min_y = df['POINT_Y'].min()
max_y = df['POINT_Y'].max()

df['text'] = '<br>Moths Trapped ' + (df['count']).astype(str)
limits = [(0, 1), (1, 20), (20, 50), (50, 200), (200, 3000)]
colors = ["lightseagreen", "yellow", "orange", "crimson", "red"]
cities = []
scale = 5000

zoom, center = zoom_center(
    lons=[min_x, max_x],
    lats=[min_y - 3, max_y + 4]
)

fig = go.Figure()
for i in range(len(limits)):
    lim = limits[i]
    df_sub = df[(df["count"] >= lim[0]) & (df["count"] < lim[1])]
    fig.add_trace(go.Scattermapbox(
        #        locationmode='USA-states',
        lon=df_sub['POINT_X'],
        lat=df_sub['POINT_Y'],
        text=df_sub['text'],
        marker=dict(
            size=(df_sub['count'] / 1.5 + 10),
            color=colors[i],
            sizemode='area',
        ),
        name='{0} - {1}'.format(lim[0], lim[1])))

fig.update_layout(
    mapbox_style="open-street-map",
    mapbox={'center': center, 'zoom': zoom},
    title_text='1988-2019 Gypsy Moth Trap Data',
    showlegend=True,
)

fig.show()
fig.write_html("2016.html")
