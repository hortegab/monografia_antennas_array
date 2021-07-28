# Aqui se reunen una serie de funciones que puede ser de utilidad en la definicion o configuracion de arreglos de antenas

import numpy as np

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
    
#distintos patrones de radiación para elementos. Ver ejemplo de arreglo lineal abajo para su uso
###############################################################################
##     Patrones de radiacion que pueden ser usados en los radiadores         ##
###############################################################################

def patron1():
    # Patrón arbitrario generado a partir de tabla
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

##################################################################
##   Varias configuraciones de posiciones para arreglos         ##
##################################################################
#     FALTA     FALTA

