"""
Módulo para carga, generación o conexión de datos para el Dashboard.
"""
import pandas as pd
import numpy as np

def get_monthly_sales_summary():
    """Retorna un DataFrame con resumen de ventas mensuales."""
    
    ej=pd.DataFrame({
        "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct"],
        "Ventas": [12500, 15000, 14200, 18900, 21000, 20400, 23500, 25100, 24000, 28000],
        "Objetivo": [13000, 14000, 15000, 17000, 19000, 20000, 22000, 24000, 25000, 26000]
    })
    
    archivo=pd.read_excel("data/Reporte de Actividades Diarias CPI.xlsx", sheet_name="diario", engine="openpyxl")
    # Seleccionar columnas relevantes
    datos_EV = archivo[["Fecha", "EV"]]
    # Eliminar filas con valores vacíos en 'Fecha' o 'EV'
    datos_EV = datos_EV.dropna(subset=["Fecha", "EV"])
    # Ordenar por fecha ascendente
    datos_EV = datos_EV.sort_values("Fecha")
    datos_EV = datos_EV[datos_EV['EV'] > 0]
    # Calcular acumulado de EV
    datos_EV["EV_acumulado"] = datos_EV["EV"].cumsum()
    
    return datos_EV
