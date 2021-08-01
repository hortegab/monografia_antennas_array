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
# nos parecio mas claro para ususario que se entregen las fases solamente.
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
    
## pruebas
pp=patronMonopoloCuartoOnda
print("Ej1, pp=", pp(np.pi/4,np.pi/8))
#print("Ej1, pp=", pp(np.pi/4))
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
