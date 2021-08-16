# Lo que hace este programa es lo siguiente:
# * calcula todos los valores angulares en los que un
# receptor se debe ubicar con el fin de poder 
# medir todos los valores de campo y con todo eso
# poder graficar el patron de radiacion en 3d
# * A diferencia de lo que se hace en la programacion
# tradicional, donde se dice que phi tiene unos valore
# entre 0 y 360 grados y theta entre 0 y 180, aqui, por usar
# programacion de tiempo real hay que imaginar que tomamos un dron
# y le pre-programos toda la ruta que hay que seguir para 
# sea posible obtener todos los datos del patron de radiacion
# de un arreglo
#
# Como se usa:
# * supongamos que Ud desea que la ruta se haga que tenga Nang=128 puntos angulares por cada anilo
# Entonces crea el objeto po=receiver_path(128) . Nota Nang debe ser tipo 2 a la m
# * puede obtener los valores unicos de phi como po.phi
# * los de theta como po.theta
# * los valores que phi para toda la ruta como po.phi_path()
# * los valores que theta para toda la ruta como po.theta_path()
# * tambien se puede acceder al numero de anillos que la grafica
# tendra en el eje z como po.Nrings
# * igualmente, el numero de puntos de cada anillo po.Nang
# * y el numero de puntos de toda la ruta po.L_path

import numpy as np

def zerooh(x,Sps):
    Lx=len(x)
    g=np.array([x[0]]*Sps)
    for i in range(1,Lx):
        g=np.concatenate((g,np.array([x[i]]*Sps)))
    return g

class receiver_path(object):
    def __init__(self, Nang):
        self.Nang=Nang
        self.Nrings=int(Nang/2)
        self.pasoAngular=360/Nang
        self.L_path=Nang*self.Nrings
        self.phi=np.linspace(0,360,Nang)*np.pi/180
        self.theta=np.linspace(0,180,self.Nrings)*np.pi/180
      
    # calculo de los valores de phi para todo el recorrido            
    def phi_path(self,):
        return(np.tile(self.phi, self.Nrings))

    # calculo de los valores de theta para todo el recorrido
    def theta_path(self,):
        return(zerooh(self.theta,self.Nang))


