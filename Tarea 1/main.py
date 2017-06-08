# coding=utf-8
"""
    Tarea 1: Radiacion termica de planta industrial

    Javier Gomez
    19.516.104-6
    javier.gomez.p@ug.uchile.cl
"""

#   Importamos librerias
import numpy as np
import random
import matplotlib.pyplot as plt
import math
import tqdm

# Entrega la pendiente m de la recta entre dos puntos (x1,y1) y (x2,y2)
def pendiente(x1,x2,y1,y2):
    dy = y2-y1 #int
    dx = x2-x1 #int
    m = (dy * 1.0) / dx
    return m  # m no es int

# Entrega -1 o 1 aleatoriamente (se utilizará para aumentar o disminuir los puntos en las cordilleras)
def randPercent():
    a = random.randint(0,10)
    if a >= 5:
        return -1
    else:
        return 1

# Entrega la temperatura del agua (condicion de borde) en un tiempo t
def tagua(t):
    if t <=8:
        return 4
    elif t <= 16:
        return t*2 - 12
    else:
        return -2*t + 52

# Entrega la temperatura de la planta en un tiempo t
def tempPlanta(t): # T perteneces a [0, 24]
    return 500 * (math.cos((t*math.pi) / 12) + 2)

# Creamos la clase Litoral con sus parametros
class Litoral(object):
    def __init__(self, h, t1, t2, t3, t4, t5, it, alpha):

        # Alpha (Bonus 3)
        self.alpha = alpha
        # Numero de iteraciones
        self.it = it

        # Tamaño del perfil
        self.alto = 2000  # metros
        self.ancho = 4000  # metros

        # Declaramos h y t
        self.h = h
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4
        self.t5 = t5

        # Tamaño de la matriz
        self.anchom = self.ancho / self.h
        self.altom = self.alto / self.h

        # Creamos la matriz
        self.matrizCB = np.zeros((self.altom, self.anchom))  # matriz caso base
        self.matriz1 = np.zeros((self.altom, self.anchom))   #
        self.matriz2 = np.zeros((self.altom, self.anchom))   #
        self.matriz3 = np.zeros((self.altom, self.anchom))   #
        self.matriz4 = np.zeros((self.altom, self.anchom))   #
        self.matriz5 = np.zeros((self.altom, self.anchom))   #

    # Fx's para la temperatura de la atmosfera para el caso base
    def eq(self, y, t):
        pendiente = (-1 * 12.0) / self.altom
        r = pendiente * y + tagua(t)
        return r

    # Generacion del terreno
    def perf(self):
        # AGUA
        porcentaje_raw = random.randint(30, 40)
        limite = int(abs((porcentaje_raw / 100.0) * self.anchom))

        # T de la atmosfera en caso base
        j= self.altom
        for i in range(0, self.altom - (int(self.altom * 0.1))):
            self.matrizCB[i, :] = self.eq(j,self.t1)
            self.matriz1[i,:] = self.eq(j,self.t1)
            self.matriz2[i, :] = self.eq(j,self.t2)
            self.matriz3[i, :] = self.eq(j,self.t3)
            self.matriz4[i, :] = self.eq(j,self.t4)
            self.matriz5[i, :] = self.eq(j,self.t5)
            j -= 1

        ##rellenamos las ultimas filas (10%) con la condicion de borde (solo hasta el 30~40 %
        for i in range(1, limite + 1):
            for j in range(self.altom - (int(self.altom * 0.1)), self.altom):
                self.matrizCB[j, i - 1] = tagua(self.t1) #Caso base en t=0
                self.matriz1[j, i - 1] = tagua(self.t1)
                self.matriz2[j, i - 1] = tagua(self.t2)
                self.matriz3[j, i - 1] = tagua(self.t3)
                self.matriz4[j, i - 1] = tagua(self.t4)
                self.matriz5[j, i - 1] = tagua(self.t5)

        # MOUNTAINS
        prom = self.altom / 2

        # Para mountains
        alturas = np.ones(self.anchom - limite - (100/self.h))

        # Le damos altura inicial al bloque de montañas
        alturas *= prom
        if self.alpha == 1:
            indx1 = int((self.anchom - limite - (100/self.h))*0.1)
            indx2 = int((self.anchom - limite - (100/self.h))*0.2)
            indx3 = int((self.anchom - limite - (100/self.h))*0.3)
            indx4 = int((self.anchom - limite - (100/self.h))*0.4)
            indx5 = int((self.anchom - limite - (100/self.h))*0.5)
            indx6 = int((self.anchom - limite - (100/self.h))*0.6)
            indx7 = int((self.anchom - limite - (100/self.h))*0.7)
            indx8 = int((self.anchom - limite - (100/self.h))*0.8)
            indx9 = int((self.anchom - limite - (100/self.h))*0.9)

            # Tenemos las alturas "aleatorias", falta unirlas
            alturas[indx1] += randPercent()* random.random()*prom
            alturas[indx2] += randPercent()* random.random()*prom
            alturas[indx3] += randPercent()* random.random()*prom
            alturas[indx4] += randPercent()* random.random()*prom
            alturas[indx5] += randPercent()* random.random()*prom
            alturas[indx6] += randPercent()* random.random()*prom
            alturas[indx7] += randPercent()* random.random()*prom
            alturas[indx8] += randPercent()* random.random()*prom
            alturas[indx9] += randPercent()* random.random()*prom

            alturas[0] = int(self.altom * 0.1)

            # entre 0 y indx1
            m1 = int(pendiente(0,indx1,alturas[0],alturas[indx1])) # no es int
            j=1
            for i in range(0,indx1+1):
                if i !=0:
                    alturas[i] = m1*j + alturas[0]
                    j+=1
                else:
                    pass

            # Calculamos la pendiente entre indx1 y indx2, y siguientes
            m2 = int(pendiente(indx1,indx2,alturas[indx1],alturas[indx2]))
            j=1
            for i in range (indx1 +1, indx2+1):
                alturas[indx1+j] = m2*j + alturas[indx1]
                j+=1
            m3 = int(pendiente(indx2, indx3, alturas[indx2], alturas[indx3]))
            j = 1
            for i in range(indx2 + 1, indx3 + 1):
                alturas[indx2 + j] = m3 * j + alturas[indx2]
                j += 1

            m4 = int(pendiente(indx3, indx4, alturas[indx3], alturas[indx4]))
            j = 1
            for i in range(indx3 + 1, indx4 + 1):
                alturas[indx3 + j] = m4 * j + alturas[indx3]
                j += 1
            m5 = int(pendiente(indx4, indx5, alturas[indx4], alturas[indx5]))
            j = 1
            for i in range(indx4 + 1, indx5 + 1):
                alturas[indx4 + j] = m5 * j + alturas[indx4]
                j += 1

            m6 = int(pendiente(indx5, indx6, alturas[indx5], alturas[indx6]))
            j = 1
            for i in range(indx5 + 1, indx6 + 1):
                alturas[indx5 + j] = m6 * j + alturas[indx5]
                j += 1

            m7 = int(pendiente(indx6, indx7, alturas[indx6], alturas[indx7]))
            j = 1
            for i in range(indx6 + 1, indx7 + 1):
                alturas[indx6 + j] = m7 * j + alturas[indx6]
                j += 1

            m8 = int(pendiente(indx7, indx8, alturas[indx7], alturas[indx8]))
            j = 1
            for i in range(indx7 + 1, indx8 + 1):
                alturas[indx7 + j] = m8 * j + alturas[indx7]
                j += 1

            m9 = int(pendiente(indx8, indx9, alturas[indx8], alturas[indx9]))
            j = 1
            for i in range(indx8 + 1, indx9 + 1):
                alturas[indx8 + j] = m9 * j + alturas[indx8]
                j += 1

            m10 = int(pendiente(indx9, self.anchom - limite -1, alturas[indx9], alturas[self.anchom - limite - (100/self.h) - 1]))
            j = 1
            for i in range(indx9 + 1, self.anchom - limite - (100/self.h)):
                alturas[indx9 + j] = m10 * j + alturas[indx9]
                j += 1
        else:
            pass

        # Ingresamos mountains a la matriz (matrices)
        j = 0
        for i in range(limite + (100/self.h), self.anchom):
            for k in range(int(alturas[j])-1):
                self.matriz1[self.altom - k - 1,i-1] = np.nan
                self.matriz2[self.altom - k - 1, i - 1] = np.nan
                self.matriz3[self.altom - k - 1, i - 1] = np.nan
                self.matriz4[self.altom - k - 1, i - 1] = np.nan
                self.matriz5[self.altom - k - 1, i - 1] = np.nan
                self.matrizCB[self.altom - k - 1, i - 1] = np.nan
            j += 1

        # Agregamos la planta
        for i in range(0, (100/self.h)):
            self.matriz1[self.altom - (int(self.altom * 0.1)), limite+i-1] = tempPlanta(self.t1)
            self.matriz2[self.altom - (int(self.altom * 0.1)), limite + i - 1] = tempPlanta(self.t2)
            self.matriz3[self.altom - (int(self.altom * 0.1)), limite + i - 1] = tempPlanta(self.t3)
            self.matriz4[self.altom - (int(self.altom * 0.1)), limite + i - 1] = tempPlanta(self.t4)
            self.matriz5[self.altom - (int(self.altom * 0.1)), limite + i - 1] = tempPlanta(self.t5)

            for u in range(self.altom - (int(self.altom * 0.1))+1, self.altom):
                self.matriz1[u,limite +i -1] = np.nan
                self.matriz2[u, limite + i - 1] = np.nan
                self.matriz3[u, limite + i - 1] = np.nan
                self.matriz4[u, limite + i - 1] = np.nan
                self.matriz5[u, limite + i - 1] = np.nan
                self.matrizCB[u, limite + i - 1] = np.nan

        # Iteraciones
        for _ in tqdm.tqdm(range(self.it)):
            for x in range(1, self.anchom-1):
                for y in range(1, self.altom-(int(self.altom * 0.1))):

                    # Hacemos un ciclo para iterar sobre las 6 matrices distintas (los distintos t's)
                    for matrices in range(6):
                        if matrices == 0:
                            if np.isnan(self.matrizCB[y,x]):
                                pass
                            else:
                                A = self.matrizCB[y - 1, x]
                                B = self.matrizCB[y + 1, x]
                                C = self.matrizCB[y, x - 1]
                                D = self.matrizCB[y, x + 1]
                                if np.isnan(A):
                                    a = 15
                                else:
                                    a = A
                                if np.isnan(B):
                                    b = 15
                                else:
                                    b = B
                                if np.isnan(C):
                                    c = 15
                                else:
                                    c = C
                                if np.isnan(D):
                                    d = 15
                                else:
                                    d = D
                                self.matrizCB[y,x] = 0.25*(a+b+c+d)
                        if matrices == 1:
                            if np.isnan(self.matriz1[y,x]):
                                pass
                            else:
                                A = self.matriz1[y - 1, x]
                                B = self.matriz1[y + 1, x]
                                C = self.matriz1[y, x - 1]
                                D = self.matriz1[y, x + 1]
                                if np.isnan(A):
                                    a = 15
                                else:
                                    a = A
                                if np.isnan(B):
                                    b = 15
                                else:
                                    b = B
                                if np.isnan(C):
                                    c = 15
                                else:
                                    c = C
                                if np.isnan(D):
                                    d = 15
                                else:
                                    d = D
                                self.matriz1[y,x] = 0.25*(a+b+c+d)
                        if matrices == 2:
                            if np.isnan(self.matriz2[y,x]):
                                pass
                            else:
                                A = self.matriz2[y - 1, x]
                                B = self.matriz2[y + 1, x]
                                C = self.matriz2[y, x - 1]
                                D = self.matriz2[y, x + 1]
                                if np.isnan(A):
                                    a = 15
                                else:
                                    a = A
                                if np.isnan(B):
                                    b = 15
                                else:
                                    b = B
                                if np.isnan(C):
                                    c = 15
                                else:
                                    c = C
                                if np.isnan(D):
                                    d = 15
                                else:
                                    d = D
                                self.matriz2[y,x] = 0.25*(a+b+c+d)
                        if matrices == 3:
                            if np.isnan(self.matriz3[y,x]):
                                pass
                            else:
                                A = self.matriz3[y - 1, x]
                                B = self.matriz3[y + 1, x]
                                C = self.matriz3[y, x - 1]
                                D = self.matriz3[y, x + 1]
                                if np.isnan(A):
                                    a = 15
                                else:
                                    a = A
                                if np.isnan(B):
                                    b = 15
                                else:
                                    b = B
                                if np.isnan(C):
                                    c = 15
                                else:
                                    c = C
                                if np.isnan(D):
                                    d = 15
                                else:
                                    d = D
                                self.matriz3[y,x] = 0.25*(a+b+c+d)
                        if matrices == 4:
                            if np.isnan(self.matriz4[y,x]):
                                pass
                            else:
                                A = self.matriz4[y - 1, x]
                                B = self.matriz4[y + 1, x]
                                C = self.matriz4[y, x - 1]
                                D = self.matriz4[y, x + 1]
                                if np.isnan(A):
                                    a = 15
                                else:
                                    a = A
                                if np.isnan(B):
                                    b = 15
                                else:
                                    b = B
                                if np.isnan(C):
                                    c = 15
                                else:
                                    c = C
                                if np.isnan(D):
                                    d = 15
                                else:
                                    d = D
                                self.matriz4[y,x] = 0.25*(a+b+c+d)
                        if matrices == 5:
                            if np.isnan(self.matriz5[y,x]):
                                pass
                            else:
                                A = self.matriz5[y - 1, x]
                                B = self.matriz5[y + 1, x]
                                C = self.matriz5[y, x - 1]
                                D = self.matriz5[y, x + 1]
                                if np.isnan(A):
                                    a = 15
                                else:
                                    a = A
                                if np.isnan(B):
                                    b = 15
                                else:
                                    b = B
                                if np.isnan(C):
                                    c = 15
                                else:
                                    c = C
                                if np.isnan(D):
                                    d = 15
                                else:
                                    d = D
                                self.matriz5[y,x] = 0.25*(a+b+c+d)

    def plot(self):
        """
        Plotea la solución
        :return:
        """
        # Matriz 1
        fig = plt.figure(1)
        ax = fig.add_subplot(111)
        ax.set_title('Perfil con 100 iteraciones en t = 0')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')

        extnt = [0, self.ancho, 0, self.alto];

        # Se agrega grafico al plot
        cax = ax.imshow(self.matriz1, extent=extnt)
        fig.colorbar(cax)

        # Matriz 2
        fig = plt.figure(2)
        ax = fig.add_subplot(111)
        ax.set_title('Perfil con 100 iteraciones en t = 8')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')

        extnt = [0, self.ancho, 0, self.alto];

        # Se agrega grafico al plot
        cax = ax.imshow(self.matriz2, extent=extnt)
        fig.colorbar(cax)

        # Matriz 3
        fig = plt.figure(3)
        ax = fig.add_subplot(111)
        ax.set_title('Perfil con 100 iteraciones en t = 12')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')

        extnt = [0, self.ancho, 0, self.alto];

        # Se agrega grafico al plot
        cax = ax.imshow(self.matriz3, extent=extnt)
        fig.colorbar(cax)

        # Matriz 4
        fig = plt.figure(4)
        ax = fig.add_subplot(111)
        ax.set_title('Perfil con 100 iteraciones en t = 16')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')

        extnt = [0, self.ancho, 0, self.alto];

        # Se agrega grafico al plot
        cax = ax.imshow(self.matriz4, extent=extnt)
        fig.colorbar(cax)

        # Matriz 5
        fig = plt.figure(5)
        ax = fig.add_subplot(111)
        ax.set_title('Perfil con 100 iteraciones en t = 20')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')

        extnt = [0, self.ancho, 0, self.alto];

        # Se agrega grafico al plot
        cax = ax.imshow(self.matriz5, extent=extnt)
        fig.colorbar(cax)

        # Matriz Caso Base (para el informe)
        fig = plt.figure(6)
        ax = fig.add_subplot(111)
        ax.set_title('Perfil sin la planta con 100 iteraciones en t = 0')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')

        extnt = [0, self.ancho, 0, self.alto];

        # Se agrega grafico al plot
        cax = ax.imshow(self.matrizCB, extent=extnt)
        fig.colorbar(cax)

        plt.show()

# Creamos el objeto lit del tipo Litoral, le damos el paso h, los distintos tiempo y el numero de iteraciones
lit = Litoral(10, 0, 8, 12, 16, 20, 100, 1)
lit.perf()
lit.plot()
