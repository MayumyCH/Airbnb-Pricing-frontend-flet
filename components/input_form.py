
import flet as ft
from typing import Callable

class InputForm(ft.Column):
    def __init__(self, on_submit: Callable):
        super().__init__(spacing=15, expand=True)
        self.on_submit_callback = on_submit
        self._is_disabled = True

        # --- Estilo común para campos de texto ---
        textfield_style = {
            "bgcolor": "#3C4046",
            "border_width": 0,
            "border_radius": 10,
            "text_size": 14,
        }

        # --- Campos del formulario ---
        self.lat_field = ft.TextField(label="Latitud", read_only=True, **textfield_style)
        self.lon_field = ft.TextField(label="Longitud", read_only=True, **textfield_style)
        self.guests_field = ft.TextField(label="Huéspedes", value="2", keyboard_type=ft.KeyboardType.NUMBER, **textfield_style)
        self.rooms_field = ft.TextField(label="Habitaciones", value="1", keyboard_type=ft.KeyboardType.NUMBER, **textfield_style)
        self.beds_field = ft.TextField(label="Camas", value="1", keyboard_type=ft.KeyboardType.NUMBER, **textfield_style)
        self.nights_field = ft.TextField(label="Noches", value="3", keyboard_type=ft.KeyboardType.NUMBER, **textfield_style)

        # --- Botón de envío ---
        self.submit_button = ft.Container(
            content=ft.Text("Calcular Precio Estimado 🪄", size=14, weight=ft.FontWeight.BOLD),
            width=float("inf"),
            padding=ft.padding.all(15),
            alignment=ft.alignment.center,
            border_radius=10,
            on_click=self._handle_submit_click,
        )
        self._update_button_style() # Aplicar estilo inicial

        self.controls = [
            ft.Text("Detalles de la Propiedad ✨", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([self.lat_field, self.lon_field], spacing=10),
            ft.Row([self.guests_field, self.rooms_field], spacing=10),
            ft.Row([self.beds_field, self.nights_field], spacing=10),
            self.submit_button,
        ]

    def _handle_submit_click(self, e):
        if not self._is_disabled:
            self.on_submit_callback(e)

    def _update_button_style(self):
        if self._is_disabled:
            self.submit_button.bgcolor = "#44484E" # Gris oscuro para deshabilitado
            self.submit_button.content.opacity = 0.5
        else:
            self.submit_button.bgcolor = "#4A90E2" # Azul para habilitado
            self.submit_button.content.opacity = 1.0

    def update_location(self, lat: float, lon: float):
        self.lat_field.value = f"{lat:.4f}"
        self.lon_field.value = f"{lon:.4f}"
        self._is_disabled = False
        self._update_button_style()
        self.update()

    def get_data(self) -> dict:
        return {
            "latitude": float(self.lat_field.value),
            "longitude": float(self.lon_field.value),
            "guests": int(self.guests_field.value or 0),
            "rooms": int(self.rooms_field.value or 0),
            "beds": int(self.beds_field.value or 0),
            "nights": int(self.nights_field.value or 0),
        }

