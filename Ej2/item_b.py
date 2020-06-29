import random
from matplotlib import pyplot as plt

def request_was_received():
    rand = random.random()
    return rand <= 0.025


def request_was_proccesed():
    rand = random.random()
    return rand <= 0.0333

def register_state(state,quantity_by_state):
    if state in quantity_by_state:
        quantity_by_state[state] = quantity_by_state[state] + 1
    else:
        quantity_by_state[state] = 1


quantity_in_queue = 0

quantity_in_queue_in_t = []

quantity_by_state = {}
quantity_of_processing = 0

for t in range(100000):
    if request_was_received():
        quantity_in_queue = quantity_in_queue + 1
    if request_was_proccesed()  and quantity_in_queue > 0:
        quantity_in_queue = quantity_in_queue - 1
        quantity_of_processing = quantity_of_processing + 1
    quantity_in_queue_in_t.append(quantity_in_queue)
    register_state(quantity_in_queue,quantity_by_state)



keys = list(quantity_by_state.keys())
keys.sort()
print("keys:"+str(keys))
values = list(map(lambda key: quantity_by_state[key],keys))
print("values:"+str(values))
print("quantity of processing",quantity_of_processing)

plt.bar([str(i) for i in keys], values, color='g')
plt.show()

plt.plot(quantity_in_queue_in_t)
plt.show()


