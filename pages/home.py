import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from components.navbar import create_navbar

# Registrar esta vista como página de inicio
dash.register_page(__name__, path="/home", name="Resumen General")

# Datos de muestra
sales_data = pd.DataFrame({
    "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct"],
    "Ventas": [12500, 15000, 14200, 18900, 21000, 20400, 23500, 25100, 24000, 28000],
    "Objetivo": [13000, 14000, 15000, 17000, 19000, 20000, 22000, 24000, 25000, 26000]
})

category_data = pd.DataFrame({
    "Categoría": ["Electrónica", "Ropa", "Hogar", "Deportes", "Libros"],
    "Total": [45000, 32000, 28000, 19000, 11000]
})

# Gráfico de líneas (Tendencia)
fig_trend = px.line(
    sales_data,
    x="Mes",
    y=["Ventas", "Objetivo"],
    markers=True,
    title="Evolución de Ventas vs Objetivo",
    template="plotly_white",
    color_discrete_sequence=["#2563eb", "#94a3b8"],
)
fig_trend.update_layout(
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode="x unified",
)

# Gráfico de barras (Categorías)
fig_bar = px.bar(
    category_data,
    x="Categoría",
    y="Total",
    title="Ventas por Categoría",
    template="plotly_white",
    color="Categoría",
    color_discrete_sequence=px.colors.qualitative.Prism,
)
fig_bar.update_layout(
    margin=dict(l=20, r=20, t=50, b=20),
    showlegend=False,
)

def create_kpi_card(title, value, change, icon_class, is_positive=True):
    """Genera una tarjeta KPI moderna."""
    badge_color = "success" if is_positive else "danger"
    badge_icon = "bi-arrow-up-right" if is_positive else "bi-arrow-down-right"

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Span(title, className="text-muted small fw-medium"),
                        html.Div(
                            html.I(className=f"bi {icon_class} text-primary fs-5"),
                            className="bg-light p-2 rounded-circle d-flex align-items-center justify-content-center",
                            style={"width": "40px", "height": "40px"},
                        ),
                    ],
                    className="d-flex justify-content-between align-items-center mb-2",
                ),
                html.H3(value, className="fw-bold mb-2 text-dark"),
                html.Div(
                    [
                        dbc.Badge(
                            [html.I(className=f"bi {badge_icon} me-1"), change],
                            color=badge_color,
                            className="me-2 px-2 py-1",
                        ),
                        html.Small("vs el registro anterior", className="text-muted"),
                    ],
                    className="d-flex align-items-center",
                ),
            ]
        ),
        className="kpi-card h-100",
    )

layout = html.Div(
    [
        create_navbar("Resumen General de Operaciones"),
        
        # Fila de Tarjetas KPI
        dbc.Row(
            [
                dbc.Col(create_kpi_card("Ingresos Totales", "$182,600", "+12.4%", "bi-currency-dollar"), md=6, lg=3, className="mb-4"),
                dbc.Col(create_kpi_card("Nuevos Clientes", "1,429", "+8.1%", "bi-people"), md=6, lg=3, className="mb-4"),
                dbc.Col(create_kpi_card("Tasa de Conversión", "3.24%", "-0.4%", "bi-graph-up-arrow", is_positive=False), md=6, lg=3, className="mb-4"),
                dbc.Col(create_kpi_card("Pedidos Activos", "312", "+15.3%", "bi-bag-check"), md=6, lg=3, className="mb-4"),
            ]
        ),

        # Fila de Gráficos
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([dcc.Graph(figure=fig_trend, config={"displayModeBar": False})]),
                        className="shadow-sm border-0 rounded-3 mb-4",
                    ),
                    lg=8,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([dcc.Graph(figure=fig_bar, config={"displayModeBar": False})]),
                        className="shadow-sm border-0 rounded-3 mb-4",
                    ),
                    lg=4,
                ),
            ]
        ),
    ]
)
