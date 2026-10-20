import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from components.navbar import create_navbar

# Registrar página
dash.register_page(__name__, path="/analytics", name="Analítica y Métricas")

# Datos de muestra por región
df_regions = pd.DataFrame({
    "Región": ["Norte", "Sur", "Este", "Oeste"] * 4,
    "Trimestre": ["Q1", "Q1", "Q1", "Q1", "Q2", "Q2", "Q2", "Q2", "Q3", "Q3", "Q3", "Q3", "Q4", "Q4", "Q4", "Q4"],
    "Rendimiento": [85, 70, 92, 60, 88, 75, 95, 68, 90, 82, 99, 74, 94, 85, 105, 80],
    "Satisfaccion": [4.2, 3.9, 4.7, 4.0, 4.3, 4.1, 4.8, 4.2, 4.5, 4.3, 4.9, 4.1, 4.6, 4.4, 5.0, 4.3],
})

layout = html.Div(
    [
        create_navbar("Analítica Avanzada y Métricas"),

        # Tarjeta de Filtros Interactivos
        dbc.Card(
            dbc.CardBody(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Métrica a analizar:", className="fw-semibold small text-muted mb-2"),
                                dcc.Dropdown(
                                    id="analytics-metric-select",
                                    options=[
                                        {"label": "Rendimiento Operativo", "value": "Rendimiento"},
                                        {"label": "Índice de Satisfacción (1-5)", "value": "Satisfaccion"},
                                    ],
                                    value="Rendimiento",
                                    clearable=False,
                                ),
                            ],
                            md=6,
                            className="mb-3 mb-md-0",
                        ),
                        dbc.Col(
                            [
                                html.Label("Visualización:", className="fw-semibold small text-muted mb-2"),
                                dbc.RadioItems(
                                    id="analytics-chart-type",
                                    options=[
                                        {"label": " Gráfico de Barras", "value": "bar"},
                                        {"label": " Gráfico de Líneas", "value": "line"},
                                    ],
                                    value="bar",
                                    inline=True,
                                    className="pt-2",
                                ),
                            ],
                            md=6,
                        ),
                    ]
                )
            ),
            className="shadow-sm border-0 rounded-3 mb-4",
        ),

        # Gráfico dinámico
        dbc.Card(
            dbc.CardBody([dcc.Graph(id="analytics-graph")]),
            className="shadow-sm border-0 rounded-3",
        ),
    ]
)

@callback(
    Output("analytics-graph", "figure"),
    Input("analytics-metric-select", "value"),
    Input("analytics-chart-type", "value"),
)
def update_analytics_chart(metric, chart_type):
    if chart_type == "bar":
        fig = px.bar(
            df_regions,
            x="Trimestre",
            y=metric,
            color="Región",
            barmode="group",
            title=f"Comparativa: {metric} por Región",
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Safe,
        )
    else:
        fig = px.line(
            df_regions,
            x="Trimestre",
            y=metric,
            color="Región",
            markers=True,
            title=f"Tendencia: {metric} a lo largo del año",
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Safe,
        )

    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20), hovermode="x unified")
    return fig
