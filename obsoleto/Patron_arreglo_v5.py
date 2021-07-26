#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'notebook')
#%matplotlib qt
import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate
import scipy.interpolate as interp


# In[ ]:


def grafica3d(ax,f,phi,theta,corteLobuloPrincipal=2**-.5):
    THETA, PHI = np.meshgrid(theta,phi)
    R = f(PHI,THETA)
    X = R * np.cos(PHI) * np.sin(THETA)
    Y = R * np.sin(PHI) * np.sin(THETA)
    Z = R * np.cos(THETA)
    Rmax = np.max(R)
    ax.set_xlim(-Rmax,Rmax)
    ax.set_ylim(-Rmax,Rmax)
    ax.set_zlim(-Rmax,Rmax)
    Rhp=Rmax*corteLobuloPrincipal
    lpr=np.reshape(R>=Rhp,R.shape+(1,))
    colores = cm.winter(R/Rhp)*(~lpr)+cm.inferno(R/Rmax)*(lpr)
    # colores[:,:,-1]=.5 # transparencia
    ax.plot_surface(X,Y,Z,rcount=100,ccount=100,facecolors=colores,shade=False)
    return Rmax


# In[ ]:


class ArregloGeneral(object):

    def __init__(self,posiciones,excitaciones,patrones = None):
        """Arreglo tridimensional de fuentes puntuales
        
           @param posiciones matriz real n*3 cuyos vectores fila son las posiciones x,y,z de las fuentes del arreglo
           @param excitaciones vector complejo de n elementos representando la amplitud y fase de excitación de cada fuente del arreglo
           """
        self.posiciones = posiciones
        self.excitaciones = excitaciones
        if patrones is not None:
            self.patrones = patrones
        else:
            self.patrones = [lambda phi,theta: 1]
            
    def apuntar(self,phi,theta):
        """Modifica las fases de las excitaciones manteniendo sus amplitudes para apuntar el haz principal en la dirección dada
        
        @param phi ángulo diedro del plano xz al plano xr donde r es la dirección de apuntamiento
        @param theta ángulo del eje z al vector de apuntamiento r
        """
        
        pesos = np.abs(self.excitaciones)
        self.excitaciones = pesos*self.calcularFasesApuntamiento(phi,theta)
    
    def calcularFasesApuntamiento(self,phi,theta):
        normal = np.array((np.cos(phi)*np.sin(theta),np.sin(phi)*np.sin(theta),np.cos(theta)))
        fases = -2*np.pi*self.posiciones@normal

        return np.exp(1j*fases)

    def _campo_dirUnica(self,phi_i,theta_i):
        normal = np.array((np.cos(phi_i)*np.sin(theta_i),np.sin(phi_i)*np.sin(theta_i),np.cos(theta_i)))
        fases = 2*np.pi*self.posiciones@normal
        if len(self.patrones) == 1:
            patronAntena = self.patrones[0](phi_i,theta_i)
            return patronAntena*sum(self.excitaciones*np.exp(1j*fases))
        else:
            patronesAntenas = np.array([g_i(phi_i,theta_i) for g_i in self.patrones])
            return sum(self.excitaciones*patronesAntenas*np.exp(1j*fases))

    def _densidadPotencia_dirUnica(self,phi_i,theta_i):
        return (np.abs(self._campo_dirUnica(phi_i,theta_i))**2)/(2*120*np.pi)
    def _potenciaMedia(self):
        # Los primeros límites de integración corresponden a la segunda variable de la función integrando!!
        return integrate.dblquad(lambda phi,theta: self._densidadPotencia_dirUnica(phi,theta)*np.sin(theta)
                                 ,0,np.pi,-np.pi,np.pi)[0]/(4*np.pi)
    def directividad(self,phi,theta):
        promedio=self._potenciaMedia()
        def directividad_dirUnica(phi_i,theta_i):
            return self._densidadPotencia_dirUnica(phi_i,theta_i)/promedio
        
        directividad_vec = np.vectorize(directividad_dirUnica)
        return directividad_vec(phi,theta)
    
    def campo(self,phi,theta):
        campo_vec = np.vectorize(self._campo_dirUnica)

        return campo_vec(phi,theta)


