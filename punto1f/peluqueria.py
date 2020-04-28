import numpy as np

def color(min, max):
    tiempo = np.random.uniform(min,max)
    print("Duracion del color ", tiempo, "minutos")
    return tiempo

def cortar(min, max, demora):
    
    tiempo = np.random.uniform(min,max) + np.random.random_integers(demora)
    print("Duracion del corte ", tiempo, "minutos")
    return tiempo

def lavar(min,max):
    tiempo = np.random.uniform(min, max)
    print("Duracion del lavado ", tiempo, "minutos")
    return tiempo

def clasificar_cliente(CANT_CLIENTES):
    return np.random.random_integers(2,size=(CANT_CLIENTES,1))

def calcular_demora(clientes):
    MIN_LAVADO = 3
    MAX_LAVADO = 5
    MIN_CORTE = 10
    MAX_CORTE = 15
    MIN_COLOR = 30
    MAX_COLOR = 45
    DEMORA = 5
    duracion = 0
    for cliente in clientes:
        tiempo = 0
        print("Comienza atencion tipo de cliente ", cliente)
        tiempo = lavar(MIN_LAVADO,MAX_LAVADO)
        tiempo += cortar(MIN_CORTE,MAX_CORTE, DEMORA)
        if(cliente == 2):
            tiempo += color(MIN_COLOR,MAX_COLOR)
        print("Duracion del servicio", tiempo, "minutos")
        print("----------------------------------")
        duracion += tiempo
    return duracion
if __name__ == "__main__":
    CANT_CLIENTES=5
    clientes = clasificar_cliente(CANT_CLIENTES)
    print("El tiempo maximo para un cliente del tipo 1 es 20 minutos")
    print("El tiempo maximo para un cliente del tipo 2 es 65 minutos")
    print("----------------------------------")
    duracion = calcular_demora(clientes)
    print("La duracion total del proyecto es ", duracion," minutos")
    

