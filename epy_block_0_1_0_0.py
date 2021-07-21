import numpy as np
from gnuradio import gr
import matplotlib.pyplot as plt

class polar_graf_f(gr.sync_block):
    """
    Grafica polar, pero los valores a graficar estan dados por la senal de magnitud entrante y el parametro angular theta. Hecho por Homero Ortega Boada. Universida Industrial de Santander.
Hecho con el fin de graficar cosas comos patron de radiacion de una antena, aunque inicialmente se inspiró en el visor de constelaciones. Rmax sirve para definir los limites de la grafica"""
    def __init__(self,samp_rate=32000, theta=0, Rmax=8, nombrex='Plano xy', nombrey='Eje z'):
        gr.sync_block.__init__(self,
            name="e_polar_graf_f",
            in_sig=[np.float32],
            out_sig=None)

        #########################################
        ##        Parametros                   ##
        #########################################
        self.Tsamp=1./samp_rate
        self.theta=theta
        self.Rmax=Rmax
        self.nombrex=nombrex
        self.nombrey=nombrey
        self.contador=0
        self.fig=0
        self.ax=0
        #self.xb=0
        #self.yb=0
                        
    def work(self, input_items, output_items):
        R=input_items[0]
        z=R*np.cos(self.theta)
        y=R*np.sin(self.theta)
        if self.contador == 0:
           self.contador=1
           self.fig=plt.figure()
           self.ax=self.fig.add_subplot(111)
           self.ax.set_xlim(-self.Rmax,self.Rmax)
           self.ax.set_ylim(-self.Rmax,self.Rmax)
           plt.ylabel(self.nombrey)
           plt.xlabel(self.nombrex)
        
        #self.ax.scatter(self.xb,self.yb,c='w', marker='o')
        
        self.ax.plot(y,z, color="blue")
        plt.pause(self.Tsamp)
        
        #L=len(R)
        #self.xb=y[L-1]
        #self.yb=z[L-1]
        #self.ax.scatter(self.xb,self.yb,c='r', marker='o')
        # plt.clf() # esto limpia la grafica
        return len(input_items[0])
