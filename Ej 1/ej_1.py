import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import statistics as stats

MEDIA_GENERAL = 4
MEDIA_P1_U1 = 0.7 #60% con esta media
MEDIA_P1_U2 = 1 #40% con esta media
MEDIA_P2 = 0.8
CANT_SOLICITUDES = 100000

def ej1():
    z_general = np.random.exponential(MEDIA_GENERAL, CANT_SOLICITUDES) #simula 100000 llegadas

    z_general = z_general.tolist() #convierte el array de np en lista

    t_procesamiento_u1, t_procesamiento_u2, t_arribo_u1, t_arribo_u2 = tpos_arribo_y_procesamiento(z_general)

    t_procesamiento_p2 = []
    t_procesamiento_p2 = np.random.exponential(MEDIA_P2, CANT_SOLICITUDES) #genera 100000 tpos de procesamiento con media = 0.8
    t_procesamiento_p2 = t_procesamiento_p2.tolist()

    t_atencion_u1, t_espera_u1, sin_espera_u1 = tpos_atencion_y_espera(t_arribo_u1, t_procesamiento_u1)
    t_atencion_u2, t_espera_u2, sin_espera_u2 = tpos_atencion_y_espera(t_arribo_u2, t_procesamiento_u2)

    t_arribo_p2 = []
    t_arribo_p2.append(0) #inicializo en 0

    for i in range (0, CANT_SOLICITUDES): 
        t_arribo_p2.append(t_arribo_p2[-1] + z_general[i]) #guarda en una nueva entrada el tiempo acumulado + el nuevo tiempo de llegada

    t_atencion_p2, t_espera_p2, sin_espera_p2 = tpos_atencion_y_espera(t_arribo_p2, t_procesamiento_p2)

    
    t_total_u1 = np.add(t_espera_u1, t_procesamiento_u1) #tiempo de espera + tiempo de procesamiento
    t_total_u2 = np.add(t_espera_u2, t_procesamiento_u2)
    t_total_p2 = np.add(t_espera_p2, t_procesamiento_p2)

    t_total_u1 = t_total_u1.tolist()
    t_total_u2 = t_total_u2.tolist()
    t_total_p2 = t_total_p2.tolist()

    t_total_p1 = t_total_u1 + t_total_u2 #concatena las dos unidades de la P1

    t_espera_p1 = t_espera_u1 + t_espera_u2


    '''muestras_t_total = np.random.exponential(stats.mean(t_total_p2), len(t_total_p2)) #genera muestras de una exponencial con la media sacada de los tiempos generados

    plt.figure(1)
    plt.hist(t_espera_u1, bins = "sturges", align = "left")
    plt.figure(2)
    plt.hist(t_total_p2, bins = "sturges", align = "left")
    plt.figure(3)
    plt.hist(t_atencion_u1, bins = "sturges", align = "left")
    plt.figure(4)
    plt.hist(muestras_t_total, bins = "sturges", align = "left") #acá me fijo cómo sería una dist exponencial con la media sacada del tiempo de atención total
    plt.show()

    plt.subplot(221).set_title("Tiempo espera u1")
    plt.hist(t_espera_u1, bins = "sturges", align = "left") #cantidad de azules a la izq
    plt.subplot(222).set_title("Tiempo espera u2")
    plt.hist(t_espera_u2, bins = "sturges", align = "left") #cantidad de azules a la der
    plt.subplot(223).set_title("Tiempo espera p1")
    plt.hist(t_espera_p1, bins = "sturges", align = "left") #cantidad de rojos a la izq
    plt.subplot(224).set_title("tiempo espera p2")
    plt.hist(t_espera_p2, bins = "sturges", align = "left") #cantidad de rojos a la der
    plt.show()
    '''
        
    print("\nMedia de tiempo de espera P1 en horas: ", stats.mean(t_espera_p1))
    print("Media de tiempo de espera P2 en horas: ", stats.mean(t_espera_p2))
    
    print("\nFraccion solicitudes P1 con espera 0: ", (sin_espera_u1+sin_espera_u2) / CANT_SOLICITUDES)
    print("Fraccion solicitudes P2 con espera 0: ", sin_espera_p2 / CANT_SOLICITUDES)

    print("\nMedia de tiempo de atención P1 en horas: ", stats.mean(t_total_p1))
    print("Media de tiempo de atención P2 en horas: ", stats.mean(t_total_p2))

    print("\nEl tiempo medio que le llevó a P1 procesar cada solicitud representa un {0:.2f}% del tiempo medio que le llevó a P2".format(stats.mean(t_total_p1)*100/stats.mean(t_total_p2)))

    t_finalizacion_p1 = max(t_atencion_u1[-1]+t_procesamiento_u1[-1], t_atencion_u2[-1])+t_procesamiento_u2[-1]
    t_finalizacion_p2 = t_atencion_p2[-1]+t_procesamiento_p2[-1]

    print("\nEl tiempo que le llevó al P1 procesar todas fue: ", t_finalizacion_p1 ) #muestra el tiempo de la unidad que temrino mas tarde
    print("El tiempo que le llevó al P2 procesar todas fue: ", t_finalizacion_p2)

    print("\nEl tiempo que le llevó a P1 procesar las 100.000 muestras representa un {0:.2f}% del tiempo que le llevó a P2".format(t_finalizacion_p1*100/t_finalizacion_p2))

    print(" ")
    

