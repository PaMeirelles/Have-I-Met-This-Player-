import time
from search import *

player1 = "PyMeirelles"
player2 = "zeru0itu"
region = "BR1"

start = time.perf_counter()

puuid1 = get_puuid(player1, region)
puuid2 = get_puuid(player2, region)
x = get_duo_wr(puuid1, puuid2, ranked_only=True)

stop = time.perf_counter()
print(x)
print(str(round(stop-start, 2)) + "s")