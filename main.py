from simulation import ejecutar_simulacion
from view import procesar_datos, generar_graficos, generar_tabla

def main():
    # Paso 1: Ejecutar simulación
    datos, SIM_TIME, WARM_UP = ejecutar_simulacion()
    
    # Paso 2: Procesar datos
    metricas = procesar_datos(datos, SIM_TIME, WARM_UP)
    metricas['SIM_TIME'] = SIM_TIME
    metricas['WARM_UP'] = WARM_UP
    
    # Paso 3: Generar visualizaciones
    generar_graficos(metricas, metricas['datos_filtrados'])
    df = generar_tabla(metricas)
    
    # Paso 4: Mostrar resultados en consola
    print("\nRESULTADOS DE LA SIMULACIÓN:")
    print(df.to_string(index=False))
    print("\nGráficos guardados como:")
    print("- evolucion_robots.png")
    print("- distribucion_cola.png")
    print("- tabla_resultados.png")
    print("- utilizacion_reparadores.png")

if __name__ == "__main__":
    main()