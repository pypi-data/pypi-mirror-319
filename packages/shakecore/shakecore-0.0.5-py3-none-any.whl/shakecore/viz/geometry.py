import numpy as np
import plotly.graph_objects as go

from shakecore.utils import latlon_2_utm


def geometry(
    self,
    mode="2d",  # "2d" or "3d"
    axis="latlon",  # 'latlon' or 'xy'
    template="plotly",  # "plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"
    style="open-street-map",  # "open-street-map", "stamen-terrain", "stamen-toner", "stamen-watercolor"
    marker_size=10,
    marker_color="brown",
    marker_opacity=1.0,
    marker_colorscale="Viridis",
    show_marker_colorscale=False,
    line_width=3,
    line_color="yellow",
    mapbox_access_token=None,
    zoom_level=None,
    origin_3d=[0, 0],
    xlim_3d=[None, None],
    ylim_3d=[None, None],
    zlim_3d=[None, None],
    width=900,
    height=700,
    show=True,
    save_path=None,
    dpi=100,
):
    """
    Plot the map in the stream.

    parameters
    ----------
    mode : str
        map mode
    style : str
        map style (openstreetmap, stamen_terrain, stamen_toner, stamen_watercolor, )
    """

    # use the following values (maybe include np.nan, but no effects) to plot
    network = np.array(self.stats.network)
    station = np.array(self.stats.station)
    location = np.array(self.stats.location)
    channel = np.array(self.stats.channel)
    latitude = np.array(self.stats.latitude)
    longitude = np.array(self.stats.longitude)
    elevation = np.array(self.stats.elevation)
    x = np.array(self.stats.x) - origin_3d[0]
    y = np.array(self.stats.y) - origin_3d[1]

    # remove nan is only used for calculating zoom level and center
    lat = latitude[~np.isnan(latitude)]
    lon = longitude[~np.isnan(longitude)]
    # elev = elevation[~np.isnan(elevation)]
    lat_center = (np.max(lat) + np.min(lat)) / 2
    lon_center = (np.max(lon) + np.min(lon)) / 2
    lat_range = np.max(lat) - np.min(lat)
    lon_range = np.max(lon) - np.min(lon)

    # check zoom
    if zoom_level is not None:
        zoom_level = zoom_level
    elif lat_range > 120 or lon_range > 180:
        zoom_level = 0
    elif lat_range > 90 or lon_range > 120:
        zoom_level = 1
    elif lat_range > 60 or lon_range > 60:
        zoom_level = 2
    elif lat_range > 30 or lon_range > 30:
        zoom_level = 3
    elif lat_range > 15 or lon_range > 15:
        zoom_level = 4
    elif lat_range > 8 or lon_range > 8:
        zoom_level = 5
    elif lat_range > 4 or lon_range > 4:
        zoom_level = 6
    elif lat_range > 2 or lon_range > 2:
        zoom_level = 7
    elif lat_range > 1 or lon_range > 1:
        zoom_level = 8
    elif lat_range > 0.5 or lon_range > 0.5:
        zoom_level = 9
    elif lat_range > 0.25 or lon_range > 0.25:
        zoom_level = 10
    elif lat_range > 0.125 or lon_range > 0.125:
        zoom_level = 11
    elif lat_range > 0.0625 or lon_range > 0.0625:
        zoom_level = 12
    elif lat_range > 0.03125 or lon_range > 0.03125:
        zoom_level = 13
    elif lat_range > 0.015625 or lon_range > 0.015625:
        zoom_level = 14
    elif lat_range > 0.0078125 or lon_range > 0.0078125:
        zoom_level = 15
    elif lat_range > 0.00390625 or lon_range > 0.00390625:
        zoom_level = 16
    elif lat_range > 0.001953125 or lon_range > 0.001953125:
        zoom_level = 17
    elif lat_range > 0.0009765625 or lon_range > 0.0009765625:
        zoom_level = 18
    elif lat_range > 0.00048828125 or lon_range > 0.00048828125:
        zoom_level = 19
    elif lat_range > 0.000244140625 or lon_range > 0.000244140625:
        zoom_level = 20
    elif lat_range > 0.0001220703125 or lon_range > 0.0001220703125:
        zoom_level = 21
    else:
        zoom_level = 22

    fig = go.Figure()
    if mode == "2d":
        # check if it is a line geometry
        if self.stats.interval > 0.0:
            fig.add_trace(
                go.Scattermapbox(
                    lat=latitude,
                    lon=longitude,
                    mode="lines",
                    name="sensor line",
                    line=dict(
                        color=line_color,
                        width=line_width,
                    ),
                    hoverinfo="none",
                )
            )

        # plot stations
        text = []
        for i in range(len(latitude)):
            content = f"network {network[i]}<br>station: {station[i]}<br>location: {location[i]}<br>channel: {channel[i]}<br>latitude: {latitude[i]}<br>longitude: {longitude[i]}<br>elevation: {elevation[i]}<br>x: {x[i]}<br>y: {y[i]}"
            text.append(content)

        if show_marker_colorscale:
            color = elevation
            showscale = True
        else:
            color = marker_color
            showscale = False

        marker = go.scattermapbox.Marker(
            size=marker_size,
            color=color,
            colorscale=marker_colorscale,
            showscale=showscale,
            sizemode="diameter",
            colorbar=dict(len=0.6, title="elevation (m)"),
            opacity=marker_opacity,
        )
        fig.add_trace(
            go.Scattermapbox(
                lat=latitude,
                lon=longitude,
                mode="markers",
                marker=marker,
                text=text,
                hoverinfo="text",
                textposition="bottom right",
                name="sensor",
            )
        )

        # set layout
        fig.update_layout(
            autosize=False,
            width=width,
            height=height,
            hovermode="closest",
            template=template,
            mapbox=go.layout.Mapbox(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=go.layout.mapbox.Center(lat=lat_center, lon=lon_center),
                pitch=0,
                zoom=zoom_level,
                style=style,
            ),
            showlegend=True,
        )
    elif mode == "3d":
        dx = 0.1 * (np.max(x) - np.min(x))
        dy = 0.1 * (np.max(y) - np.min(y))
        dz = 0.1 * (np.max(elevation) - np.min(elevation))
        if self.stats.interval > 0.0:
            fig.add_trace(
                go.Scatter3d(
                    x=x,
                    y=y,
                    z=elevation,
                    mode="lines",
                    name="sensor line",
                    line=dict(
                        color=line_color,
                        width=line_width,
                    ),
                    hoverinfo="none",
                )
            )

        # plot stations
        text = []
        for i in range(len(x)):
            content = f"network {network[i]}<br>station: {station[i]}<br>location: {location[i]}<br>channel: {channel[i]}<br>latitude: {latitude[i]}<br>longitude: {longitude[i]}<br>elevation: {elevation[i]}<br>x: {x[i]}<br>y: {y[i]}"
            text.append(content)

        if show_marker_colorscale:
            color = elevation
            showscale = True
        else:
            color = marker_color
            showscale = False

        marker = dict(
            size=marker_size,
            color=color,
            colorscale=marker_colorscale,
            showscale=showscale,
            sizemode="diameter",
            colorbar=dict(len=0.6, title="elevation (m)"),
            opacity=marker_opacity,
        )
        fig.add_trace(
            go.Scatter3d(
                x=x,
                y=y,
                z=elevation,
                mode="markers",
                marker=marker,
                text=text,
                hoverinfo="text",
                textposition="bottom right",
                name="sensor",
            )
        )
        if xlim_3d[0] is None and xlim_3d[1] is None:
            xlim_3d = [np.min(x) - dx, np.max(x) + dx]
        if ylim_3d[0] is None and ylim_3d[1] is None:
            ylim_3d = [np.min(y) - dy, np.max(y) + dy]
        if zlim_3d[0] is None and zlim_3d[1] is None:
            zlim_3d = [np.min(elevation) - dz, np.max(elevation) + dz]

        fig.update_layout(
            autosize=False,
            width=width,
            height=height,
            hovermode="closest",
            template=template,
            geo=dict(projection_type="mercator"),
            showlegend=True,
            scene=dict(
                xaxis_title="x (m)",
                yaxis_title="y (m)",
                zaxis_title="elevation (m)",
                xaxis=dict(range=xlim_3d),
                yaxis=dict(range=ylim_3d),
                zaxis=dict(range=zlim_3d),
            ),
        )
    else:
        raise ValueError("mode must be 'map' or '3d'")

    # save and show
    if show:
        fig.show()
    if save_path is not None:
        if save_path.endswith(".html"):
            fig.write_html(save_path)
        else:
            fig.write_image(save_path, scale=dpi / 72)
