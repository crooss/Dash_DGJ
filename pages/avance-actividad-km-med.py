import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from components.navbar import create_navbar
from data.sample_data import get_monthly_sales_summary
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import plotly.graph_objects as go

dash.register_page(__name__, path="/avance-actividad-km-med", name="Avance por actividad x unidad")

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

datos = pd.read_excel("data/Reporte de Actividades Diarias CPI.xlsx", sheet_name="diario", engine="openpyxl")
datos=datos.dropna(subset=["Fecha", "EV"])
datos = datos.sort_values("Fecha")

datos = datos[['Codigo_actividad','Fecha','EV','nombre_actividad', 'Avance_km', 'Avance_Med']]
datos['Avance_km'].fillna(0, inplace=True)
datos['Avance_Med'].fillna(0, inplace=True)

datos['avance']=datos['Avance_km']+datos['Avance_Med']
# print(datos)
datos['EV_acumulado'] = datos['EV'].cumsum()
grupos=datos.groupby('nombre_actividad')



# Placeholder data: you can replace with real data source later
# For now, we show a simple message and a chart area
layout = html.Div(
    [
        create_navbar("Avance por actividad x unidad"),
        
        dbc.Row(
            [
                # dbc.Col(create_kpi_card1("Ingresos Totales", f"${EV_max:,.0f}", f"+{porc_avance_EV:.1f}%", "bi-currency-dollar", texto='% general'), md=6, lg=3, className="mb-4"),
                # dbc.Col(create_kpi_card1("Fecha de corte", fecha_max.strftime('%d-%B-%Y'), "", "bi-calendar3", texto='fecha'), md=6, lg=3, className="mb-4"),
                # dbc.Col(create_kpi_card1("Tasa de Conversión", "3.24%", "-0.4%", "bi-graph-up-arrow", is_positive=False), md=6, lg=3, className="mb-4"),
                # dbc.Col(create_kpi_card1("Pedidos Activos", "312", "+15.3%", "bi-bag-check"), md=6, lg=3, className="mb-4"),
            ]
        ),
        dbc.Container(
            [
                html.H3("Avance por actividad"),
                html.P(
                    "Esta sección mostrará el avance acumulado basado en el monto ejecutado de las actividades por unidades."
                ),
                dcc.Loading(
                    id="loading-avance-concepto",
                    type="circle",
                    children=html.Div([
                        dcc.Graph(id="avance-actividad-km-med-graph")
                    ])
                ),
                # dcc.Graph(id="avance-actividad-graph"),
            ],
            fluid=True,
            className="mt-4",
        ),
    ]
)

# Simple callback that returns an empty figure for now
@callback(Output("avance-actividad-km-med-graph", "figure"), Input("avance-actividad-km-med-graph", "id"))
def update_figure(grupos): # type: ignore
    fig = go.Figure()
    fig.update_layout(height=600, width=1200)  
        
    for grupo in grupos:
        gr=grupo[1]
        gr=gr.reset_index()
        gr['Avance_km'] = gr['Avance_km'].fillna(0)
        gr['Avance_Med'] = gr['Avance_Med'].fillna(0)
        gr['EV_acumulado'] = gr['EV'].cumsum() # type: ignore
        gr['km_acumulado'] = gr['Avance_km'].cumsum() # type: ignore
        gr['Med_acumulado'] = gr['Avance_Med'].cumsum() # type: ignore
        gr['Avance_km'] = gr['Avance_km'].fillna(0)
        gr['km_acumulado'] = gr['Avance_km'].cumsum()
        gr['Avance']=gr["km_acumulado"]+gr["Med_acumulado"]
        # print(gr['Avance'])
        fig.add_trace(go.Scatter(
            x=gr["Fecha"],
            y=gr["Avance"],
            customdata=gr['Avance'],
            mode="lines",
            name=str(gr["nombre_actividad"].iloc[0]),
            hovertemplate=(
            "Actividad=%{fullData.name}<br>"
            "Fecha=%{x|%d/%B/%Y}<br>"
            # "EV acumulado actual=%{y:$,.1f}<br>"
            "Avance=%{customdata:.1f}<br>"
            "<extra></extra>"
                            ),
        ))
    fig.update_layout(title="EV acumulado por actividad", template="plotly_white",colorway=px.colors.qualitative.Set1)
    # fig.update_yaxes(tickprefix='$', tickformat=',')
    fig.update_xaxes(dtick="M1",tickformat="%b\n%Y")
    fig.show()
    return fig

# update_figure(grupos)