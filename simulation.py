import simpy
import numpy as np

def ejecutar_simulacion():
    N_robots = 10
    lambda_fallo = 1/30
    mu_reparacion = 1/3
    SIM_TIME = 10000
    WARM_UP = 1000

    datos = {
        'tiempos_llegada': [],
        'tiempos_salida': [],
        'tiempos_espera_cola': [],
        'tiempos_servicio': [],
        'estado_robots': [],
        'reparadores_ocupados': [],
        'uso_reparador': [0.0, 0.0]  # Reparador 1 y 2
    }

    def proceso_robot(env, nombre, reparadores):
        while True:
            tiempo_fallo = np.random.exponential(1/lambda_fallo)
            yield env.timeout(tiempo_fallo)
            
            tiempo_llegada = env.now
            datos['tiempos_llegada'].append(tiempo_llegada)
            
            with reparadores.request() as req:
                
                # Registrar reparador asignado (0 o 1)
                if reparadores.count == 1:
                    reparador_asignado = 0  # Solo uno disponible, no hay opción
                else:
                    reparador_asignado = np.random.randint(0, 2)
                tiempo_inicio = env.now
                datos['tiempos_espera_cola'].append(tiempo_inicio - tiempo_llegada)
                
                tiempo_servicio = np.random.exponential(1/mu_reparacion)
                datos['tiempos_servicio'].append(tiempo_servicio)
                datos['uso_reparador'][reparador_asignado] += tiempo_servicio
                
                yield env.timeout(tiempo_servicio)
                datos['tiempos_salida'].append(env.now)

    def monitor_estados(env, reparadores):
        while True:
            datos['reparadores_ocupados'].append(reparadores.count)
            datos['estado_robots'].append(N_robots - reparadores.count)
            yield env.timeout(0.1)

    # Configurar entorno
    env = simpy.Environment()
    reparadores = simpy.Resource(env, capacity=2)  # Sería un recurso con capacidad 2
    
    for i in range(N_robots):
        env.process(proceso_robot(env, f'Robot_{i}', reparadores))
    
    env.process(monitor_estados(env, reparadores))
    env.run(until=SIM_TIME)
    
    return datos, SIM_TIME, WARM_UP