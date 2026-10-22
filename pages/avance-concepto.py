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

dash.register_page(__name__, path="/avance-concepto", name="Avance por concepto")

datos = pd.read_excel("data/Reporte de Actividades Diarias CPI.xlsx", sheet_name="diario", engine="openpyxl")
catalogo=pd.read_excel("data/Reporte de Actividades Diarias CPI.xlsx", sheet_name="Conceptos")

catalogo['cod_act']=catalogo['POSICIÓN'].astype(str)+' '+catalogo['nom'].astype(str)

conjunto=pd.merge(catalogo, datos, how='left', left_on='POSICIÓN', right_on='Codigo_actividad')

summary=conjunto.groupby('POSICIÓN', sort=False).agg({'EV':'sum', 'Avance_km':'sum', 'Avance_Med':'sum', 'CANTIDAD':'max', 'PRECIO UNITARIO':'max', 'cod_act':'first', 'ETAPA':'first'}).reset_index()
summary['ejecutado']=summary['Avance_km']+summary['Avance_Med']
summary[['POSICIÓN', 'cod_act','EV','ejecutado','CANTIDAD', 'PRECIO UNITARIO']]


summary['%av']=round(summary['ejecutado']/summary['CANTIDAD'], 4)

summary_plot = summary.copy()
# print(summary_plot)
summary_plot["ETAPA"] = summary_plot["ETAPA"].astype(str)
summary_plot["cod_act"] = summary_plot["cod_act"].astype(str)


etapas = sorted(summary_plot["ETAPA"].unique(), key=lambda e: e.split()[1] if len(e.split()) > 1 else e, reverse=True)

# datos=datos.dropna(subset=["Fecha", "EV"])
# datos = datos.sort_values("Fecha")

# datos = datos[['Codigo_actividad','Fecha','EV','nombre_actividad', 'Avance_km', 'Avance_Med']]
# datos['EV_acumulado'] = datos['EV'].cumsum()
# grupos=datos.groupby('nombre_actividad')



# Placeholder data: you can replace with real data source later
# For now, we show a simple message and a chart area
layout = html.Div(
    [
        create_navbar("Avance por concepto"),
        
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
                html.H3("Avance por concepto"),
                html.P(
                    f"Esta sección mostrará el avance acumulado basado en el % de avance de los conceptos."
                ),
                # Example placeholder graph
                dcc.Graph(id="avance-concepto-graph"),
            ],
            fluid=True,
            className="mt-4",
        ),
    ]
)

# Simple callback that returns an empty figure for now
@callback(Output("avance-concepto-graph", "figure"), Input("avance-concepto-graph", "id"))
def update_figure(_): # type: ignore
    import plotly.graph_objects as go
    fig = go.Figure()
    for etapa in etapas:
        df_etapa = summary_plot[summary_plot["ETAPA"] == etapa].sort_values("cod_act", ascending=False)

        fig.add_trace(go.Bar(
            x=df_etapa["%av"],
            y=df_etapa["cod_act"],
            orientation="h",
            name=etapa,
            text=df_etapa["%av"].map(lambda v: "" if v==0 else f"{v:.2%}"),
            textposition="auto",
            customdata=df_etapa[["ETAPA", "%av"]].values,
            hovertemplate="<b>Actividad</b>=%{y}<br><b>Etapa</b>=%{customdata[0]}<br>% Avance=%{customdata[1]:.2%}<extra></extra>",
            marker=dict(
                color=df_etapa["%av"],
                colorscale="Jet_r",
                cmin=0,
                cmax=1.0,
                colorbar=dict(title="% Avance", tickformat=".0%")
            )
        ))

    x_vline=1
    fig.add_vline(x=x_vline,
                line_dash="dash",
                line_color="green",
                line_width=2,
                annotation_text=f"{(x_vline*100)}%",
                annotation_position="top")
    
    buttons = [
        {
            "label": "Todas",
            "method": "update",
            "args": [{"visible": [True] * len(fig.data)}, {"title": "% de Avance por actividad"}] # type: ignore
        }
    ]

    for etapa in sorted(etapas):
        visible = [trace.name == etapa for trace in fig.data] # type: ignore
        buttons.append({
            "label": etapa,
            "method": "update",
            "args": [{"visible": visible}, {"title": f"% de EV por actividad - {etapa}"}]
        })

    fig.update_layout(
        updatemenus=[{
            "type": "buttons",
            "direction": "left",
            "x": 1.0,
            "y": 1.100,
            "showactive": True,
            "buttons": buttons,
            "pad":dict(r=5, t=5, b=5, l=5),
        }],
        template="plotly_white",
        xaxis_title="% Avance",
        yaxis_title="Actividad",
        height=800,
        width=1000,
        title="% de Avance por actividad")
    
    fig.update_yaxes(tickfont=dict(size=10))
    fig.update_layout(coloraxis_colorbar=dict(
                        tickformat=".0%"))
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_xaxes(range=[0, summary["%av"].max() * 1.15])
    fig.update_layout(showlegend=True)
    fig.update_xaxes(tickprefix='', tickformat='.0%')
    fig.update_layout(
        legend=dict(
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.1,
            yanchor="top",
            title_text="Etapa",
            font=dict(size=12),
        )
    )
    return fig

