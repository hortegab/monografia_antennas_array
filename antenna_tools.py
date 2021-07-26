# Aqui se reunen una serie de funciones que puede ser de utilidad en la definicion o configuracion de arreglos de antenas

import numpy as np

# Para apuntar el patron de un arreglo a una direccion phi,theta, usa esta funcion de la siguiente
# manera:
# * Llama esta funcion por ejemplo asi:w_apuntar=calcularFasesApuntamiento(phi,theta,posiciones)
# * ve a tu arreglo y muliplica las exitaciones por w_apuntar
def calcularFasesApuntamiento(phi,theta, posiciones):
    normal = np.array((np.cos(phi)*np.sin(theta),np.sin(phi)*np.sin(theta),np.cos(theta)))
    fases = -2*np.pi*posiciones@normal
    return fases
    