# In[ ]:


def graficaDirectividad(arreglo,phi,theta,nombre="",ax=None):
    if ax is None:
        ax = plt.subplot(projection = '3d')
    Rmax = grafica3d(ax,arreglo.directividad,phi,theta,corteLobuloPrincipal=.5)
    ax.set_title("Directividad "+nombre+" max: %g"%Rmax)
def graficaCampo(arreglo,phi,theta,nombre="",ax=None):
    if ax is None:
        ax = plt.subplot(1,2,2,projection = '3d')
    Rmax = grafica3d(ax,lambda x,y: np.abs(arreglo.campo(x,y)),phi,theta)
    ax.set_title("$|E|$ "+nombre+" max: %g"%Rmax)
def graficaExcitaciones(arreglo,nombre="",ax=None):
    def sep_xyz(filas_xyz):
        return (filas_xyz[:,0],filas_xyz[:,1],filas_xyz[:,2])
    if ax is None:
        ax = plt.subplot(projection='3d')
        
    pmin=arreglo.posiciones.min()
    pmax=arreglo.posiciones.max()
    lims = (pmin-(pmax-pmin)*.1,pmax+(pmax-pmin)*.1)

    ax.plot3D(*sep_xyz(arreglo.posiciones),'or')
    Emax=np.abs(arreglo.excitaciones).max()
    if arreglo.posiciones.shape[0]>1:
        dmin=min((np.linalg.norm(x-y) for x in arreglo.posiciones for y in arreglo.posiciones if np.linalg.norm(x-y) >0))
        factor = .618*dmin/Emax
    else:
        factor = 1
        lims = (-1,1)
    ax.quiver(*sep_xyz(arreglo.posiciones),
              arreglo.excitaciones.real*factor,arreglo.excitaciones.imag*factor,np.zeros(arreglo.excitaciones.shape))
    ax.set_xlim(*lims)
    ax.set_ylim(*lims)
    ax.set_zlim(*lims)
    ax.set_title("Alimentación "+nombre)
    
def dibujaFigura2(arreglo,phi,theta,directividad=True,nombre=""):
        
    a1=arreglo
        
    plt.figure()
    if directividad:
        graficaDirectividad(arreglo,phi,theta,nombre,plt.subplot(1,2,1,projection='3d'))
        graficaCampo(arreglo,phi,theta,nombre,plt.subplot(1,2,2,projection='3d'))
    else:
        graficaCampo(arreglo,phi,theta,nombre)
    
    plt.figure()
    ax = plt.subplot(1,2,1)
    ax.plot(theta,np.abs(a1.campo(0,theta)))

    ax.set_title("Patron $\\phi=0$ "+nombre)


    ax = plt.subplot(1,2,2,projection='3d')
    graficaExcitaciones(arreglo,nombre,ax)
    


# In[ ]:


def amplitudCosElev(posiciones,escala=0.8):
    centro = np.mean(posiciones,axis=0)
    desplazamientos = posiciones-centro
    radios = np.linalg.norm(desplazamientos,axis=1)
    rmax=np.max(radios)
    A = 1+np.cos(np.pi*escala*radios/rmax)
    return A/np.linalg.norm(A)*A.size**.5


# In[ ]:


plt.figure()
D=0.5
N=100
posiciones=D*np.array([(x,0,0) for x in range(N)])
plt.plot(amplitudCosElev(posiciones))


# In[ ]:


#distintos patrones de radiación para elementos. Ver ejemplo de arreglo lineal abajo para su uso

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


# In[ ]:


# una sola antena, para probar patrones

