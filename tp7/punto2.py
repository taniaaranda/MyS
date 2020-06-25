import numpy as np
import statistics as stats
import seaborn as sns
import matplotlib.pyplot as plt

class Evento:
    def __init__(self, tipo, cliente, reloj_inicio, duracion):
        self.tipo = tipo
        self.cliente = cliente
        self.reloj_inicio = reloj_inicio
        self.duracion = duracion

class Caja:
    def __init__(self, nombre, cajero):
        self.nombre = nombre
        self.ocupado = False
        self.cajero = cajero
        self.cliente_atendiendo = None
        self.ocupacion = 0
        self.porcentaje_ocupacion = 0 

class Cliente:
    def __init__(self, id, llegada):
        self.id = id
        self.llegada = llegada
        self.espera = 0

class Cajero:
    def __init__(self, nombre, distribucion):
        self.nombre = nombre
        self.distribucion = distribucion
    

class CajeroNormal(Cajero):
    def __init__(self, nombre, distribucion, media, desvio):
        Cajero.__init__(self, nombre, distribucion)
        self.media = media
        self.desvio = desvio

    def calcular_tiempo_atencion(self):
        return np.random.normal(self.media,self.desvio)

class CajeroExponencial(Cajero):    
    def __init__(self, nombre, distribucion, promedio):
        Cajero.__init__(self, nombre, distribucion)
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

#Busco el caja que esta atendiendo el cliente y lo marco como desocupado
def finalizar_atencion(fel, cliente, reloj, cajas):
    ocupados = list(filter(lambda caja: caja.ocupado == True, cajas))
    caja = list(filter(lambda s: s.cliente_atendiendo.id == cliente.id, ocupados))[0]
    caja.cliente_atendiendo = None
    caja.ocupado = False

#Creo evento de fin de atencion 
def programar_evento_fin(fel, cliente, reloj, duracion):
    tipo = 'FA'
    reloj_inicio = reloj + duracion
    evento = Evento(tipo, cliente, reloj_inicio,0)
    fel.append(evento)

#Busca el primero caja disponible y lo marca como ocupado
def asignar_caja(cliente, cajas):
    desocupados = list(filter(lambda caja: caja.ocupado == False,cajas))
    desocupados[0].cliente_atendiendo = cliente
    desocupados[0].ocupado = True 
    return desocupados[0]

#asignar caja, calcular la espera, calcular el tiempo de atencion
def atender(fel, cliente, reloj, cajas):
    caja = asignar_caja(cliente, cajas)
    cliente.espera = (reloj - cliente.llegada)
    duracion = (caja.cajero).calcular_tiempo_atencion()
    caja.ocupacion += duracion   
    programar_evento_fin(fel, cliente, reloj, duracion)

#Creo un nuevo evento llegada, calculando su inicio y asignandole un cliente.
def programar_prox_llegada(fel, clientes, reloj):
    reloj_inicio = reloj + np.random.exponential(10)
    cliente = Cliente(len(clientes), reloj_inicio)
    tipo ='L'
    evento = Evento(tipo, cliente, reloj_inicio, 0)
    clientes.append(cliente)
    fel.append(evento)

def inicializar(cant_clientes):
    fel = []
    clientes = []
    reloj = 0
    for i in range(cant_clientes):
        programar_prox_llegada(fel, clientes, reloj)
        reloj = fel[len(fel)-1].reloj_inicio
    fel.sort(key = lambda x: x.reloj_inicio)
    return fel,clientes

def inicializar_cajas(cant_cajas):
    cajas = []

    cajero = CajeroNormal("cajero 1", "Normal", 15, 3)
    caja = Caja("caja 1", cajero)
    cajas.append(caja)

    cajero = CajeroExponencial("cajero 2", "Exponencial", 12)
    caja = Caja("caja 2", cajero)
    cajas.append(caja)

    if cant_cajas == 3:
        cajero = CajeroNormal("cajero 3", "Normal", 14,6)
        caja = Caja("caja 3", cajero)
        cajas.append(caja)

    return cajas    
    
if __name__ == "__main__":
    CANT_EXPERIMENTOS = 365
    CANT_CORRIDAS = 1
    CANT_CAJAS = 2
    CANT_CLIENTES = 48
    RELOJ_TOPE = 8*60

    esperas = []


    cajas = inicializar_cajas(CANT_CAJAS)
    for i in range(CANT_EXPERIMENTOS):
        promedio_experimento = 0 
        for j in range(CANT_CORRIDAS):
            reloj = 0 
            cola = []
            fel,clientes = inicializar(CANT_CLIENTES) 
            
            while len(fel) != 0 or reloj <= RELOJ_TOPE:
                if len(fel) != 0: 
                    evento = fel[0]
                    cliente = evento.cliente 
                    reloj = evento.reloj_inicio
        
                    if evento.tipo == 'L':
                        if not all(caja.ocupado for caja in cajas):
                            atender(fel, cliente, reloj, cajas)
                        else:
                            cola.append(cliente)
                            
                    if evento.tipo == 'FA':
                        finalizar_atencion(fel, evento.cliente, reloj, cajas)
                        if len(cola) != 0:
                            cliente_esperando = cola[0]
                            cola.remove(cliente_esperando)       
                            atender(fel, cliente_esperando, reloj, cajas)

                    fel.remove(evento)
                    fel.sort(key = lambda cl: cl.reloj_inicio)
                else:
                    break

            #Sumo la espera de la corrida            
            promedio_experimento += sum(c.espera for c in clientes)
        
        #Promedio por cada experimento
        esperas.append(promedio_experimento/CANT_CLIENTES)
        

    
    #Promedio de espera todas las corridas
    media = stats.mean(esperas)
    z = 1.96
    limite_inferior, limite_superior = calcular_IC(len(esperas), media, stats.stdev(esperas), z)


    print("El tiempo promedio de espera es de ",media," minutos")
    print("El Intervalo de confianza tiene un limite inferior = ",limite_inferior," y un limite superior = ",limite_superior)
    for caja in cajas:
        caja.porcentaje_ocupacion = caja.ocupacion * 100 / (RELOJ_TOPE * (CANT_EXPERIMENTOS * CANT_CORRIDAS))
        print("El porcentaje de ocupacion de la ",caja.nombre," es de ",caja.porcentaje_ocupacion)    
    
    graficar_histograma(esperas)