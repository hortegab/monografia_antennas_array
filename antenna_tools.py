# Aqui se reunen una serie de funciones que puede ser de utilidad en la definicion o configuracion de arreglos de antenas

import numpy as np
import scipy.integrate as integrate
import scipy.interpolate as interp
###############################################################################
##     Funciones utiles para el direcionamiento del patron del arreglo       ##
###############################################################################
# Para apuntar el patron de un arreglo a una direccion phi,theta, es necesario conocer las fases
# de con las que se debe alimentar a los radiadores. Para eso se usa la funcion calcularFasesApuntamiento()
# de la siguiente manera:
# * Llama esta funcion por ejemplo asi:w_apuntar=calcularFasesApuntamiento(phi,theta,posiciones)
# * ve a tu arreglo y muliplica las exitaciones por w_apuntar
# Nota: la version del profe Binomi se diferencia de esta en que entrega las exponenciales complejas
# nos pareció más claro para ususario que se entregen las fases solamente.
def calcularFasesApuntamiento(phi,theta, posiciones):
    normal = np.array((np.cos(phi)*np.sin(theta),np.sin(phi)*np.sin(theta),np.cos(theta)))
    fases = -2*np.pi*posiciones@normal
    return fases
    
###############################################################################
##                 Funciones utiles para las aperturas                       ##
###############################################################################
def amplitudCosElev(posiciones,escala=0.8):
    centro = np.mean(posiciones,axis=0)
    desplazamientos = posiciones-centro
    radios = np.linalg.norm(desplazamientos,axis=1)
    rmax=np.max(radios)
    A = 1+np.cos(np.pi*escala*radios/rmax)
    return A/np.linalg.norm(A)*A.size**.5
    
#distintos patrones de radiacion para elementos. Ver ejemplo de arreglo lineal abajo para su uso
###############################################################################
##     Patrones de radiacion que pueden ser usados en los radiadores         ##
###############################################################################

def patron1():
    # Patron arbitrario generado a partir de tabla
    if ("patron" not in dir(patron1)):
        angulosTheta = np.array([0,30,60,90,120,150,180])*np.pi/180
        intensidadesRel = np.array([1e-3,1,1.2,2,.3,.1,0])
        f_denorm = interp.interp1d(angulosTheta,intensidadesRel,kind="cubic")
        # potenciaMedia = integrate.dblquad(lambda fi,th: f_denorm(th)**2*np.sin(th),0,np.pi,-np.pi,np.pi)[0]/(4*np.pi)
        # Por haber simetria respecto al eje z, la integral se reduce a
        potenciaMedia = integrate.quad(lambda th: f_denorm(th)**2*np.sin(th),0,np.pi)[0]/2
        escala = 1/potenciaMedia**.5 # para normalizar a potencia media 1
        def patron(phi,theta):
            return escala*f_denorm(theta)
        patron1.patron = patron
    return patron1.patron

def patronDipoloCorto():
    if ("patron" not in dir(patronDipoloCorto)):
        f_denorm = np.sin
        #simetria axial, eje z
        potenciaMedia = integrate.quad(lambda th: f_denorm(th)**2*np.sin(th),0,np.pi)[0]/2
        escala = 1/potenciaMedia**.5 # para normalizar a potencia media 1
        def patron(phi,theta):
            return escala*f_denorm(theta)
        patronDipoloCorto.patron = patron
    return patronDipoloCorto.patron
def patronDipoloMediaOnda():
    self = patronDipoloCorto
    if ("patron" not in dir(self)):
        epsilon = 1e-6
        def f_denorm(theta):
            theta=np.array(theta)
            determinado = (theta > epsilon) & ((np.pi-theta) > epsilon)
            result = np.zeros(theta.shape)
            theta_determinado = theta[determinado]
            result[determinado] = np.cos(np.pi/2*np.cos(theta_determinado))/np.sin(theta_determinado) 
            return result
        #simetria axial, eje z
        potenciaMedia = integrate.quad(lambda th: f_denorm(th)**2*np.sin(th),0,np.pi)[0]/2
        escala = 1/potenciaMedia**.5 # para normalizar a potencia media 1
        def patron(phi,theta):
            return escala*f_denorm(theta)
        self.patron = patron
    return self.patron
