import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from components.navbar import create_navbar
import plotly.graph_objects as go

dash.register_page(__name__, path="/avance-waterfall", name="Avance x mes")

layout = html.Div(
    [
        create_navbar("Avance por mes"),
        
        # dbc.Row(
        #     [
        #         dbc.Col(create_kpi_card1("Ingresos Totales", f"${EV_max:,.0f}", f"+{porc_avance_EV:.1f}%", "bi-currency-dollar", texto='% general'), md=6, lg=3, className="mb-4"),
        #         dbc.Col(create_kpi_card1("Fecha de corte", fecha_max.strftime('%d-%B-%Y'), "", "bi-calendar3", texto='fecha'), md=6, lg=3, className="mb-4"),
        #         # dbc.Col(create_kpi_card1("Tasa de Conversión", "3.24%", "-0.4%", "bi-graph-up-arrow", is_positive=False), md=6, lg=3, className="mb-4"),
        #         # dbc.Col(create_kpi_card1("Pedidos Activos", "312", "+15.3%", "bi-bag-check"), md=6, lg=3, className="mb-4"),
        #     ]
        # ),
        dbc.Container(
            [
                html.H3("Avance por mes"),
                html.P(
                    "Esta sección mostrará el avance acumulado basado en el monto ejecutado por mes."
                ),
                dcc.Loading(
                    id="loading-avance-waterfall",
                    type="circle",
                    children=html.Div([
                        dcc.Graph(id="avance-waterfall-graph")
                    ])
                ),
                # dcc.Graph(id="avance-monto-graph"),
            ],
            fluid=True,
            className="mt-4",
        ),
    ]
)

balance=pd.read_excel(r"data/Reporte de Actividades Diarias CPI.xlsx", sheet_name="balance")
balance=balance.sort_values('fecha')



@callback(Output("avance-waterfall-graph", "figure"), Input("avance-waterfall-graph", "id"))
def update_figure(_): # type: ignore
    
    fig = go.Figure(go.Waterfall(
        x=balance["mes_letter"],#.dt.strftime("%b %Y"),
        y=balance["EV"],
        measure=balance['measure'],
        name="EV por mes",
        text=[f"${v:,.0f}" for v in balance["EV"]],
        textposition="outside",
        connector={"line": {"color": "rgba(50,50,50,0.6)", "width": 1}},
        increasing={"marker": {"color": "#2ca02c"}},
        decreasing={"marker": {"color": "#d62728"}},
        totals={"marker": {"color": "#1f77b4"}},
        hovertemplate="<b>Mes</b>: %{x}<br><b>EV</b>: $%{y:,.0f}<extra></extra>",
        ))
    
    # fig=

    fig.update_layout(title="Waterfall de EV por mes",
                    template="plotly_white",
                    xaxis_title="Mes",
                    yaxis_title="EV",
                    showlegend=False,
                    height=600,
                    width=1000,
                    xaxis_tickangle=-90)
    
    y_min = balance["EV"].min()
    y_max = balance["EV"].max()
    padding = (y_max - y_min) * 0.2 if y_max != y_min else 1
    fig.update_yaxes(range=[0, y_max + padding])
    fig.update_yaxes(tickprefix='$', tickformat=',')
        
        
    return fig