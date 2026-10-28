import dash
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
from components.navbar import create_navbar

dash.register_page(__name__, path="/cards", name="Avances")


datos = pd.read_excel( "data/Reporte de Actividades Diarias CPI.xlsx", sheet_name="diario", engine="openpyxl")
catalogo = pd.read_excel("data/Reporte de Actividades Diarias CPI.xlsx",sheet_name="Conceptos")
catalogo["cod_act"] = (catalogo["POSICIÓN"].astype(str) + " " + catalogo["nom"].fillna("").astype(str)).str.strip()

avance = pd.merge(
    catalogo,
    datos,
    how="left",
    left_on="POSICIÓN",
    right_on="Codigo_actividad")
summary = (avance.groupby("POSICIÓN", sort=False).agg(
        {
            "EV": "sum",
            "Avance_km": "sum",
            "Avance_Med": "sum",
            "CANTIDAD": "max",
            "cod_act": "first",
            "ETAPA": "first",
        }
        ).reset_index()
)
summary["ejecutado"] = summary["Avance_km"] + summary["Avance_Med"]
summary["ETAPA"] = summary["ETAPA"].fillna("Sin etapa").astype(str)


def tarjeta(actividad):
    cantidad = actividad["CANTIDAD"]
    ejecutado = actividad["ejecutado"]
    porcentaje = ejecutado / cantidad * 100 if pd.notna(cantidad) and cantidad > 0 else None
    avance_texto = f"{porcentaje:.1f}%" if porcentaje is not None else "Sin cantidad"
    ejecutado_texto = (
        f"Ejecutado: {ejecutado:,.2f} / {cantidad:,.2f}"
        if pd.notna(cantidad)
        else f"Ejecutado: {ejecutado:,.2f}"
    )

    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div([
                                html.Span(actividad["cod_act"], className="fw-bold text-dark mb-3"),
                                html.Div(html.I(className=f"bi bi-percent text-primary fs-5"),
                                        className="bg-light p-2 rounded-circle d-flex align-items-center justify-content-center",
                                        style={"width": "40px", "height": "40px", "width": "fit-content"})
                             ],
                            className="d-flex justify-content-between align-items-center mb-2",
                            ),
                    html.Div(
                        [
                            html.Span("Avance", className="text-muted"),
                            html.Span(avance_texto, className="fw-semibold"),
                        ],
                        className="d-flex justify-content-between mb-2",
                    ),
                    dbc.Progress(
                        value=min(max(porcentaje or 0, 0), 100),
                        color=(
                            "success"
                            if porcentaje is not None and porcentaje >= 100
                            else "primary"
                        ),
                        className="mb-3",
                        style={"height": "15px"},
                    ),
                    html.Div(
                        [
                            html.Small(
                                ejecutado_texto,
                                className="text-muted d-block",
                            ),
                            html.Small(
                                f"EV: ${actividad['EV']:,.2f}",
                                className="text-muted d-block mt-1",
                            ),
                        ]
                    ),
                ]
            ),
            className="kpi-card h-80",
        ),
        xs=12,
        md=6,
        lg=5,
        xl=3,
        className="mb-4",
    )


secciones_etapa = []
for etapa, actividades in summary.groupby("ETAPA", sort=False):
    secciones_etapa.append(
        html.Section(
            [
                html.H3(etapa, className="mb-3"), # type: ignore
                dbc.Row([tarjeta(actividad) for _, actividad in actividades.iterrows()]),
            ],
            className="mb-4",
        )
    )

layout = html.Div(
    [
        create_navbar("Avance por actividad"),
        dbc.Container(
            [
                html.H2("Avance por etapa y actividad", className="mb-4"),
                *secciones_etapa,
            ],
            fluid=True,
            className="mt-4",
        ),
    ]
)
