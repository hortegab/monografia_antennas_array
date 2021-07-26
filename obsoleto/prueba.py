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
        self.Nrings=int(self.Nang/2)
        self.pasoAngular=360/self.Nang
        self.L_path=self.Nang*self.Nrings
        self.phi=np.linspace(0,360-self.pasoAngular,self.Nang)*np.pi/180
        self.theta=np.linspace(0,180-self.pasoAngular,self.Nrings)*np.pi/180
      
    # calculo de los valores de phi para todo el recorrido            
    def phi_path(self,):
        return(np.tile(self.phi, self.Nrings))

    # calculo de los valores de theta para todo el recorrido
    def theta_path(self,):
        return(zerooh(self.theta,self.Nang))

po=receiver_path(8)
fi=po.phi_path()
print('phi=',fi)
