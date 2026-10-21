import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from components.navbar import create_navbar
from data.sample_data import get_monthly_sales_summary
# from pages.home import create_kpi_card

def create_kpi_card1(title, value, change, icon_class, is_positive=True, texto=""):
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
                        html.Small(texto, className="text-muted"),
                    ],
                    className="d-flex align-items-center",
                ),
            ]
        ),
        className="kpi-card h-100",
    )
# Register the page with Dash Pages
# The URL path will be '/avance-monto'
# The display name appears in the browser tab

datos = get_monthly_sales_summary()
EV_max=datos["EV_acumulado"].max()
print(f"El valor máximo de EV_acumulado es: {datos['EV_acumulado'].iloc[-1]}")
porc_avance_EV = (EV_max / 33000000) * 100

datos["Fecha"] = pd.to_datetime(datos["Fecha"])  # solo si la columna aún no es datetime
fecha_max = datos["Fecha"].max()
print(f"Fecha máxima en los datos: {fecha_max.strftime('%d-%B-%Y')}")


dash.register_page(__name__, path="/avance-monto", name="Avance por monto ejecutado")

# Placeholder data: you can replace with real data source later
# For now, we show a simple message and a chart area
layout = html.Div(
    [
        create_navbar("Avance por monto ejecutado"),
        
        dbc.Row(
            [
                dbc.Col(create_kpi_card1("Ingresos Totales", f"${EV_max:,.0f}", f"+{porc_avance_EV:.1f}%", "bi-currency-dollar", texto='% general'), md=6, lg=3, className="mb-4"),
                dbc.Col(create_kpi_card1("Fecha de corte", fecha_max.strftime('%d-%B-%Y'), "", "bi-calendar3", texto='fecha'), md=6, lg=3, className="mb-4"),
                # dbc.Col(create_kpi_card1("Tasa de Conversión", "3.24%", "-0.4%", "bi-graph-up-arrow", is_positive=False), md=6, lg=3, className="mb-4"),
                # dbc.Col(create_kpi_card1("Pedidos Activos", "312", "+15.3%", "bi-bag-check"), md=6, lg=3, className="mb-4"),
            ]
        ),
        dbc.Container(
            [
                html.H3("Avance por monto ejecutado"),
                html.P(
                    "Esta sección mostrará el avance acumulado basado en el monto ejecutado de las actividades."
                ),
                # Example placeholder graph
                dcc.Graph(id="avance-monto-graph"),
            ],
            fluid=True,
            className="mt-4",
        ),
    ]
)

# Simple callback that returns an empty figure for now
@callback(Output("avance-monto-graph", "figure"), Input("avance-monto-graph", "id"))
def update_figure(_): # type: ignore
    import plotly.graph_objects as go
    fig = go.Figure()
    fig = px.line(
                datos,
                x="Fecha",
                y=["EV_acumulado"],
                markers=False,
                title="Evolución de Ventas vs Objetivo",
                template="plotly_white",
                color_discrete_sequence=["#2563eb", "#94a3b8"], 
                height=650,)   
    fig.update_layout(title="Gráfico de avance (EV)", template="plotly_white")
    return fig