def tpos_arribo_y_procesamiento(z_general):

    elige_unidad = np.random.random(CANT_SOLICITUDES)

    unidad1 = [] #guarda los z generales distribuidos por unidad
    unidad2 = []

    t_arribo_u1 = [] #vector de tiempo acumulado, o sea en que t hay una llegada
    t_arribo_u2 = []
    
    t_arribo_u1.append(0)
    t_arribo_u2.append(0)

    contador_tiempo_u1 = 0
    contador_tiempo_u2 = 0

    t_procesamiento_u1 = []
    t_procesamiento_u2 = []

    for i in range (0,CANT_SOLICITUDES): #separa las llegadas en dos vectores de acuerdo a la unidad que lo procesara
        
        if elige_unidad[i] <= 0.6:
            unidad1.append(z_general[i])
            t_arribo_u1.append(t_arribo_u1[contador_tiempo_u1] + z_general[i]) #guarda en una nueva entrada el tiempo acumulado + el nuevo tiempo de espera
            contador_tiempo_u1 = contador_tiempo_u1+1
            t_procesamiento_u1.append(np.random.exponential(MEDIA_P1_U1)) #genera el tiempo de procesamiento de cada solicitud
        else:
            unidad2.append(z_general[i])
            t_arribo_u2.append(t_arribo_u2[contador_tiempo_u2] + z_general[i])
            contador_tiempo_u2 = contador_tiempo_u2+1
            t_procesamiento_u2.append(np.random.exponential(MEDIA_P1_U2))


    return t_procesamiento_u1, t_procesamiento_u2, t_arribo_u1, t_arribo_u2

def tpos_atencion_y_espera(t_arribo, t_procesamiento):
    t_atencion = []
    t_espera = []

    t_espera.append(0)

    sin_espera = 0

    t_atencion.append(t_arribo[0]) 
    t_atencion.append(t_arribo[1]) #a la primera solicitud se la atiende en el instante que llega

    for i in range (1, len(t_arribo)-1):
        a = t_atencion[i] + t_procesamiento[i-1]
        if a > t_arribo[i+1]:
            t_atencion.append(a)
            t_espera.append(t_atencion[-1] - t_arribo[i+1])
        else:
            t_atencion.append(t_arribo[i+1])
            t_espera.append(0)
            sin_espera = sin_espera+1
    
    return t_atencion, t_espera, sin_espera


ej1()