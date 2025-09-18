
import flet as ft
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

        self.initial_text = ft.Text(
            "¡Haz clic en el mapa para empezar!",
            size=16,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )

        self.marker_layer = MarkerLayer(markers=[])

        self.map_control = Map(
            layers=[
                TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                ),
                self.marker_layer,
            ],
            initial_center=MapLatitudeLongitude(40.416775, -3.703790), # Centro en Madrid
            initial_zoom=6,
            interaction_configuration=MapInteractionConfiguration(
                flags=MapInteractiveFlag.ALL
            ),
            on_tap=self._handle_map_click,
        )

        self.content = ft.Stack(
            [
                self.map_control,
                ft.Container(
                    content=self.initial_text,
                    alignment=ft.alignment.center,
                    visible=True,
                )
            ]
        )

    def _handle_map_click(self, e: ft.ControlEvent):
        lat, lon = e.data.coordinates.latitude, e.data.coordinates.longitude
        
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
        
        self.content.controls[1].visible = False # Ocultar el texto inicial
        self.on_map_click(lat, lon)
        self.update()
