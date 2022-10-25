import requests
import time
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",

  
    "X-Riot-Token": "RGAPI-37dba1a0-380b-472f-b71a-2f447814fcab"
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

def get_player_result(match_id):
  page = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}", headers=headers)
  if(page.status_code != 200):
    print(page.status_code)
    exit(page.status_code)
  participants = page.json()["info"]["participants"]
  player_result = {}
  for p in participants:
    player_result[p["puuid"]] = p["win"]
  return player_result

def get_duo_result(player_result, player_1, player_2):
  if player_result[player_1] != player_result[player_2]:
    return "different teams"
  if player_result[player_1]:
    return "win"
  return "loss"
