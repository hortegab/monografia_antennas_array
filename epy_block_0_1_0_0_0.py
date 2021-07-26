from mpl_toolkits import mplot3d
import numpy as np
from gnuradio import gr
import matplotlib.pyplot as plt

class polar_graf_f(gr.sync_block):
    """
Hecho por Homero Ortega Boada. Universidad Industrial de Santander.
Permite hacer una grafica polar con coordenadas esfericas como es el caso del patron de radaicacion de un arreglo de antenas. Las graficas las hacemos con herramientas externas a GNU Radio ya que al momento no sabiamos como hacerlo de otra manera. Los parametros de entrada son:

* samp_rate: es la frecuencia de muestreo en Hz que nunca falta en GNURadio. Influye en la velocidad de la grafica, supuestamente se los valores de medicion del  campo llegan con esa rata
* Rmax sirve para definir los limites de la grafica, se supone que es el máximo valor que puede llegar a tomar el campo en magnitud
* phi: son los valores unicos usados en la grafica para phi. Usualmente phi es un vector de valores entre 0 y 2pi con un cierto paso angular
theta: son los valores unicos usados en la grafica. Usualmente phi es un vector de valores entre 0 y pi con el mismo paso angular que phi. De manera que este vector tiene 2 veces menos valores que phi
* La senal que entra al bloque corresponde a las mediciones de campo realizadas  para todos los posibles ubicaciones angulares que se puede lograr con las combinaciones de phi y theta

Nota: Por ahora no hemos pretendido que el patron se pueda redibujar en tiempo real para nuevas situaciones. Ppor ejemplo, que si en cierto momento cambia la alimentacion de los elementos de radiacion que entonces el patron se redibuje adotando la nueva forma. Si queremos lograr eso, es posible que haya que hacer unas ligeras modidificaciones a la funcione que grafica, para que, cada vez que dibuje un nuevo patron previamente borre el anterior. Quiza tambien haya que quitar el plt.show() 

Retos para mejorar: es mas natural que el bloque pueda identifcar phi y theta a partir de las senals que aporta la ruta, es decir, usando las mismas senales que usa el bloque e_polar_graf_3d_p_f
"""
    def __init__(self,samp_rate=32000, Rmax=8,phi=0,theta=0 ):
        gr.sync_block.__init__(self,
            name="e_polar_graf_3d_f",
            in_sig=[np.float32],
            out_sig=None)
            
        # Parametros                   
        self.Tsamp=1./samp_rate
        self.Rmax=Rmax
        self.contador=0
        self.phi=phi
        self.theta=theta
        
    # Canvas grafica la plantilla sobre la que se posicionara la grafica 3d
    def canvas_3d(self, Rmax, nombre):
        fig=plt.figure()
        ax2=fig.add_subplot(111, projection='3d')
        ax2.set_xlim(-Rmax,Rmax)
        ax2.set_ylim(-Rmax,Rmax)
        ax2.set_zlim(-Rmax,Rmax)
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')
        ax2.set_zlabel('z')
        ax2.set_title(nombre)
        return ax2

    # Traduccion de coordenadas esfericas a cartecianas
    def esferica2cartesiana(self,phi,theta,R):
        x = R * np.cos(phi) * np.sin(theta)
        y = R * np.sin(phi) * np.sin(theta)
        z = R * np.cos(theta)
        return(x,y,z)                                   

    def work(self, input_items, output_items):
        # Inicialmente se deben crear 3 matrices de NringsxNang:
        # * PHI
        # * THETA
        # * R
        # Nrings: es el numero de filasy equivale al numero de anillos en la graf 3d
        # Nang: es el numero de columnas y a la vez de puntos por cada anillo de la graf 3d
        R_path=input_items[0] 
        Nang=len(self.phi) 
        Nrings=len(self.theta)
        PHI,THETA=np.meshgrid(self.phi,self.theta)
        R=R_path.reshape(Nrings,Nang)
        X,Y,Z=self.esferica2cartesiana(PHI,THETA,R)
        
        # El if  es porque el canva solo se dibuna una vez y no hemos logrado que se haga
        # dentro del constructor.
        if self.contador == 0:
           self.contador=1
           ax2=self.canvas_3d(self.Rmax, 'Patron 3d')

        # Finalmente se ordena la grafica de los valores en X,Y,Z       
        #ax2.plot_wireframe(X,Y,Z)
        #plt.clr()
        ax2.plot_surface(X,Y,Z,cmap="coolwarm")
        plt.pause(self.Tsamp)
        plt.show()
        return len(input_items[0])