def patronMonopoloCuartoOnda():
    self = patronMonopoloCuartoOnda
    if ("patron" not in dir(self)):
        epsilon = 1e-6
        def f_denorm(theta):
            theta=np.array(theta)
            determinado = (theta > epsilon) & (theta <= np.pi/2)
            result = np.zeros(theta.shape)
            theta_determinado = theta[determinado]
            result[determinado] = np.cos(np.pi/2*np.cos(theta_determinado))/np.sin(theta_determinado) 
            return result
        #simetria axial, eje z
        potenciaMedia = integrate.quad(lambda th: f_denorm(th)**2*np.sin(th),0,np.pi)[0]/2
        escala = 1/potenciaMedia**.5 # para normalizar a potencia media 1
        def patron(phi,theta):
            return escala*f_denorm(theta)
        self.patron = patron
    return self.patron

#def pmcoka(phi,theta):
#    pmcoi=patronMonopoloCuartoOnda()
#    p=pmcoi(phi,theta)
#    return p
##################################################################
##   Varias configuraciones de posiciones para arreglos         ##
##################################################################
#     Arreglo planar
# permite obtener las posiciones para un arreglo planar
# organizado de manera que vemos Nx filas y Ny columnas
# de manera que hay N=Nx x Ny radiadores y todos están distanciados
# de sus vecinos en una distand D x lambda
# las posiciones se entregan en forma de un vector de N elementos.

def posiciones_arreglo_planar(Nx,Ny, D):
    return D*np.array([(x,y,0) for x in range(Nx) for y in range(Ny)])
    
def posiciones_arreglo_esferico(Nx,Ny,D):
    cx=(Nx-1)/2
    cy=(Ny-1)/2
    return D*np.array([(x,y,np.sqrt(2*max(cx,cy)**2-(x-cx)**2-(y-cy)**2)) for x in range(Nx) for y in range(Ny)])

def posiciones_arreglo_cilindro(Nx,Ny,D):
    cx = (Nx-1)/2
    return D*np.array([(x,y,np.sqrt(2*cx**2-(x-cx)**2)) for x in range(Nx) for y in range(Ny)])

def posiciones_arreglo_linealz(Nz,Dz):
    return Dz*np.array([(0,0,z) for z in range(Nz)])
def posiciones_arreglo_sat_viejo():
    # Todas las distancias estan en lambdas
    # Bl el largo del panel solar
    # Ba el ancho del panel solar
    # D distancia entre radiadores de la parte basica
    Bl=3
    Ba=1
    antena11=np.array([Ba/2, Bl,0])
    antena12=np.array([-Ba/2, Bl,0])
    antena13=np.array([Ba/2, Bl-Ba,0])
    antena14=np.array([-Ba/2, Bl-Ba,0])
    arreglo1=np.array([antena11,antena12,antena13,antena14])
    return arreglo1    


def posiciones_arreglo_sat_ladoyp(Nx,Ny,D):
    # radiadores en el eje y parte positiva
    a1=posiciones_arreglo_planar(Nx,Ny,D)
    # lo siguiente es para correr el array del centro para despejar el
    # espacio que ocupa el cubo del satelite
    a1=a1+np.array([-D/2,1.5*D,0])
    return a1    

def posiciones_arreglo_sat_ladoydoble(Nx,Nypos,D):
    # radiadores en el eje y a ambos lados
    # Nypos, es el numero de elementos solo en el lado y positivo
    a1=posiciones_arreglo_sat_ladoyp(Nx,Nypos,D)
    a2=a1+np.array([0,-(Nypos+2)*D,0])
    return np.concatenate((a1,a2))

def posiciones_arreglo_sat_ladoxp(Nx,Ny,D):
    a1=posiciones_arreglo_planar(Nx,Ny,D)
    # lo siguiente es para correr el array del centro para despejar el
    # espacio que ocupa el cubo del satelite
    a1=a1+np.array([1.5*D,-D/2,0])
    return a1    
def posiciones_arreglo_sat_ladoxdoble(Nxpos,Ny,D):
    # radiadores en el eje y a ambos lados
    # Nypos, es el numero de elementos solo en el lado y positivo
    a1=posiciones_arreglo_sat_ladoxp(Nxpos,Ny,D)
    a2=a1+np.array([-(Nxpos+2)*D,0,0])
    return np.concatenate((a1,a2)) 

def posiciones_arreglo_sat_full(Nx,Ny,D):
   a1=posiciones_arreglo_sat_ladoydoble(Nx,Ny,D)
   a2=posiciones_arreglo_sat_ladoxdoble(Ny,Nx,D)
   return np.concatenate((a1,a2)) 
   #return a1
      

