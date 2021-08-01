
import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Hecho por Homero Ortega Boada con la tutoria y de Fernando Alberto Miranda Binomi.
   Ajuste de patron. Es un complemento al bloque e_array_iso_cc poder considerar el patron que puede tenen tener los radiadores de un arreglo. Pero este ajuste se limita al caso en que todos los radiadores del arreglo tienen el mismo patron
     """

    def __init__(self, patron=1):  
        gr.sync_block.__init__(
            self,
            name='e_array_ajuste_x_paton_cc',   
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.patron = patron
      
    def work(self, input_items, output_items):
        s=input_items[0]
        e=output_items[0]        
        e[:] = s*self.patron
        return len(output_items[0])
