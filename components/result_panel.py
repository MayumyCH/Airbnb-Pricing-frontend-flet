
import flet as ft
from typing import Dict, Any, Callable

def _create_analysis_bar(label: str, value: float, max_value: float, color: str) -> ft.Row:
    """Helper function to create a competitive analysis bar."""
    percentage = value / max_value if max_value > 0 else 0
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(label, size=12, width=80),
            ft.Stack(
                [
                    ft.Container(bgcolor="#3C4046", width=200, height=20, border_radius=10),
                    ft.Container(bgcolor=color, width=200 * percentage, height=20, border_radius=10),
                ]
            ),
            ft.Text(f"${value:.2f}", size=12, weight=ft.FontWeight.BOLD, width=70, text_align=ft.TextAlign.RIGHT),
        ]
    )

class ResultPanel(ft.Column):
    def __init__(self, on_edit: Callable):
        super().__init__(visible=False, spacing=20, scroll=ft.ScrollMode.ADAPTIVE)
        self.on_edit_callback = on_edit

        # --- Elementos de la UI que se actualizarán ---
        self.suggested_price_text = ft.Text(size=32, weight=ft.FontWeight.BOLD)
        self.percentage_tag = ft.Container(
            padding=ft.padding.symmetric(vertical=5, horizontal=10),
            border_radius=ft.border_radius.all(20),
        )
        self.justification_list = ft.Column(spacing=10)
        self.analysis_bars_column = ft.Column(spacing=8)

        self.edit_button = ft.Container(
            content=ft.Text("Modificar Consulta ✏️", size=14, weight=ft.FontWeight.BOLD),
            width=float("inf"),
            padding=ft.padding.all(15),
            alignment=ft.alignment.center,
            border_radius=10,
            bgcolor="#44484E",
            on_click=self._handle_edit_click,
        )

        self.controls = [
            ft.Text("Resultado del Análisis 📊", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([self.suggested_price_text, self.percentage_tag], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            # ft.ExpansionPanelList(
            #     expand_icon_color=ft.Colors.BLUE_GREY_300,
            #     elevation=0,
            #     divider_color=ft.Colors.BLUE_GREY_800,
            #     controls=[
            #         ft.ExpansionPanel(
            #             bgcolor="#2D3035",
            #             header=ft.ListTile(title=ft.Text("Justificación del Precio", weight=ft.FontWeight.BOLD)),
            #             content=ft.Container(content=self.justification_list, padding=ft.padding.only(left=15, right=15, bottom=15)),
            #         )
            #     ]
            # ),
            ft.Text("Análisis Competitivo (Vecindario)", size=16, weight=ft.FontWeight.BOLD),
            self.analysis_bars_column,
            ft.Divider(),
            self.edit_button,
        ]

    def _handle_edit_click(self, e):
        if self.on_edit_callback:
            self.on_edit_callback(e)

    def update_data(self, data: Dict[str, Any], average_data: Dict[str, Any]):
        # 1. Precio sugerido y porcentaje
        price = data.get("suggested_price", 0)
        filtered_avg_price = average_data.get("filtered_average_price", 0)

        if filtered_avg_price > 0:
            percentage = ((price - filtered_avg_price) / filtered_avg_price) * 100
        else:
            percentage = 0
        self.suggested_price_text.value = f"${price:.2f} / noche"
        
        is_positive = percentage >= 0
        self.percentage_tag.content = ft.Text(f"{'+' if is_positive else ''}{percentage:.1f}%", weight=ft.FontWeight.BOLD, color="#FFFFFF")
        self.percentage_tag.bgcolor = "#38761D" if is_positive else "#990000"
        self.percentage_tag.border = ft.border.all(1, "#66FF99" if is_positive else "#FF9999")

        # 2. Justificación
        # self.justification_list.controls.clear()
        # for item in data.get("justification", []):
        #     is_pos_impact = item["type"] == "positive"
        #     self.justification_list.controls.append(
        #         ft.Row([
        #             ft.Icon(name=ft.icons.CHECK_CIRCLE, color=ft.Colors.GREEN_ACCENT_400) if is_pos_impact else ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.AMBER_ACCENT_400),
        #             ft.Text(f"{item['description']} ({'+' if is_pos_impact else '-'}{abs(item['impact']):.1f}%)"),
        #         ])
        #     )

        # 3. Análisis competitivo
        your_price = data.get("suggested_price", 0)
        filtered_avg_price = average_data.get("filtered_average_price", 0)
        global_avg_price = average_data.get("global_average_price", 0)

        max_price = max(your_price, filtered_avg_price, global_avg_price, 1)

        self.analysis_bars_column.controls.clear()
        self.analysis_bars_column.controls.append(
            _create_analysis_bar("Tu Precio", your_price, max_price, "#4A90E2") # Azul
        )
        self.analysis_bars_column.controls.append(
            _create_analysis_bar("Prom. Filtrado", filtered_avg_price, max_price, "#7E57C2") # Morado
        )
        self.analysis_bars_column.controls.append(
            _create_analysis_bar("Prom. Global", global_avg_price, max_price, "#7F8C8D") # Gris
        )

        self.visible = True

