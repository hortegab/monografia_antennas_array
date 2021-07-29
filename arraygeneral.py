#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: arraygeneral
# GNU Radio version: 3.9.0.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import antenna_tools  # embedded python module
import epy_block_0
import epy_block_0_1_0_0_0
import numpy as np
import ruta3d  # embedded python module



from gnuradio import qtgui

class arraygeneral(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "arraygeneral", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("arraygeneral")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "arraygeneral")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.Ny = Ny = 4
        self.Nx = Nx = 4
        self.D = D = 0.4
        self.theta_apuntar_gr = theta_apuntar_gr = 45
        self.posiciones = posiciones = D*np.array([(x,y,0) for x in range(Nx) for y in range(Ny)])
        self.phi_apuntar_gr = phi_apuntar_gr = 45
        self.w_magnitudes = w_magnitudes = antenna_tools.amplitudCosElev(posiciones)
        self.w_fases = w_fases = antenna_tools.calcularFasesApuntamiento(phi_apuntar_gr*np.pi/180,theta_apuntar_gr*np.pi/180, posiciones)
        self.N = N = Nx*Ny
        self.samp_rate = samp_rate = 32000
        self.po = po = ruta3d.receiver_path(128)
        self.patrones = patrones = None
        self.excitaciones = excitaciones = w_magnitudes*np.exp(1j*w_fases)
        self.Rmax = Rmax = N

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("Campo E")

        labels = ['Campo E', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, 0)
            self.qtgui_number_sink_0.set_max(i, Rmax)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.epy_block_0_1_0_0_0 = epy_block_0_1_0_0_0.polar_graf_f(samp_rate=samp_rate, Rmax=Rmax, phi=po.phi, theta=po.theta, posiciones=posiciones, excitaciones=excitaciones)
        self.epy_block_0_1_0_0_0.set_block_alias("3d_f")
        self.epy_block_0 = epy_block_0.blk(posiciones=posiciones, excitaciones=excitaciones, patrones=patrones)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, po.L_path)
        self.blocks_vector_source_x_0_0 = blocks.vector_source_f(po.theta_path(), False, 1, [])
        self.blocks_vector_source_x_0 = blocks.vector_source_f(po.phi_path(), False, 1, [])
        self.blocks_throttle_0_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_float*1, po.L_path)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_throttle_0_0_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.epy_block_0, 1))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.epy_block_0, 2))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.epy_block_0_1_0_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_throttle_0_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "arraygeneral")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_Ny(self):
        return self.Ny

    def set_Ny(self, Ny):
        self.Ny = Ny
        self.set_N(self.Nx*self.Ny)
        self.set_posiciones(self.D*np.array([(x,y,0) for x in range(self.Nx) for y in range(self.Ny)]))

    def get_Nx(self):
        return self.Nx

    def set_Nx(self, Nx):
        self.Nx = Nx
        self.set_N(self.Nx*self.Ny)
        self.set_posiciones(self.D*np.array([(x,y,0) for x in range(self.Nx) for y in range(self.Ny)]))

    def get_D(self):
        return self.D

    def set_D(self, D):
        self.D = D
        self.set_posiciones(self.D*np.array([(x,y,0) for x in range(self.Nx) for y in range(self.Ny)]))

    def get_theta_apuntar_gr(self):
        return self.theta_apuntar_gr

    def set_theta_apuntar_gr(self, theta_apuntar_gr):
        self.theta_apuntar_gr = theta_apuntar_gr
        self.set_w_fases(antenna_tools.calcularFasesApuntamiento(self.phi_apuntar_gr*np.pi/180,self.theta_apuntar_gr*np.pi/180, self.posiciones))

    def get_posiciones(self):
        return self.posiciones

    def set_posiciones(self, posiciones):
        self.posiciones = posiciones
        self.set_w_fases(antenna_tools.calcularFasesApuntamiento(self.phi_apuntar_gr*np.pi/180,self.theta_apuntar_gr*np.pi/180, self.posiciones))
        self.epy_block_0.posiciones = self.posiciones
        self.epy_block_0_1_0_0_0.posiciones = self.posiciones
        self.set_w_magnitudes(antenna_tools.amplitudCosElev(self.posiciones))

    def get_phi_apuntar_gr(self):
        return self.phi_apuntar_gr

    def set_phi_apuntar_gr(self, phi_apuntar_gr):
        self.phi_apuntar_gr = phi_apuntar_gr
        self.set_w_fases(antenna_tools.calcularFasesApuntamiento(self.phi_apuntar_gr*np.pi/180,self.theta_apuntar_gr*np.pi/180, self.posiciones))

    def get_w_magnitudes(self):
        return self.w_magnitudes

    def set_w_magnitudes(self, w_magnitudes):
        self.w_magnitudes = w_magnitudes
        self.set_excitaciones(self.w_magnitudes*np.exp(1j*self.w_fases))

    def get_w_fases(self):
        return self.w_fases

    def set_w_fases(self, w_fases):
        self.w_fases = w_fases
        self.set_excitaciones(self.w_magnitudes*np.exp(1j*self.w_fases))

    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N
        self.set_Rmax(self.N)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0_0_0.set_sample_rate(self.samp_rate)

    def get_po(self):
        return self.po

    def set_po(self, po):
        self.po = po

    def get_patrones(self):
        return self.patrones

    def set_patrones(self, patrones):
        self.patrones = patrones
        self.epy_block_0.patrones = self.patrones

    def get_excitaciones(self):
        return self.excitaciones

    def set_excitaciones(self, excitaciones):
        self.excitaciones = excitaciones
        self.epy_block_0.excitaciones = self.excitaciones
        self.epy_block_0_1_0_0_0.excitaciones = self.excitaciones

    def get_Rmax(self):
        return self.Rmax

    def set_Rmax(self, Rmax):
        self.Rmax = Rmax
        self.epy_block_0_1_0_0_0.Rmax = self.Rmax




def main(top_block_cls=arraygeneral, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
