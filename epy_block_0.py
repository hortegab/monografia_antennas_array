
import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Hecho por Homero Ortega Boada con la tutoria y de Fernando Alberto Miranda Binomi.
   Arreglo tridimensional de fuentes puntuales con radiadores isotropicos.

   Parametros y senales:
   * Por In0 entra la envolvente compleja de la senal a ser transmitida.
   * Por In1 y In2 llega la posicion actual del receptor en coordenadas esfericas. In1 para phi, In2 para theta
   * La salida es la senal que entra por In0 pero afectada por su paso atraves del arreglo
   * posiciones: es un vector de longitud N, el cual contiene las posiciones en el espacio 3d de los N radiadores que componen el arreglo. Solo hay que tener en cuenta que cada posicion consta de 3 elementos que representan las coordenadas x,y,x. Por eso, desde el punto de vista de todos los datos, "posiciones" es una matrix N x 3
   * excitaciones: Es el vector de longitud N que contiene las exitaciones para cada uno de los N radiadores. Usualmente esos valores son coplejos, donde la magnitud impacta a la apertura del arreglo, mientras que las fases impactan la direccionalidad del patron. Si no se desea impactar nada de eso, las excitaciones puede ser un vector de puros unos.
   
   Nota: es posible usar este bloque para obtener el patron del arreglo teniendo en cuenta lo siguiente:
   * se senal en In0 puede ser igual a 1, pero solo para mejorar la velocidad del calculo
   * las senales In1, In2 deben representar la ruta, en angulos phi, theta, que el receptor realiza, como si se tratara de un drone que va volando al rededor del arreglo mientras mide el campo, hasta cubrir todos esos angulos.   
   
   Nota para disenadores: este bloque es una evolucion del bloque e_array_general_cc con el fin de lograr soluciones mas modulares y mas sencillas, de manera mas acorde con la vision de GNU Radio. La simplicidad se logron teniendo en cuenta que hay varias cosas que pueden ser realizadas por otros bloques externos, entres esas cosas estan:
   * En la practica los radiadores son casi siempre de patron similar, En ese caso, un bloque externo puede hacer el ajuste correspondiente para considerar la forma de ese patron.
   * La directividad y la densidad de potencia. Son parametros que son mas del interes de un sistema de medicion que de un sistema de tiempo real.  
    """

    def __init__(self, posiciones=0,excitaciones=1):  
        gr.sync_block.__init__(
            self,
            name='e_array_iso_cc',   
            in_sig=[np.complex64, np.float32, np.float32],
            out_sig=[np.complex64]
        )
        self.posiciones = posiciones
        self.excitaciones = excitaciones
        
    def _campo_dirUnica(self,phi_i,theta_i):
        # normal es el vector que aparece en formula Maillou que senala la direccion de observacion
        normal = np.array((np.cos(phi_i)*np.sin(theta_i),np.sin(phi_i)*np.sin(theta_i),np.cos(theta_i)))
        # @ es para que se surta el producto matricial porque el uso de * seria un producto punto o escalar
        fases = 2*np.pi*self.posiciones@normal
        return sum(self.excitaciones*np.exp(1j*fases))
 
    def campo(self,phi,theta):
        campo_vec = np.vectorize(self._campo_dirUnica)
        return campo_vec(phi,theta)
        
    def work(self, input_items, output_items):
        s=input_items[0]
        theta=input_items[2]
        phi=input_items[1]
        e=output_items[0]
        e[:]=self.campo(phi,theta)
        return len(output_items[0])
