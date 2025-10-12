import flet as ft
import json
from flet_map import (
    Map,
    Marker,
    MarkerLayer,
    MapLatitudeLongitude,
    TileLayer,
    PolygonMarker,
    PolygonLayer,
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
                PolygonLayer(
                    polygons=[
                        PolygonMarker(
                            #label="Área de Sevilla",
                            color=ft.Colors.with_opacity(0.2, ft.Colors.BLUE_GREY),
                            border_stroke_width=2,
                            border_color=ft.Colors.BLUE_GREY_800,
                            # Define las 4 esquinas para enmarcar Sevilla
                            coordinates=[
                                MapLatitudeLongitude(37.44, -6.04),  # Esquina Superior Izquierda
                                MapLatitudeLongitude(37.44, -5.92),  # Esquina Superior Derecha
                                MapLatitudeLongitude(37.33, -5.92),  # Esquina Inferior Derecha
                                MapLatitudeLongitude(37.33, -6.04),  # Esquina Inferior Izquierda
                            ],
                        ),
                    ],
                ),
            ],
            initial_center=MapLatitudeLongitude(37.3891, -5.9845), # Centro en Sevilla
            initial_zoom=12, # Un zoom más cercano para Sevilla
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
                    src="https://raw.githubusercontent.com/MayumyCH/Airbnb-Pricing-frontend-flet/refs/heads/develop/assets/marcadorMapa2.png",
                    width=100,
                    height=100,
                ),
                coordinates=MapLatitudeLongitude(lat, lon),
            )
        )
        
        self.on_map_click(lat, lon)
        self.update()
