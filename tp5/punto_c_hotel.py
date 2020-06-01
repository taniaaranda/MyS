import numpy as np
import statistics as stats
import seaborn as sns
import matplotlib.pyplot as plt

#Obtiene, suma y retorna las demoras de las tareas a, b, y c del acceso superior 
def calcular_acceso_superior():
    tarea_a = np.random.uniform(2,4)
    tarea_b = np.random.uniform(3,6)
    tarea_c = np.random.uniform(2,5)
    return tarea_a + tarea_b + tarea_c

#Obtiene, suma y retorna las demoras de las tareas d y e del acceso medio
def calcular_acceso_medio():
    tarea_d = np.random.uniform(3,6)
    tarea_e = np.random.uniform(2,5)
    return tarea_d + tarea_e

#Obteniene, suma y retorna las demoras de las tareas f y g del acceso inferior
def calcular_acceso_inferior():
    tarea_f = np.random.uniform(4,8)
    tarea_g = np.random.uniform(3,7)
    return tarea_f + tarea_g

#Obtiene y retorna las demoras de los accesos
def preparar_desayuno():
    acceso_superior = calcular_acceso_superior()
    acceso_medio = calcular_acceso_medio()
    acceso_inferior = calcular_acceso_inferior()
    return [acceso_superior,acceso_medio,acceso_inferior]    

#Calcula el intervalo de confianza
def calcular_IC(n, media, desvio, z):
    l = z * (desvio / np.sqrt(n))
    return media - l ,  media + l 

def graficar_histograma(a):
    sns.set()
    sns.distplot(a,color="violet")
    plt.show()

if __name__ == "__main__":
    
    CANT_EXPERIMENTOS = 30
    CANT_CORRIDAS = 100
    duraciones = []
    promedios_experimentos = []
    criticidad_as = 0
    criticidad_am = 0
    criticidad_ai = 0

    #Simulacion de los 30 experimentos de 100 corridas
    for i in range(CANT_EXPERIMENTOS):
        duracion_experimento = 0
        for j in range(CANT_CORRIDAS):
            accesos = preparar_desayuno()
            duracion_corrida = sum(accesos)
            duraciones.append(duracion_corrida)
            duracion_experimento += duracion_corrida

            #Obtengo el acceso mas critico y aumento su contador
            criticidad = max(accesos)        
            if criticidad == accesos[0]:
                criticidad_as += 1
            if criticidad == accesos[1]:
                criticidad_am += 1
            if criticidad == accesos[2]:
                criticidad_ai += 1

        promedios_experimentos.append(duracion_experimento/CANT_CORRIDAS)

    
    media = stats.mean(duraciones)
    z = 2.57
    limite_inferior, limite_superior = calcular_IC(len(duraciones), media, stats.stdev(duraciones), z)     
    
    #Calculo los porcentajes de la criticidad de cada acceso
    porcentaje_criticidad_as = criticidad_as * 100 / (CANT_EXPERIMENTOS * CANT_CORRIDAS) 
    porcentaje_criticidad_am = criticidad_am * 100 / (CANT_EXPERIMENTOS * CANT_CORRIDAS)
    porcentaje_criticidad_ai = criticidad_ai * 100 / (CANT_EXPERIMENTOS * CANT_CORRIDAS)
    
    print("El tiempo promedio de finalizacion del proyecto es de ",media," minutos")
    print("El Intervalo de confianza tiene un limite inferior = ",limite_inferior," y un limite superior = ",limite_superior)
    print("El porcentaje de criticidad del acceso superior es de ",porcentaje_criticidad_as,"%")
    print("El porcentaje de criticidad del acceso medio es de ",porcentaje_criticidad_am,"%")
    print("El porcentaje de criticidad del acceso inferior es de ",porcentaje_criticidad_ai, "%")

    graficar_histograma(duraciones)
    graficar_histograma(promedios_experimentos)