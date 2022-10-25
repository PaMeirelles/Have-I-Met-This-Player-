import requests
import time
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",

  
    "X-Riot-Token": "RGAPI-37dba1a0-380b-472f-b71a-2f447814fcab"
}
rate = 0.6

def get_puuid(name, region):
  page = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}", headers=headers).json()
  time.sleep(rate)

  return page["puuid"]

def get_matches(puuid, ranked_only=False):
  matches = []
  i = 0
  while(True):
    if ranked_only:
      page = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?&type=ranked&start={i}&count={100}", headers=headers)
    else:
      page = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?&start={i}&count={100}", headers=headers)
    time.sleep(rate)
    
    jp = page.json()
    if len(jp) == 0:
      break
    matches += jp
    i += 100
  return matches

def simple_search(puuid1, puuid2, ranked_only=False):
  matches1 = get_matches(puuid1, ranked_only)
  matches2 = get_matches(puuid2, ranked_only)

  return set(matches1) & set(matches2)

def get_player_result(match_id):
  page = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}", headers=headers)
  time.sleep(rate)

  if(page.status_code != 200):
    print(page.status_code)
    exit(page.status_code)
  participants = page.json()["info"]["participants"]
  player_result = {}
  for p in participants:
    player_result[p["puuid"]] = p["win"]
  return player_result

def get_duo_result(player_result, puuid1, puuid2):
  if player_result[puuid1] != player_result[puuid2]:
    return "different teams"
  if player_result[puuid1]:
    return "win"
  return "loss"

def get_duo_wr(puuid1, puuid2, ranked_only=False):
  matches = simple_search(puuid1, puuid2, ranked_only)
  duo_result = {"win": 0, "loss": 0, "different teams": 0, "total": 0}

  for n, m in enumerate(matches):
    if n % 10 == 0:
      print(n)
    pr = get_player_result(m)
    dr = get_duo_result(pr, puuid1, puuid2)
    duo_result[dr] += 1
    duo_result["total"] += 1
  return duo_result