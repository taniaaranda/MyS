import numpy as np
import statistics as stats
import seaborn as sns
import matplotlib.pyplot as plt

class Evento:
    def __init__(self, tipo, camion, reloj_inicio, duracion):
        self.tipo = tipo
        self.camion = camion
        self.reloj_inicio = reloj_inicio
        self.duracion = duracion

class Surtidor:
    def __init__(self, nombre, empleado):
        self.nombre = nombre
        self.ocupado = False
        self.empleado = empleado
        self.camion_atendiendo = None
        self.ocupacion = 0
        self.porcentaje_ocupacion = 0 

class Camion:
    def __init__(self, id, llegada):
        self.id = id
        self.llegada = llegada
        self.espera = 0

class Empleado:
    def __init__(self, nombre, distribucion):
        self.nombre = nombre
        self.distribucion = distribucion
    

class EmpleadoNormal(Empleado):
    def __init__(self, nombre, distribucion, media, desvio):
        Empleado.__init__(self, nombre, distribucion)
        self.media = media
        self.desvio = desvio

    def calcular_tiempo_atencion(self):
        return np.random.normal(self.media,self.desvio)

class EmpleadoExponencial(Empleado):    
    def __init__(self, nombre, distribucion, promedio):
        Empleado.__init__(self, nombre, distribucion)
        self.beta = promedio
    
    def calcular_tiempo_atencion(self):
        return np.random.exponential(self.beta)

def graficar_histograma(a):
    sns.set()
    sns.distplot(a,color="violet")
    plt.show()

#Calcula el intervalo de confianza
def calcular_IC(n, media, desvio, z):
    l = z * (desvio / np.sqrt(n))
    return media - l ,  media + l 

#Busco el surtidor que esta atendiendo el camion y lo marco como desocupado
def finalizar_atencion(fel, camion, reloj, surtidores):
    ocupados = list(filter(lambda surtidor: surtidor.ocupado == True, surtidores))
    surtidor = list(filter(lambda s: s.camion_atendiendo.id == camion.id, ocupados))[0]
    surtidor.camion_atendiendo = None
    surtidor.ocupado = False

#Creo evento de fin de atencion 
def programar_evento_fin(fel, camion, reloj, duracion):
    tipo = 'FA'
    reloj_inicio = reloj + duracion
    evento = Evento(tipo, camion, reloj_inicio,0)
    fel.append(evento)

#Busca el primero surtidor disponible y lo marca como ocupado
def asignar_surtidor(camion, surtidores):
    desocupados = list(filter(lambda surtidor: surtidor.ocupado == False,surtidores))
    desocupados[0].camion_atendiendo = camion
    desocupados[0].ocupado = True 
    return desocupados[0]

#asignar surtidor, calcular la espera, calcular el tiempo de atencion
def atender(fel, camion, reloj, surtidores):
    surtidor = asignar_surtidor(camion, surtidores)
    camion.espera = (reloj - camion.llegada)
    duracion = (surtidor.empleado).calcular_tiempo_atencion()
    surtidor.ocupacion += duracion    
    programar_evento_fin(fel, camion, reloj, duracion)

#Creo un nuevo evento llegada, calculando su inicio y asignandole un camion.
def programar_prox_llegada(fel, camiones, reloj):
    reloj_inicio = reloj + np.random.exponential(15)
    camion = Camion(len(camiones), reloj_inicio)
    tipo ='L'
    evento = Evento(tipo, camion, reloj_inicio, 0)
    camiones.append(camion)
    fel.append(evento)

def inicializar(cant_camiones):
    fel = []
    camiones = []
    reloj = 0
    for i in range(cant_camiones):
        programar_prox_llegada(fel, camiones, reloj)
        reloj = fel[len(fel)-1].reloj_inicio
    fel.sort(key = lambda x: x.reloj_inicio)
    return fel, camiones

def inicializar_surtidores(cant_surtidores):
    surtidores = []

    empleado = EmpleadoNormal("Empleado 1", "Normal", 18, 4)
    surtidor = Surtidor("Surtidor 1", empleado)
    surtidores.append(surtidor)

    empleado = EmpleadoExponencial("Empleado 2", "Exponencial", 15)
    surtidor = Surtidor("Surtidor 2", empleado)
    surtidores.append(surtidor)

    empleado = EmpleadoExponencial("Empleado 3", "Exponencial", 16)
    surtidor = Surtidor("Surtidor 3", empleado)
    surtidores.append(surtidor)

    empleado = EmpleadoNormal("Empleado 4", "Normal", 14, 3)
    surtidor = Surtidor("Surtidor 4", empleado)
    surtidores.append(surtidor)

    if(cant_surtidores == 5):
        empleado = EmpleadoNormal("Empleado 5", "Normal", 19, 5)
        surtidor = Surtidor("Surtidor 5", empleado)
        surtidores.append(surtidor)
    
    return surtidores    
    
if __name__ == "__main__":
    CANT_EXPERIMENTOS = 60 
    CANT_CORRIDAS = 100
    CANT_SURTIDORES = 4
    CANT_CAMIONES = 94
    esperas = []


    surtidores = inicializar_surtidores(CANT_SURTIDORES)
    for i in range(CANT_EXPERIMENTOS):
        promedio_experimento = 0 
        for j in range(CANT_CORRIDAS):
            reloj = 0 
            cola = []
            fel, camiones = inicializar(CANT_CAMIONES) 
            
            while len(fel) != 0:
                evento = fel[0]
                camion = evento.camion 
                reloj = evento.reloj_inicio
            
                if evento.tipo == 'L':
                    if not all(surtidor.ocupado for surtidor in surtidores):
                        atender(fel, camion, reloj, surtidores)
                    else:
                        cola.append(camion)
                        
                if evento.tipo == 'FA':
                    finalizar_atencion(fel, evento.camion, reloj, surtidores)
                    if len(cola) != 0:
                        camion_esperando = cola[0]
                        cola.remove(camion_esperando)       
                        atender(fel, camion_esperando, reloj, surtidores)

                fel.remove(evento)
                fel.sort(key = lambda event: event.reloj_inicio)
            
            #Sumo la espera de la corrida            
            promedio_experimento += sum(c.espera for c in camiones)
        
        #Promedio por cada experimento
        esperas.append(promedio_experimento/CANT_CAMIONES)
        

    
    #Promedio de espera todas las corridas
    media = stats.mean(esperas)
    z = 2.58
    limite_inferior, limite_superior = calcular_IC(len(esperas), media, stats.stdev(esperas), z)


    print("El tiempo promedio de espera es de ",media," minutos")
    print("El Intervalo de confianza tiene un limite inferior = ",limite_inferior," y un limite superior = ",limite_superior)
    for surtidor in surtidores:
        surtidor.porcentaje_ocupacion = surtidor.ocupacion * 100 / (24 * 60 * (CANT_EXPERIMENTOS * CANT_CORRIDAS))
        print("El porcentaje de ocupacion del ",surtidor.nombre," es de ",surtidor.porcentaje_ocupacion)    
    
    graficar_histograma(esperas)
                


    

