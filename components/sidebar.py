import dash_bootstrap_components as dbc
from dash import html

def create_sidebar():
    """
    Crea el componente de barra lateral (Sidebar) con navegación,
    logo e información de usuario.
    """
    return html.Div(
        [
            # Header / Logo
            html.Div(
                [
                    html.I(className="bi bi-speedometer2 fs-3 text-primary me-2"),
                    html.H4("Dashboard", className="m-0 fw-bold text-white"),
                ],
                className="d-flex align-items-center mb-4 pb-3 border-bottom border-secondary border-opacity-25",
            ),
            
            # Subtítulo o sección
            html.Div(
                "MENÚ PRINCIPAL",
                className="text-uppercase text-secondary fw-semibold mb-2",
                style={"fontSize": "0.75rem", "letterSpacing": "0.05em"},
            ),

            # Enlaces de navegación con Dash Pages
            dbc.Nav(
                [
                    dbc.NavLink(
                        [
                            html.I(className="bi bi-currency-dollar"),
                            html.Span("Avance por monto ejecutado"),
                        ],
                        href="/",
                        active="exact",
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="bi bi-currency-dollar"),
                            html.Span("Avance por actividad"),
                        ],
                        href="/avance-actividad",
                        active="exact",
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="bi bi-graph-up"),
                            html.Span("Avance por concepto"),
                        ],
                        href="/avance-concepto",
                        active="exact",
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="bi bi-graph-up"),
                            html.Span("Avance por mes"),
                        ],
                        href="/avance-waterfall",
                        active="exact",
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="bi bi-percent"),
                            html.Span("KPI Actividades"),
                        ],
                        href="/cards",
                        active="exact",
                    ),
                    # dbc.NavLink(
                    #     [
                    #         html.I(className="bi bi-grid-1x2-fill"),
                    #         html.Span("Resumen General"),
                    #     ],
                    #     href="/home",
                    #     active="exact",
                    # ),
                    # dbc.NavLink(
                    #     [
                    #         html.I(className="bi bi-graph-up"),
                    #         html.Span("Analítica y Métricas"),
                    #     ],
                    #     href="/analytics",
                    #     active="exact",
                    # ),

                    # dbc.NavLink(
                    #     [
                    #         html.I(className="bi bi-gear-fill"),
                    #         html.Span("Configuración"),
                    #     ],
                    #     href="/settings",
                    #     active="exact",
                    # ),

                ],
                vertical=True,
                pills=True,
                className="mb-auto",
            ),

            # Perfil / Pie de barra lateral
            html.Div(
                [
                    html.Hr(className="border-secondary border-opacity-25"),
                    html.Div(
                        [
                            html.I(className="bi bi-person-circle fs-3 me-2 text-info"),
                            html.Div(
                                [
                                    html.Div("Administrador", className="fw-semibold small text-white"),
                                    html.Div("arturogodoy@corrosionyproteccion.com", className="text-secondary", style={"fontSize": "0.75rem"}),
                                ],
                                className="overflow-hidden text-truncate",
                            ),
                        ],
                        className="d-flex align-items-center",
                    ),
                ],
                className="mt-auto pt-3",
            ),
        ],
        className="sidebar d-flex flex-column",
    )
