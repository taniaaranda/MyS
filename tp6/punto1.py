import numpy as np
import statistics as stats
import seaborn as sns
import matplotlib.pyplot as plt

def graficar_histograma(a):
    sns.set()
    sns.distplot(a,color="violet")
    plt.show()

#Calcula el intervalo de confianza
def calcular_IC(n, media, desvio, z):
    l = z * (desvio / np.sqrt(n))
    return media - l ,  media + l

def simular(inventario_minimo):
    CANT_AÑOS = 30
    CANT_DIAS = 250
    INVENTARIO_INICIAL = 80
    PRODUCCION = 130
    COSTO_MANTENIMIENTO = 70
    DESVIO = 25
    MEDIA = 150 
    Z = 2.58

    adicionales = []
    costos = []

    for i in range(CANT_AÑOS):
        costo = 0
        turnos_adicionales = 0
        inventario = INVENTARIO_INICIAL
        for j in range(CANT_DIAS):
            inventario += PRODUCCION
            demanda = round(np.random.normal(MEDIA, DESVIO))
            if inventario < demanda:
                demanda -= demanda -inventario
            inventario -= demanda
            if inventario <= inventario_minimo:
                turnos_adicionales += 1
                inventario += PRODUCCION
            costo += inventario * COSTO_MANTENIMIENTO
        adicionales.append(turnos_adicionales)
        costos.append(costo)
    
    promedio_turnos_adicionales = round(stats.mean(adicionales))
    promedio_costos = round(stats.mean(costos))

    limite_inferior, limite_superior = calcular_IC(len(costos), promedio_costos, stats.stdev(costos), Z)

    print("Para la cantidad minima de", inventario_minimo," unidades diarias en el inventario")
    print("El promedio de turnos adicionales es de ", promedio_turnos_adicionales,"turnos")
    print("El costo promedio de mantenimiento es de $", promedio_costos)
    print("El Intervalo de confianza tiene un limite inferior = ",limite_inferior," y un limite superior = ",limite_superior)

    graficar_histograma(costos)

if __name__ == "__main__":

    INVENTARIO_MINIMO_1 = 50
    INVENTARIO_MINIMO_2 = 60
    INVENTARIO_MINIMO_3 = 70

    simular(INVENTARIO_MINIMO_1)
    simular(INVENTARIO_MINIMO_2)
    simular(INVENTARIO_MINIMO_3)
    
