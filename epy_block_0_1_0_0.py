from mpl_toolkits import mplot3d
import numpy as np
from gnuradio import gr
import matplotlib.pyplot as plt

class polar_graf_f(gr.sync_block):
    """
    Grafica polar, pero los valores a graficar estan dados por la senal de magnitud entrante y el parametro angular theta. Hecho por Homero Ortega Boada. Universida Industrial de Santander.
Hecho con el fin de graficar cosas comos patron de radiacion de una antena, aunque inicialmente se inspiró en el visor de constelaciones. Rmax sirve para definir los limites de la grafica"""
    def __init__(self,samp_rate=32000, Rmax=8):
        gr.sync_block.__init__(self,
            name="e_polar_graf_3d_p_f",
            in_sig=[np.float32]*3,
            out_sig=None)

        #########################################
        ##        Parametros                   ##
        #########################################
        self.Tsamp=1./samp_rate
        self.Rmax=Rmax
        self.contador=0
        #self.fig=0
        self.ax=None

    # Canvas grafica la plantilla sobre la que se posecionara la grafica 3d
    def canvas_3d(self, Rmax, nombre):
        fig=plt.figure()
        ax=fig.add_subplot(111, projection='3d')
        ax.set_xlim(-Rmax,Rmax)
        ax.set_ylim(-Rmax,Rmax)
        ax.set_zlim(-Rmax,Rmax)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title(nombre)
        return ax

    # Traduccion de coordenadas esfericas a cartecianas
    def esferica2cartesiana(self,phi,theta,R):
        x = R * np.cos(phi) * np.sin(theta)
        y = R * np.sin(phi) * np.sin(theta)
        z = R * np.cos(theta)
        return(x,y,z)                                   

    def work(self, input_items, output_items):
        R_path=input_items[0]
        theta_path=input_items[2]
        phi_path=input_items[1]
        x,y,z=self.esferica2cartesiana(phi_path,theta_path,R_path)
        
        if self.contador == 0:
           self.contador=1
           self.ax=self.canvas_3d(self.Rmax, 'Patron 3d')
               
        self.ax.cla()
        self.ax.plot(x,y,z, color="blue")
        #ax.scatter(x,y,z, c='y', marker='o')
        plt.pause(self.Tsamp)
        return len(input_items[0])
