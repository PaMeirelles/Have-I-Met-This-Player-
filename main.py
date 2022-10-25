import time
from search import *

player1 = "PyMeirelles"
player2 = "pefofo123"
region = "BR1"
m = "BR1_2604297919"
print("Simple search")
start = time.perf_counter()
# x = simple_search(player1, player2, region)
x = get_player_result(m)
stop = time.perf_counter()
# print(len(x))
print(x)
print(str(round(stop-start, 2)) + "s")