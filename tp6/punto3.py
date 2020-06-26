import numpy as np
import statistics as stats
import seaborn as sns
import matplotlib.pyplot as plt

class Evento:
    def __init__(self, tipo, dia, reloj_inicio, duracion, cantidad):
        self.tipo = tipo
        self.dia = dia
        self.reloj_inicio = reloj_inicio
        self.duracion = duracion
        self.cantidad = cantidad

def graficar_histograma(a):
    sns.set()
    sns.distplot(a,color="violet")
    plt.show()

def agregar_evento(fel, evento):
    if evento.reloj_inicio in fel:
        fel[evento.reloj_inicio].append(evento)
    else:
        fel[evento.reloj_inicio] = [evento]

def es_mes(dia):
    meses = {1: 31, 2: 59, 3: 90, 4: 120, 5: 151, 6: 181, 7: 212, 8: 243, 9: 273, 10: 304, 11: 334, 12: 365}
    for k in meses:
        if dia == meses[k]:
            return True
    return False

#Calcula el intervalo de confianza
def calcular_IC(n, media, desvio, z):
    l = z * (desvio / np.sqrt(n))
    return media - l ,  media + l

def simular(fel, dia, demanda, stock, reorden, costo_total_mes, costos_mensuales, ganancia_total):
    COSTO_UNITARIO = 450
    COSTO_FALTANTE = 20
    COSTO_ORDENAR = 93
    COSTO_ALMACENAMIENTO = 35
    CANTIDAD_ORDENAR = 100
    DIAS_ESPERA = 3
    

    #Hoy llegaron unidades 
    if fel.get(dia) != None:
        eventos_hoy = fel.get(dia)
        for evento_hoy in eventos_hoy:
            if evento_hoy.tipo == "LLEGO_ORDEN":
                stock += evento_hoy.cantidad
                eventos_hoy.remove(evento_hoy)
        fel.pop(dia)

    #Alcanza stock     
    if stock >= demanda:
        stock -= demanda
        ganancia_total += demanda * COSTO_UNITARIO 

    #No alcanza stock    
    elif stock < demanda:
        faltante = demanda - stock
        stock -= demanda - faltante
        costo_total_mes += faltante * COSTO_FALTANTE
        
    #Reordenar stock
    if stock <= reorden:
        costo_total_mes += CANTIDAD_ORDENAR * COSTO_ORDENAR
        evento = Evento("LLEGO_ORDEN", dia, dia + DIAS_ESPERA, DIAS_ESPERA, CANTIDAD_ORDENAR)
        agregar_evento(fel, evento)
            
    #Costo de mantenimiento por dia
    costo_total_mes += stock * COSTO_ALMACENAMIENTO
    #Si es fin de mes
    if es_mes(dia+1):
        costos_mensuales.append(costo_total_mes)
        costo_total_mes = 0

    return stock, costo_total_mes, ganancia_total

        

if __name__ == "__main__":
    DIAS = 365
    STOCK_INICIAL = 150
    REORDEN_1 = 30
    REORDEN_2 = 15
    REORDEN_3 = 40

    fel_1 = {}
    fel_2 = {}
    fel_3 = {}

    stock_1 = STOCK_INICIAL
    stock_2 = STOCK_INICIAL
    stock_3 = STOCK_INICIAL
    
    costo_total_1 = 0
    costo_total_2 = 0
    costo_total_3 = 0

    ganacias_1 = 0
    ganacias_2 = 0
    ganacias_3 = 0
    
    costos_mensuales_1 = []
    costos_mensuales_2 = []
    costos_mensuales_3 = []
    
    for dia in range(DIAS):
        demanda = np.random.poisson(37)

        stock_1, costo_total_1, ganancia_1 = simular(fel_1, dia, demanda, stock_1, REORDEN_1, costo_total_1, costos_mensuales_1, ganacias_1)
        stock_2, costo_total_2, ganancia_2 = simular(fel_2, dia, demanda, stock_2, REORDEN_2, costo_total_2, costos_mensuales_2, ganacias_2)
        stock_3, costo_total_3, ganancia_3 = simular(fel_3, dia, demanda, stock_3, REORDEN_3, costo_total_3, costos_mensuales_3, ganacias_3)

    #Calculo el costo anual para cada estrategia
    costo_total_1= sum(costos_mensuales_1)
    costo_total_2= sum(costos_mensuales_2)
    costo_total_3= sum(costos_mensuales_3)

    #IC para cada estrategia por mes
    promedio_costos_1 = stats.mean(costos_mensuales_1)
    promedio_costos_2 = stats.mean(costos_mensuales_2)
    promedio_costos_3 = stats.mean(costos_mensuales_3)

    Z = 1.96

    limite_inferior_1, limite_superior_1 = calcular_IC(len(costos_mensuales_1), promedio_costos_1, stats.stdev(costos_mensuales_1), Z)
    limite_inferior_2, limite_superior_2 = calcular_IC(len(costos_mensuales_2), promedio_costos_2, stats.stdev(costos_mensuales_2), Z)
    limite_inferior_3, limite_superior_3 = calcular_IC(len(costos_mensuales_3), promedio_costos_3, stats.stdev(costos_mensuales_3), Z)



    print("El costo total anual para la estrategia 1 es ", costo_total_1)
    print("La ganancia anual para la estrategia 1 es ", ganancia_1)
    print("El Intervalo de confianza tiene un limite inferior = ",limite_inferior_1," y un limite superior = ",limite_superior_1)

    graficar_histograma(costos_mensuales_1)    

    print("El costo total anual para la estrategia 2 es ", costo_total_2)
    print("La ganancia anual para la estrategia 2 es ", ganancia_2)
    print("El Intervalo de confianza tiene un limite inferior = ",limite_inferior_2," y un limite superior = ",limite_superior_2)

    graficar_histograma(costos_mensuales_2)    

    print("El costo total anual para la estrategia 3 es ", costo_total_3)
    print("La ganancia anual para la estrategia 3 es ", ganancia_3)
    print("El Intervalo de confianza tiene un limite inferior = ",limite_inferior_3," y un limite superior = ",limite_superior_3)

    graficar_histograma(costos_mensuales_3)    
