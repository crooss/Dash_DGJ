import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from components.navbar import create_navbar
from data.sample_data import get_monthly_sales_summary
from pages.home import create_kpi_card

# Register the page with Dash Pages
# The URL path will be '/avance-monto'
# The display name appears in the browser tab

datos = get_monthly_sales_summary()
# Último y penúltimo valor acumulado
ev_last = datos["EV_acumulado"].iloc[-1]
ev_prev = datos["EV_acumulado"].iloc[-2]
ev_diff = ev_last - ev_prev
ev_pct_change = ev_diff / ev_prev * 100 if ev_prev != 0 else 0
ev_pct_formatted = f"{ev_pct_change:+.1f}%"
print(f"Último EV_acumulado: {ev_last}, Cambio: {ev_pct_formatted}, Diferencia: {ev_diff}")
EV_max=datos["EV_acumulado"].max()
print(f"El valor máximo de EV_acumulado es: {datos['EV_acumulado'].iloc[-1]}")
porc_avance_EV = (EV_max / 33000000) * 100

dash.register_page(__name__, path="/avance-monto", name="Avance por monto ejecutado")

# Placeholder data: you can replace with real data source later
# For now, we show a simple message and a chart area
layout = html.Div(
    [
        create_navbar("Avance por monto ejecutado"),
        
        dbc.Row(
            [
                dbc.Col(create_kpi_card("Ingresos Totales", f"${EV_max:,.0f}", f"+{porc_avance_EV:.1f}%", "bi-currency-dollar"), md=6, lg=3, className="mb-4"),
                # dbc.Col(create_kpi_card("Nuevos Clientes", "1,429", "+8.1%", "bi-people"), md=6, lg=3, className="mb-4"),
                # dbc.Col(create_kpi_card("Tasa de Conversión", "3.24%", "-0.4%", "bi-graph-up-arrow", is_positive=False), md=6, lg=3, className="mb-4"),
                # dbc.Col(create_kpi_card("Pedidos Activos", "312", "+15.3%", "bi-bag-check"), md=6, lg=3, className="mb-4"),
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
def update_figure(_):
    import plotly.graph_objects as go
    fig = go.Figure()
    fig = px.line(
                datos,
                x="Fecha",
                y=["EV_acumulado"],
                markers=False,
                title="Evolución de Ventas vs Objetivo",
                template="plotly_white",
                color_discrete_sequence=["#2563eb", "#94a3b8"], )   
    fig.update_layout(title="Gráfico de avance (próximamente)", template="plotly_white")
    return fig

