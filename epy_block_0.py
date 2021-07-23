"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Calculo los pesos complejos que afectan a la onda debido a la ubicacion del elemento radiador en el espacio"""

    def __init__(self,N=4,distancias=0):
        """fase_weight"""
        gr.sync_block.__init__(
            self,
            name='fase_weight',   
            in_sig=[np.float32],
            out_sig=[np.complex64,np.complex64,np.complex64,np.complex64]
        )
        self.distancias = distancias
        self.N=N

    def work(self, input_items, output_items):
        theta_i_gr=input_items[0]
        fases=-2*np.pi*self.distancias*np.cos(theta_i_gr*np.pi/180)
        output_items[:] = np.exp(fases*1j)
        return len(output_items[0])
