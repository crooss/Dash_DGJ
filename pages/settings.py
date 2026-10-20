import dash
from dash import html
import dash_bootstrap_components as dbc
from components.navbar import create_navbar

# Registrar página
dash.register_page(__name__, path="/settings", name="Configuración")

layout = html.Div(
    [
        create_navbar("Configuración de la Aplicación"),

        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Preferencias del Dashboard", className="fw-bold mb-4 text-dark"),
                    dbc.Form(
                        [
                            dbc.Row(
                                [
                                    dbc.Label("Nombre de la Empresa / App", width=4, className="fw-semibold text-secondary"),
                                    dbc.Col(
                                        dbc.Input(type="text", value="Mi Empresa Global", placeholder="Nombre"),
                                        width=8,
                                    ),
                                ],
                                className="mb-3",
                            ),
                            dbc.Row(
                                [
                                    dbc.Label("Zona Horaria", width=4, className="fw-semibold text-secondary"),
                                    dbc.Col(
                                        dbc.Select(
                                            options=[
                                                {"label": "América/Bogotá (UTC-5)", "value": "UTC-5"},
                                                {"label": "América/Ciudad_de_México (UTC-6)", "value": "UTC-6"},
                                                {"label": "América/Madrid (UTC+1)", "value": "UTC+1"},
                                                {"label": "América/Buenos_Aires (UTC-3)", "value": "UTC-3"},
                                            ],
                                            value="UTC-6",
                                        ),
                                        width=8,
                                    ),
                                ],
                                className="mb-3",
                            ),
                            dbc.Row(
                                [
                                    dbc.Label("Alertas Automáticas", width=4, className="fw-semibold text-secondary"),
                                    dbc.Col(
                                        dbc.Switch(id="alerts-toggle", value=True, label="Notificar por correo ante anomalías en métricas"),
                                        width=8,
                                    ),
                                ],
                                className="mb-4",
                            ),
                            html.Hr(className="my-4"),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Button("Descartar", color="light", className="me-2 border"),
                                            dbc.Button("Guardar Configuración", color="primary", className="px-4"),
                                        ],
                                        className="text-end",
                                    )
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            className="shadow-sm border-0 rounded-3 p-3",
        ),
    ]
)
