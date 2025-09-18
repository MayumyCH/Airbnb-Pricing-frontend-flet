import flet as ft
import json
from flet_map import (
    Map,
    Marker,
    MarkerLayer,
    MapLatitudeLongitude,
    TileLayer,
    MapInteractionConfiguration,
    MapInteractiveFlag,
)
from typing import Callable

class MapView(ft.Container):
    def __init__(self, on_map_click: Callable):
        super().__init__(expand=True)
        self.on_map_click = on_map_click

        self.marker_layer = MarkerLayer(markers=[])

        self.map_control = Map(
            layers=[
                TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                ),
                self.marker_layer,
            ],
            initial_center=MapLatitudeLongitude(37.38, -5.97), # Centro en Sevilla
            initial_zoom=13, # Un zoom más cercano para Sevilla
            interaction_configuration=MapInteractionConfiguration(
                flags=MapInteractiveFlag.ALL
            ),
            on_tap=self._handle_map_click,
        )

        self.content = self.map_control

    def _handle_map_click(self, e: ft.ControlEvent):
        data = json.loads(e.data)
        lat, lon = data['lat'], data['long']
        
        self.marker_layer.markers.clear()
        self.marker_layer.markers.append(
            Marker(
                content=ft.Image(
                    src="https://raw.githubusercontent.com/fferegrino/cycle-station-predictions/refs/heads/main/frontend/static/location-64.png",
                    width=40,
                    height=40,
                ),
                coordinates=MapLatitudeLongitude(lat, lon),
            )
        )
        
        self.on_map_click(lat, lon)
        self.update()
