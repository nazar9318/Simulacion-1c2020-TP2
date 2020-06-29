import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import statistics as stats

media_general=4*60*60
media_p1_u1=0.7*60*60
media_p1_u2=1*60*60
media_p2=0.8*60*60
cant_solicitudes=100000

def ej1():
    z_general=np.random.exponential(media_general, cant_solicitudes) #simula 100000 llegadas
    elige_unidad=np.random.random(cant_solicitudes) #vector de numeros random entre 0 y 1 para elegir unidad
    unidad1=[] #guarda los z generales distribuidos por unidad
    unidad2=[]

    t_arribo_u1=[] #vector de tiempo acumulado, o sea en que t hay una llegada
    t_arribo_u2=[]
    
    t_arribo_u1.append(0)
    t_arribo_u2.append(0)

    contador_tiempo_u1=0
    contador_tiempo_u2=0

    t_procesamiento_u1=[]
    t_procesamiento_u2=[]

    #t_procesamiento_u1.append(0)
    #t_procesamiento_u2.append(0)


    for i in range (0,cant_solicitudes): #separa las llegadas en dos vectores de acuerdo a la unidad que lo procesara
        
        if elige_unidad[i]<=0.6:
            unidad1.append(z_general[i])
            t_arribo_u1.append(t_arribo_u1[contador_tiempo_u1]+z_general[i]) #guarda en una nueva entrada el tiempo acumulado + el nuevo tiempo de espera
            contador_tiempo_u1=contador_tiempo_u1+1
            t_procesamiento_u1.append(np.random.exponential(media_p1_u1)) #genera el tiempo de procesamiento de cada solicitud
        else:
            unidad2.append(z_general[i])
            t_arribo_u2.append(t_arribo_u2[contador_tiempo_u2]+z_general[i])
            contador_tiempo_u2=contador_tiempo_u2+1
            t_procesamiento_u2.append(np.random.exponential(media_p1_u2))

    t_procesamiento_u1.append(np.random.exponential(media_p1_u1)) 
    t_procesamiento_u2.append(np.random.exponential(media_p1_u2)) 
    t_atencion_u1=[]
    t_atencion_u2=[]
    t_espera_u1=[]
    t_espera_u2=[]

    #t_atencion_u1.append(0)
    #t_atencion_u2.append(0)

    t_espera_u1.append(0)
    t_espera_u2.append(0)

    sin_espera=0

    t_atencion_u1.append(t_arribo_u1[0]) #a0=t0


    for i in range (1, len(t_arribo_u1)):
        a=t_atencion_u1[i-1]+t_procesamiento_u1[i-1]
        if a>t_arribo_u1[i]:
            t_atencion_u1.append(a)
            t_espera_u1.append(t_atencion_u1[-1]-t_arribo_u1[i])
        else:
            t_atencion_u1.append(t_arribo_u1[i])
            t_espera_u1.append(0)
            sin_espera=sin_espera+1

    t_total=np.add(t_espera_u1,t_procesamiento_u1)

    muestras_t_total=np.random.exponential(stats.mean(t_total), len(t_total)) #genera muestras de una exponencial con la media sacada de los tiempos generados

    plt.figure(1)
    plt.hist(t_espera_u1, bins="sturges", align="left")
    
    plt.figure(2)
    plt.hist(t_total, bins="sturges", align="left")

    plt.figure(3)
    plt.hist(t_atencion_u1, bins="sturges", align="left")
    
    plt.figure(4)
    plt.hist(muestras_t_total, bins="sturges", align="left")

    plt.show()

    print(stats.mean(t_espera_u1))
    print(stats.mean(t_total))
    print(stats.mean(t_procesamiento_u1))
    print(sin_espera/len(unidad1))
    
ej1()

