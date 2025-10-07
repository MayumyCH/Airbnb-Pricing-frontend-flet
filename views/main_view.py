import flet as ft
import asyncio
from components.map_view import MapView
from components.input_form import InputForm
from components.result_panel import ResultPanel
from services import api_client

class MainView(ft.Container):
    def __init__(self, page: ft.Page):
        # El contenedor principal ya no se expande, para permitir el scroll de la página
        super().__init__(padding=ft.padding.all(20))
        self.page = page

        # --- Instancias de los componentes ---
        self.map_view = MapView(on_map_click=self._handle_map_click)
        self.input_form = InputForm(on_submit=self._handle_submit)
        self.result_panel = ResultPanel(on_edit=self._handle_edit_request)
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
        ], spacing=20, scroll=ft.ScrollMode.AUTO)

        # --- Layout Principal Responsivo ---
        self.map_container = ft.Container(
            content=self.map_view,
            padding=ft.padding.all(10),
            height=350, # Altura fija para el mapa
            col={"xs": 12, "md": 6, "lg": 6},
            animate_size=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
        )
        self.right_panel_container = ft.Container(
            content=self.right_panel_content,
            padding=ft.padding.all(20),
            col={"xs": 12, "md": 6, "lg": 6},
            animate_size=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
        )
        self.main_layout = ft.ResponsiveRow(
            controls=[
                self.map_container,
                self.right_panel_container,
            ],
            # ResponsiveRow ya no se expande para que la página pueda hacer scroll
        )

        # --- Card principal ---
        self.main_card = ft.Card(
            elevation=8,
            color="#2D3035",
            content=self.main_layout,
            # La Card ya no se expande para permitir el scroll
        )

        # --- Layout de la Vista ---
        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Estimador de Precios Airbnb", theme_style=ft.TextThemeStyle.HEADLINE_LARGE, weight=ft.FontWeight.BOLD),
                ft.Text("Usa IA para encontrar el precio óptimo para tu propiedad", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, color=ft.Colors.BLUE_GREY_400),
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
        
        # Ejecutar ambas llamadas a la API en paralelo
        results = await asyncio.gather(
            api_client.get_price_suggestion(form_data),
            api_client.get_average_price(form_data)
        )
        api_response, average_response = results

        if "error" in api_response:
            self.page.snack_bar = ft.SnackBar(ft.Text(api_response["error"]), bgcolor=ft.Colors.RED_700)
            self.page.snack_bar.open = True
            self.result_container.visible = False
        elif "error" in average_response:
            self.page.snack_bar = ft.SnackBar(ft.Text(average_response["error"]), bgcolor=ft.Colors.RED_700)
            self.page.snack_bar.open = True
            self.result_container.visible = False
        else:
            # Paso 1: Colocar el panel en la página para que se registre
            self.result_container.content = self.result_panel
            self.page.update()
            # Paso 2: Ahora que el panel existe en la página, actualizar sus datos
            self.result_panel.update_data(api_response, average_response)
            # Expandir el mapa y reducir el panel de resultados
            self.map_container.col = {"xs": 12, "md": 8, "lg": 8}
            self.map_container.height = 500 # Aumentar la altura del mapa
            self.right_panel_container.col = {"xs": 12, "md": 4, "lg": 4}
        
        self.page.update()

    def _handle_edit_request(self, e: ft.ControlEvent):
        # Restaurar el layout original
        self.map_container.col = {"xs": 12, "md": 6, "lg": 6}
        self.map_container.height = 350
        self.right_panel_container.col = {"xs": 12, "md": 6, "lg": 6}
        self.result_container.visible = False
        self.page.update()
