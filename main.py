import requests
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
