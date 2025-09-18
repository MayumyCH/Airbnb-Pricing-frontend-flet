import flet as ft
import flet_map as map
from views.main_view import MainView

def main(page: ft.Page):
    # --- Configuración de la página ---
    page.title = "Estimador de Precios Airbnb"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#202328"
    page.window_width = 1280
    page.window_height = 800
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- Cargar la vista principal ---
    main_view = MainView(page)
    page.add(main_view)
    page.update()

if __name__ == "__main__":
    ft.app(
        target=main,
        assets_dir="assets",
        view=ft.AppView.WEB_BROWSER
    )