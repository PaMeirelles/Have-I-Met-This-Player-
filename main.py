import requests
import time
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",

  
    "X-Riot-Token": "RGAPI-024957a5-1c00-463b-bf1e-7d15e10ee271"
}

def get_puuid(name, region):
  page = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}", headers=headers).json()
  return page["puuid"]

def get_matches(puuid):
  matches = []
  i = 0
  while(True):
    page = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?&start={i}&count={100}", headers=headers)
    
    jp = page.json()
    if len(jp) == 0:
      break
    matches += jp
    i += 100
  return matches

def simple_search(name1, name2, region):
  puuid1 = get_puuid(name1, region)
  puuid2 = get_puuid(name2, region)
  
  matches1 = get_matches(puuid1)
  matches2 = get_matches(puuid2)

  return set(matches1) & set(matches2)

def get_players(match_id):
  match = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}", headers=headers)
  try:
    p = match.json()["metadata"]["participants"]
  except KeyError:
    print(match)
  return p

  
player1 = "PyMeirelles"
player2 = "pllucazz"
region = "BR1"


print("Simple search")
start = time.perf_counter()
x = simple_search(player1, player2, region)
stop = time.perf_counter()
print(len(x))
print(str(round(stop-start, 2)) + "s")
