
import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Hecho por Homero Ortega Boada y Fernando Alberto Miranda Binomi.
   Arreglo tridimensional de fuentes puntuales
        
           @param posiciones matriz real n*3 cuyos vectores fila son las posiciones x,y,z de las fuentes del arreglo
           @param excitaciones vector complejo de n elementos representando la amplitud y fase de excitación de cada fuente del arreglo 
    """

    def __init__(self, posiciones=0,excitaciones=1, patrones=None):  
        gr.sync_block.__init__(
            self,
            name='e_array-general_cc',   
            in_sig=[np.complex64, np.float32, np.float32],
            out_sig=[np.complex64]
        )
        self.posiciones = posiciones
        self.excitaciones = excitaciones
        if patrones is not None:
            self.patrones = patrones
        else:
            self.patrones = [lambda phi,theta: 1]
        
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
        
    def work(self, input_items, output_items):
        s=input_items[0]
        theta=input_items[2]
        phi=input_items[1]
        e=self.campo(phi,theta)
        
        output_items[0][:] = self.campo(phi,theta)
        return len(output_items[0])
