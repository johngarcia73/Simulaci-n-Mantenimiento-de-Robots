import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def procesar_datos(datos, SIM_TIME, WARM_UP):
    # Obtener índices válidos donde ambos tiempos_llegada y tiempos_salida existen
    indices_validos = []
    for i, t_llegada in enumerate(datos['tiempos_llegada']):
        if t_llegada >= WARM_UP and i < len(datos['tiempos_salida']):
            indices_validos.append(i)
    
    # Filtrar datos usando índices válidos
    datos_filtrados = {
        'tiempos_llegada': np.array(datos['tiempos_llegada'])[indices_validos],
        'tiempos_salida': np.array(datos['tiempos_salida'])[indices_validos],
        'tiempos_espera_cola': np.array(datos['tiempos_espera_cola'])[indices_validos],
        'tiempos_servicio': np.array(datos['tiempos_servicio'])[indices_validos],
        'estado_robots': datos['estado_robots'][int(WARM_UP*10):],
        'reparadores_ocupados': datos['reparadores_ocupados'][int(WARM_UP*10):],
        'uso_reparador': datos['uso_reparador']
    }
    
    
    
    # Calcular métricas
    L = np.mean(datos_filtrados['estado_robots'])
    W = np.mean(datos_filtrados['tiempos_salida'] - datos_filtrados['tiempos_llegada'])
    Wq = np.mean(datos_filtrados['tiempos_espera_cola'])
    P_idle = (datos_filtrados['reparadores_ocupados'].count(0) + 
             datos_filtrados['reparadores_ocupados'].count(1)) / len(datos_filtrados['reparadores_ocupados']) * 100
    utilizacion = [u/(SIM_TIME - WARM_UP)*100 for u in datos_filtrados['uso_reparador']]
    
    return {
        'L': L,
        'W': W,
        'Wq': Wq,
        'P_idle': P_idle,
        'utilizacion': utilizacion,
        'datos_filtrados': datos_filtrados
    }

def generar_graficos(metricas, datos_filtrados):
    plt.style.use('ggplot')
    plt.rcParams.update({'font.size': 12})
    
    # Gráfico 1: Evolución de robots operativos
    plt.figure(figsize=(10, 5))
    plt.plot(np.linspace(metricas['WARM_UP'], metricas['SIM_TIME'], 
             len(datos_filtrados['estado_robots'])), 
             datos_filtrados['estado_robots'], alpha=0.7)
    plt.title("Evolución del número de robots operativos")
    plt.xlabel("Tiempo (horas)")
    plt.ylabel("Robots operativos")
    plt.ylim(3, 10)
    plt.savefig("evolucion_robots.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Gráfico 2: Distribución del tiempo en cola
    plt.figure(figsize=(10, 5))
    plt.hist(datos_filtrados['tiempos_espera_cola'], bins=50, 
            density=True, alpha=0.7, color='#2ecc71')
    plt.title("Distribución del tiempo de espera en cola")
    plt.xlabel("Tiempo en cola (horas)")
    plt.ylabel("Densidad de probabilidad")
    plt.axvline(np.median(datos_filtrados['tiempos_espera_cola']), 
               color='#e74c3c', linestyle='dashed', linewidth=2, 
               label=f'Mediana: {np.median(datos_filtrados["tiempos_espera_cola"]):.2f} h')
    plt.legend()
    plt.savefig("distribucion_cola.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Gráfico 3: Utilización de reparadores
    plt.figure(figsize=(8, 5))
    plt.bar(['Reparador 1', 'Reparador 2'], metricas['utilizacion'], 
           color=['#3498db', '#e74c3c'])
    plt.title("Utilización de los reparadores")
    plt.ylabel("Porcentaje de uso (%)")
    plt.ylim(0, 100)
    plt.savefig("utilizacion_reparadores.png", dpi=300, bbox_inches='tight')
    plt.close()

def generar_tabla(metricas):
    df = pd.DataFrame({
        'Métrica': ['Robots operativos (L)', 'Tiempo total en sistema (W)', 
                   'Tiempo en cola (Wq)', '% Inactividad reparadores',
                   'Utilización Rep. 1', 'Utilización Rep. 2'],
        'Valor': [f"{metricas['L']:.2f}", f"{metricas['W']:.2f} h", 
                 f"{metricas['Wq']:.2f} h", f"{metricas['P_idle']:.2f}%",
                 f"{metricas['utilizacion'][0]:.2f}%", 
                 f"{metricas['utilizacion'][1]:.2f}%"]
    })
    
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.axis('off')
    table = ax.table(cellText=df.values, 
                   colLabels=df.columns, 
                   loc='center', 
                   cellLoc='center',
                   colColours=['#3498db']*2)
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    table.scale(1.2, 1.5)
    plt.savefig("tabla_resultados.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    return df