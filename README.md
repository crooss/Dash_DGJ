# 📊 Dash Plotly Dashboard con Sidebar

Una plantilla profesional, moderna y escalable para aplicaciones Dashboard desarrolladas con **Plotly Dash** y **Dash Bootstrap Components**, estructurada mediante el sistema nativo de páginas múltiples (*Dash Pages*).

---

## 📁 Estructura del Proyecto

```text
Dash App/
│
├── assets/
│   └── style.css            # Hoja de estilos personalizados (Sidebar fija, tarjetas KPI, etc.)
│
├── components/              # Componentes visuales modulares y reutilizables
│   ├── __init__.py
│   ├── sidebar.py           # Barra lateral de navegación fija (Sidebar)
│   └── navbar.py            # Barra superior (Navbar) opcional para acciones rápidas
│
├── pages/                   # Vistas/Páginas del Dashboard (Dash Pages automático)
│   ├── __init__.py
│   ├── home.py              # Vista principal: Métricas KPI y gráficos de resumen
│   ├── analytics.py         # Vista analítica: Gráficos interactivos y filtros dinámicos
│   └── settings.py          # Vista de configuración del sistema
│
├── data/                    # Módulos para carga, conexión a bases de datos o datasets
│   ├── __init__.py
│   └── sample_data.py       # Generador/cargador de datos de ejemplo
│
├── utils/                   # Funciones auxiliares, cálculos y transformaciones
│   └── __init__.py
│
├── app.py                   # Archivo principal de ejecución y orquestación del layout
├── requirements.txt         # Lista de dependencias del proyecto
├── .gitignore               # Configuración de exclusiones de control de versiones
└── README.md                # Documentación del proyecto
```

---

## 🚀 Puesta en Marcha

### 1. Crear y activar entorno virtual (Recomendado)

En PowerShell:
```powershell
# Crear entorno virtual
python -m venv venv

# Activar en Windows PowerShell
.\venv\Scripts\Activate.ps1
```

*(Si encuentras una restricción de políticas de scripts en PowerShell, ejecuta primero: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```powershell
python app.py
```

Abre tu navegador en: [http://127.0.0.1:8050](http://127.0.0.1:8050)

---

## 💡 Cómo agregar nuevas páginas

Gracias a **Dash Pages**, agregar una nueva vista es muy fácil:

1. Crea un nuevo archivo dentro de `pages/`, por ejemplo `pages/reports.py`.
2. Registra la página al inicio con:
   ```python
   import dash
   from dash import html

   dash.register_page(__name__, path="/reports", name="Reportes")

   layout = html.Div([
       html.H2("Página de Reportes"),
       # tus componentes y gráficos aquí
   ])
   ```
3. Agrega el enlace en [`components/sidebar.py`](components/sidebar.py) dentro del componente `dbc.Nav`:
   ```python
   dbc.NavLink(
       [html.I(className="bi bi-file-earmark-text"), html.Span("Reportes")],
       href="/reports",
       active="exact",
   )
   ```
