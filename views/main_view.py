
import flet as ft
from components.map_view import MapView
from components.input_form import InputForm
from components.result_panel import ResultPanel
from services import api_client

class MainView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, padding=ft.padding.all(20))
        self.page = page

        # --- Instancias de los componentes ---
        self.map_view = MapView(on_map_click=self._handle_map_click)
        self.input_form = InputForm(on_submit=self._handle_submit)
        self.result_panel = ResultPanel()
        self.progress_ring = ft.ProgressRing(width=32, height=32, stroke_width=4)

        # --- Paneles ---
        self.result_container = ft.Container(
            content=self.progress_ring,
            alignment=ft.alignment.center,
            expand=True
        )
        self.result_container.visible = False

        # --- Contenedor para el formulario y los resultados ---
        self.right_panel_content = ft.Column([
            self.input_form,
            self.result_container
        ], spacing=20, scroll=ft.ScrollMode.AUTO) # Permitir scroll si el contenido excede

        # --- Layout Principal en Fila ---
        self.main_layout = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(self.map_view, expand=1, padding=ft.padding.all(10)),
                ft.VerticalDivider(width=1),
                ft.Container(self.right_panel_content, expand=1, padding=ft.padding.all(20)),
            ]
        )

        # --- Card principal ---
        self.main_card = ft.Card(
            elevation=8,
            color="#2D3035",
            content=self.main_layout,
            expand=True # Asegurar que la tarjeta se expanda
        )

        # --- Layout Principal ---
        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Estimador de Precios Airbnb", style=ft.TextThemeStyle.HEADLINE_LARGE, weight=ft.FontWeight.BOLD),
                ft.Text("Usa IA para encontrar el precio óptimo para tu propiedad", style=ft.TextThemeStyle.HEADLINE_SMALL, color=ft.Colors.BLUE_GREY_400),
                ft.Divider(),
                self.main_card
            ]
        )

    def _handle_map_click(self, lat: float, lon: float):
        self.input_form.update_location(lat, lon)

    async def _handle_submit(self, e: ft.ControlEvent):
        self.result_panel.visible = False
        self.result_container.content = self.progress_ring
        self.result_container.visible = True
        self.page.update()

        form_data = self.input_form.get_data()
        print(f"Form data submitted: {form_data}") # <-- DEBUG
        api_response = await api_client.get_price_suggestion(form_data)

        if "error" in api_response:
            self.page.snack_bar = ft.SnackBar(ft.Text(api_response["error"]), bgcolor=ft.Colors.RED_700)
            self.page.snack_bar.open = True
            self.result_container.visible = False
        else:
            self.result_panel.update_data(api_response)
            self.result_container.content = self.result_panel
        
        self.page.update()
