import numpy as np
import statistics as stats
import seaborn as sns
import matplotlib.pyplot as plt

class Evento:
    def __init__(self, tipo, dia, reloj_inicio, duracion, demanda, faltante):
        self.tipo = tipo
        self.dia = dia
        self.reloj_inicio = reloj_inicio
        self.duracion = duracion
        self.demanda = demanda
        self.faltante = faltante

def graficar_histograma(a):
    sns.set()
    sns.distplot(a,color="violet")
    plt.show()

#Calcula el intervalo de confianza
def calcular_IC(n, media, desvio, z):
    l = z * (desvio / np.sqrt(n))
    return media - l ,  media + l

#Retorna la cantidad de unidades de demanda segun la probabilidad
def get_demanda():
    unidades = {0.2: 25, 0.24: 30, 0.3: 40, 0.42: 50, 0.62: 100, 0.65: 150, 0.8: 200, 0.9: 250, 1.0: 300}
    probabilidad = np.random.uniform(0,1)
    for k in sorted(unidades):
        if probabilidad <= k:
            return unidades.get(k)

#Retorna la cantidad de dias de papeleo para la entrega segun la probabilidad
def get_tiempo_papeleo():
    dias = {0.2: 1, 0.5: 2, 0.75: 3, 1.0: 4}
    probabilidad = np.random.uniform(0,1)
    for k in sorted(dias):
        if probabilidad <= k:
            return dias.get(k)

#Retorna la cantidad de días de espera por lote
def get_tiempo_espera_faltante():
    dias = {0.4: 1, 0.6: 2, 0.75: 3, 0.9: 4, 1.0: 5}
    probabilidad = np.random.uniform(0,1)
    for k in sorted(dias):
        if probabilidad <= k:
            return dias.get(k)

def es_mes(dia):
    meses = {1: 31, 2: 59, 3: 90, 4: 120, 5: 151, 6: 181, 7: 212, 8: 243, 9: 273, 10: 304, 11: 334, 12: 365}
    for k in meses:
        if dia == meses[k]:
            return True
    return False

def agregar_evento(fel, evento):
    if evento.reloj_inicio in fel:
        fel[evento.reloj_inicio].append(evento)
    else:
        fel[evento.reloj_inicio] = [evento] 

if __name__ == "__main__":

    DIAS = 365
    INVENTARIO_INICIAL = 1500
    REORDEN = 15
    CANTIDAD_ORDENAR = 100
    COSTO_UNIDAD = 950  #por unidad
    COSTO_FALTANTE = 625 #por unidad
    COSTO_ORDENAR = 3800 #por orden
    COSTO_MANTENIMIENTO = 450 #por unidad por dia

    fel = {}
    inventario = INVENTARIO_INICIAL
    reservado = 0
    costo_total = 0
    costo_total_mes = 0
    ganancia = 0

    costos_mensuales = []
    
    for dia in range(DIAS):
        demanda = get_demanda()

        #Alcanza inventario espera papeleo    
        if inventario >= demanda:
            inventario -= demanda
            reservado += demanda
            demora_papeleo = get_tiempo_papeleo()
            evento = Evento("FIN_PAPELEO", dia, dia + demora_papeleo, demora_papeleo, demanda, 0)
            agregar_evento(fel, evento)

        #No alcanza inventario hay que esperar lote    
        elif inventario < demanda:
            espera_faltante = get_tiempo_espera_faltante()
            faltante = demanda - inventario
            inventario -= demanda - faltante
            reservado +=  demanda - faltante
            evento = Evento("FIN_ESPERA_FALTANTE", dia, dia + espera_faltante, espera_faltante, demanda, faltante)
            agregar_evento(fel, evento)
            costo_total_mes += faltante * COSTO_FALTANTE
        
        #Poco inventario se ordenan 100 
        if inventario <= REORDEN:
            inventario += CANTIDAD_ORDENAR
            costo_total_mes += COSTO_ORDENAR

        #Hoy hay entregas o llegadas de lotes de faltantes
        if fel.get(dia) != None:
            eventos_hoy = fel.get(dia)
            for evento in eventos_hoy:
                #Entregar unidades
                if evento.tipo == "FIN_PAPELEO":
                    reservado -= evento.demanda
                    ganancia += evento.demanda * COSTO_UNIDAD
                    eventos_hoy.remove(evento)
                #Llego lote unidades faltantes, preparo papeleo
                if evento.tipo == "FIN_ESPERA_FALTANTE":
                    inventario += evento.faltante
                    inventario -= evento.faltante
                    reservado += evento.faltante
                    demora_papeleo = get_tiempo_papeleo()
                    evento_papeleo = Evento("FIN_PAPELEO", dia, dia + demora_papeleo, demora_papeleo, evento.demanda, 0)
                    agregar_evento(fel, evento_papeleo)
                    eventos_hoy.remove(evento)
            fel.pop(dia)

        #Costo de mantenimiento por dia
        costo_total_mes += (inventario + reservado) * COSTO_MANTENIMIENTO
        if es_mes(dia+1):
            costos_mensuales.append(costo_total_mes)
            costo_total_mes = 0
        

    costo_total = sum(costos_mensuales)
    promedio_costos = stats.mean(costos_mensuales)
    Z = 1.96
    limite_inferior, limite_superior = calcular_IC(len(costos_mensuales), promedio_costos, stats.stdev(costos_mensuales), Z)
    
    print("El costo total anual es ", costo_total)
    print("La ganancia anual es ", ganancia)
    print("El Intervalo de confianza tiene un limite inferior = ",limite_inferior," y un limite superior = ",limite_superior)

    graficar_histograma(costos_mensuales)    