import flet as ft
from components.map_view import MapView
from components.input_form import InputForm
from components.result_panel import ResultPanel
from services import api_client

class MainView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, padding=ft.padding.all(20))
        self.page = page
        self.page.on_resize = self.on_resize

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
        # Este Column se expandirá gracias a su padre, el right_panel_container
        self.right_panel_content = ft.Column([
            self.input_form,
            self.result_container
        ], spacing=20, scroll=ft.ScrollMode.AUTO)

        # --- Contenedores de layout (los que se moverán) ---
        self.map_container = ft.Container(self.map_view, expand=True, padding=ft.padding.all(10))
        self.right_panel_container = ft.Container(self.right_panel_content, expand=True, padding=ft.padding.all(20))
        self.divider = ft.VerticalDivider(width=1)

        # --- Layout Principal (será un Row o Column) ---
        # Lo inicializamos como un control vacío que se llenará en on_resize
        self.main_layout = ft.Container(expand=True)

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
        
        self._initialized = False
        # Llamada inicial para establecer el layout correcto al arrancar
        self.on_resize(None)
        self._initialized = True

    def on_resize(self, e):
        # Si la página aún no tiene ancho, no hacer nada
        if self.page.width is None:
            return

        is_desktop = self.page.width >= 800
        current_layout_is_row = isinstance(self.main_layout.content, ft.Row)

        # Solo reconstruir si el tipo de layout necesita cambiar
        if is_desktop and not current_layout_is_row:
            self.main_layout.content = ft.Row(
                controls=[
                    self.map_container,
                    self.divider,
                    self.right_panel_container
                ],
                vertical_alignment=ft.CrossAxisAlignment.START
            )
        elif not is_desktop and (current_layout_is_row or self.main_layout.content is None):
            self.main_layout.content = ft.Column(
                controls=[
                    self.map_container,
                    self.right_panel_container
                ]
            )
        
        if self._initialized:
            self.update()

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
            # Paso 1: Colocar el panel en la página para que se registre
            self.result_container.content = self.result_panel
            self.page.update()
            # Paso 2: Ahora que el panel existe en la página, actualizar sus datos
            self.result_panel.update_data(api_response)
        
        self.page.update()
