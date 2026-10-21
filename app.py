import dash
from dash import html
import dash_bootstrap_components as dbc
from components.sidebar import create_sidebar

# 1. Inicializar la aplicación Dash con soporte para páginas automáticas (Dash Pages)
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,       # Estilos base de Bootstrap
        dbc.icons.BOOTSTRAP,        # Colección de iconos Bootstrap Icons
    ],
    suppress_callback_exceptions=True,
    title="Panel de Control y Analítica",
)

server = app.server  # Exponer el servidor Flask subyacente (útil para despliegue en producción)

# 2. Definición del Layout General
# El Sidebar queda fijo a la izquierda y el contenedor 'dash.page_container'
# renderiza dinámicamente la página correspondiente según la ruta.
app.layout = html.Div(
    [
        create_sidebar(),
        html.Div(
            dash.page_container,
            className="content",
        ),
    ]
)

# 3. Punto de entrada
if __name__ == "__main__":
    print("Iniciando Dashboard en http://127.0.0.1:8050 ...")
    import os
    # Render provides PORT via environment variable; default to 8050 for local dev
    port = int(os.getenv('PORT', 8050))
    app.run(debug=True, host='localhost', port=port)
