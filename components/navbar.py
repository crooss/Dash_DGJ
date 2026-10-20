import dash_bootstrap_components as dbc
from dash import html

def create_navbar(title="Panel Principal"):
    """
    Crea una barra de navegación superior (Navbar) con título y botones de acción rápida.
    """
    return dbc.Navbar(
        dbc.Container(
            [
                html.Span(title, className="navbar-brand mb-0 h1 fw-bold text-dark"),
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.Button(
                                [html.I(className="bi bi-cloud-arrow-down me-1"), "Exportar"],
                                color="light",
                                size="sm",
                                className="me-2 border",
                            )
                        ),
                        dbc.NavItem(
                            dbc.Button(
                                [html.I(className="bi bi-arrow-clockwise me-1"), "Refrescar"],
                                color="primary",
                                size="sm",
                            )
                        ),
                    ],
                    className="ms-auto d-flex align-items-center",
                ),
            ],
            fluid=True,
        ),
        color="white",
        className="shadow-sm rounded-3 mb-4 py-2 px-3 border-0",
    )
