import random
from matplotlib import pyplot as plt

def request_was_received():
    rand = random.random()
    return rand <= 0.025


def request_will_be_proccesed():
    rand = random.random()
    return rand <= 0.0333

def register_state(state,quantity_by_state):
    if state in quantity_by_state:
        quantity_by_state[state] = quantity_by_state[state] + 1
    else:
        quantity_by_state[state] = 1


def grafic_histogram(histogram,title):
    keys = list(histogram.keys())
    keys.sort()
    print("keys:"+str(keys))
    values = list(map(lambda key: histogram[key],keys))
    print("values:"+str(values))
    plt.bar([str(i) for i in keys], values, color='g')
    plt.suptitle(title, fontsize=18)
    plt.show()

quantity_in_queue = 0
quantity_in_server = 0
quantity_in_server_in_t = []
quantity_in_queue_in_t = []
quantity_by_state_in_server = {}
quantity_by_state_in_queue = {}

quantity_without_processing = 0

for t in range(1000000):

    server_is_empty = True
    #print("lo que hay en el server {}".format(quantity_in_server))
    #print("lo que hay en el queue {}".format(quantity_in_queue))
    if request_was_received():
        #print("se recibio {}".format(t))
        quantity_in_queue = quantity_in_queue + 1
    
    will_be_processed = request_will_be_proccesed()
    quantity_in_queue_before = quantity_in_queue
    #print("will_be_processed {}".format(will_be_processed))
    #print("quantity in queue {}".format(quantity_in_queue))
    if (will_be_processed or server_is_empty) and quantity_in_queue_before > 0:
        #print("se saco {}".format(t))
        quantity_in_queue = quantity_in_queue - 1
        server_is_empty = False

    elif not server_is_empty and will_be_processed and quantity_in_queue_before == 0:
        server_is_empty = True
    
    if server_is_empty:
        quantity_without_processing += 1
    
    quantity_in_server = quantity_in_queue + 1 if server_is_empty else quantity_in_queue
    quantity_in_server_in_t.append(quantity_in_server)
    register_state(quantity_in_server,quantity_by_state_in_server)
    register_state(quantity_in_queue,quantity_by_state_in_queue)

print("cantidad de veces sin procesar {}".format(quantity_without_processing))
#print("vector t en el server {}".format(quantity_in_server_in_t))


grafic_histogram(quantity_by_state_in_server,"Solicitudes en el servidor")
grafic_histogram(quantity_by_state_in_queue,"Solicitudes en la cola")

plt.plot(quantity_in_server_in_t)
plt.suptitle('Pedidos en el servidor', fontsize=20)
plt.show()