posiciones=np.array([[0,0,0]])
exitaciones = np.array([1])
patrones = [patronMonopoloCuartoOnda()]

arreglo = ArregloGeneral(posiciones,exitaciones,patrones)


phi = np.linspace(-np.pi,np.pi,100)
theta = np.linspace(0,np.pi,600)

dibujaFigura2(arreglo,phi,theta)


# In[ ]:


# ejemplo arreglo planar
D=0.4
Nx=4
Ny=4
N=Nx*Ny

#arreglo sobre superficie esférica
posiciones=D*np.array([(x,y,0) for x in range(Nx) for y in range(Ny)])
#posiciones=D*np.array([(x,y,np.sqrt(2*1.5**2-(x-1.5)**2+(y-1.5)**2)) for x in range(Nx) for y in range(Ny)])
#posiciones=D*np.array([(x,y,np.sqrt(2*1.5**2-(x-1.5)**2-(y-1.5)**2)) for x in range(Nx) for y in range(Ny)])

exitaciones = np.array([1]*N)
exitaciones = amplitudCosElev(posiciones)
patrones = None

arreglo = ArregloGeneral(posiciones,exitaciones,patrones)

arreglo.apuntar(0*np.pi/180,0*np.pi/180)

phi = np.linspace(-np.pi,np.pi,100)
theta = np.linspace(0,np.pi,600)

dibujaFigura2(arreglo,phi,theta)


# In[ ]:


# ejemplo arreglo en superficie esférica
D=0.4
Nx=4
Ny=4
N=Nx*Ny

cx=(Nx-1)/2
cy=(Ny-1)/2
posiciones=D*np.array([(x,y,np.sqrt(2*max(cx,cy)**2-(x-cx)**2-(y-cy)**2)) for x in range(Nx) for y in range(Ny)])

exitaciones = np.array([1]*N)
exitaciones = amplitudCosElev(posiciones)
patrones = None

arreglo = ArregloGeneral(posiciones,exitaciones,patrones)

arreglo.apuntar(0*np.pi/180,0*np.pi/180)

phi = np.linspace(-np.pi,np.pi,100)
theta = np.linspace(0,np.pi,600)

dibujaFigura2(arreglo,phi,theta)


# In[ ]:


# ejemplo arreglo en superficie cilíndrica
D=0.4
Nx=4
Ny=4
N=Nx*Ny

# el cilindro tiene un eje paralelo al eje y
cx = (Nx-1)/2
posiciones=D*np.array([(x,y,np.sqrt(2*cx**2-(x-cx)**2)) for x in range(Nx) for y in range(Ny)])

exitaciones = np.array([1]*N)
exitaciones = amplitudCosElev(posiciones)
patrones = None

arreglo = ArregloGeneral(posiciones,exitaciones,patrones)

arreglo.apuntar(0*np.pi/180,0*np.pi/180)

phi = np.linspace(-np.pi,np.pi,100)
theta = np.linspace(0,np.pi,600)

dibujaFigura2(arreglo,phi,theta)


# In[ ]:


# ejemplo arreglo lineal
# 4 dipolos de media onda verticales, separados 0.6 longitudes de onda
# El patrón presenta simetría según el eje z
# Distribución de potencia no uniforme exponencial con un máximo en la antena inferior y mínimo en la superior

D=0.6
Nz=4
N=Nz

posiciones=D*np.array([(0,0,z) for z in range(Nz)])

excitaciones = 1.618**(-np.array([0,1,2,3]))
excitaciones = (excitaciones / np.linalg.norm(excitaciones))*excitaciones.size**.5
patrones = [patronDipoloMediaOnda()]

arreglo = ArregloGeneral(posiciones,excitaciones,patrones)

arreglo.apuntar(0,120*np.pi/180)

phi = np.linspace(-np.pi,np.pi,100)
theta = np.linspace(0,np.pi,600)

dibujaFigura2(arreglo,phi,theta)


# In[ ]:





# In[ ]:




