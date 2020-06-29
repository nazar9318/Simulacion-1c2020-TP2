import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import time

CANTIDAD_DE_MOVIMIENTOS = 300 #cantidad de pasos de cada particula
CANTIDAD_DE_PARTICULAS = 1000 #cantidad de particulas de cada color
ALTO_DE_LA_CAJA = 200
ANCHO_DE_LA_CAJA = 100
PASOS_GRAFICO = 10 #cada cuantos movimientos grafica la caja

def ej9():

  matriz_particulas_azules = crear_matriz(0, 49) #genera todas las posiciones de todas las particulas a la izq (azules)
  matriz_particulas_rojas = crear_matriz(51, 100) #genera todas las posiciones de todas las particulas a la der (rojas)
  
  #grafica_densidades(matriz_particulas_azules, matriz_particulas_rojas)
  
  plt.axis([0, 100, 0, 200])
  membrana = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
  x_membrana = [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
  
  for a in range (0, CANTIDAD_DE_MOVIMIENTOS-1, PASOS_GRAFICO): #a es el numero de fila, avanza de a pasos_grafico para plotear
    for b in range (0,2*CANTIDAD_DE_PARTICULAS-2, 2):
      plt.plot(matriz_particulas_azules[a][b], matriz_particulas_azules[a][b+1], 'b.') #plotea todos los puntos azules
    for c in range (0,2*CANTIDAD_DE_PARTICULAS-2, 2):
      plt.plot(matriz_particulas_rojas[a][c], matriz_particulas_rojas[a][c+1], 'r.') #plotea todos los puntos rojos
    plt.plot(x_membrana, membrana, 'k-')
    plt.draw()
    plt.pause(0.001)
    plt.clf()

def crear_matriz(limite_x_inferior, limite_x_superior): #N cantidad de particulas
  A = np.zeros((CANTIDAD_DE_MOVIMIENTOS, 2*CANTIDAD_DE_PARTICULAS))

  for z in range (0, 2*CANTIDAD_DE_PARTICULAS - 1, 2): #z numero de columna, este for asigna el valor inicial de cada particula y los siguientes 
    A[0][z] = rnd.randint(limite_x_inferior, limite_x_superior) #elige al azar la posicion incial en x dentro de la mitad correspondiente
    A[0][z+1] = rnd.randint(0, ALTO_DE_LA_CAJA) #elige al azar la posicion inicial en y dentro del alto entero de la caja
    
    r = np.random.random(CANTIDAD_DE_MOVIMIENTOS) #vector de randoms para decidir hacia donde se va a mover en cada instante
    
    for i in range (1, CANTIDAD_DE_MOVIMIENTOS): #simula todos los movimientos de una particula desde el segundo instante de tiempo
        #Para correr el punto b) es necesario agregar la llamada a la funcion puede_moverse_arriba 
        if (r[i] <= 0.25 and A[i-1][z+1] < ALTO_DE_LA_CAJA and puede_moverse_arriba(A, i, z)): #movimiento en y, se fija si la posicion anterior es inferior al borde superior de la caja
          A[i][z+1] = A[i-1][z+1] + 1 #que se mueva hacia arriba
          A[i][z] = A[i-1][z] #deja la posicion en x[i] igual que en i-1
        elif (r[i] > 0.25 and r[i] <= 0.5 and A[i-1][z+1] > 0): #movimiento en y, se fija si la posicion anterior es superior al borde inferior de la caja
          A[i][z+1] = A[i-1][z+1] - 1 #que se mueva hacia abajo
          A[i][z] = A[i-1][z]
        #Para correr el punto b) es necesario agregar la llamada a la funcion puede_moverse_izq         
        elif (r[i] > 0.5 and r[i] <= 0.75 and A[i-1][z] > 0 and puede_moverse_izq(A, i, z)):
          A[i][z] = A[i-1][z] - 1 #que se mueva hacia la izquierda
          A[i][z+1] = A[i-1][z+1]
        #Para correr el punto b) es necesario agregar la llamada a la funcion puede_moverse_der        
        elif (r[i] > 0.75 and A[i-1][z] < ANCHO_DE_LA_CAJA and puede_moverse_der(A, i, z)):
          A[i][z] = A[i-1][z] + 1 #que se mueva hacia la derecha
          A[i][z+1] = A[i-1][z+1]
        else: #si no entró a ninguno de los anteriores es porque estaba en el borde la caja entonces se queda donde esta
          A[i][z] = A[i-1][z]
          A[i][z+1] = A[i-1][z+1]
  return A
  
def grafica_densidades(matriz_particulas_azules, matriz_particulas_rojas):

  d_azules_izq = calcular_densidad(matriz_particulas_azules, 0, 49)
  d_azules_der = calcular_densidad(matriz_particulas_azules, 50, 100)
  d_rojas_izq = calcular_densidad(matriz_particulas_rojas, 0, 49)
  d_rojas_der = calcular_densidad(matriz_particulas_rojas, 50, 100)

  tiempo = np.arange(CANTIDAD_DE_MOVIMIENTOS)

  plt.subplot(221).set_title("Azules izquierda")
  plt.plot(tiempo, d_azules_izq/CANTIDAD_DE_PARTICULAS, '.', ms=2) #cantidad de azules a la izq
  plt.subplot(222).set_title("Azules derecha")
  plt.plot(tiempo, d_azules_der/CANTIDAD_DE_PARTICULAS, '.', ms=2) #cantidad de azules a la der
  plt.subplot(223).set_title("Rojas izquierda")
  plt.plot(tiempo, d_rojas_izq/CANTIDAD_DE_PARTICULAS, '.', ms=2) #cantidad de rojos a la izq
  plt.subplot(224).set_title("Rojas derecha")
  plt.plot(tiempo, d_rojas_der/CANTIDAD_DE_PARTICULAS, '.', ms=2) #cantidad de rojos a la der
  plt.show()

def calcular_densidad(A, limite_x_inferior, limite_x_superior):
  #se fija en cada instante cuantas particulas del color elegido en la mitad elegida hay. 
  #Va guardando cada resultado en una entrada de un vector

  contador = np.zeros(CANTIDAD_DE_MOVIMIENTOS)
  for a in range (0, CANTIDAD_DE_MOVIMIENTOS): 
      for b in range (0, (2*CANTIDAD_DE_PARTICULAS - 1), 2):
        if (A[a][b] >= limite_x_inferior and A[a][b] <= limite_x_superior):
          contador[a] = contador[a]+1
  
  return contador

def puede_moverse_izq(A, i, z): 
  if (A[i-1][z+1] >= ALTO_DE_LA_CAJA / 2 and A[i-1][z] < 50): #area naranja
    return True 
  elif (A[i-1][z+1] >= ALTO_DE_LA_CAJA / 2 and A[i-1][z] > 51): #area azul
    return True
  elif(A[i-1][z+1] <= ALTO_DE_LA_CAJA / 2): #area violeta o verde
    return True 
  return False

def puede_moverse_der(A, i, z):
  if (A[i-1][z+1] >= ALTO_DE_LA_CAJA / 2 and A[i-1][z] < 49): #area naranja
    return True 
  elif (A[i-1][z+1] >= ALTO_DE_LA_CAJA / 2 and A[i-1][z] > 50): #area azul
    return True
  elif(A[i-1][z+1] <= ALTO_DE_LA_CAJA / 2): #area violeta o verde
    return True 
  return False

def puede_moverse_arriba(A, i, z):
  if (A[i-1][z] == 50 and A[i-1][z+1] == 99):
    return False
  return True

ej9()