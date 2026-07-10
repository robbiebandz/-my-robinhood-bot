import requests
import time

# === CHANGE THESE TWO LINES ===
TELEGRAM_TOKEN = "8840027780:AAFel6SFEpNIpgK4gN6FrXv_plbtMNegSxQ"
CHAT_ID = "5985490720"
# ===================================

def send_alert(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})

print("Bot starting... (Looking for 10k-300k MC coins)")


seen = set()

while True:
    try:
        r = requests.get("https://api.dexscreener.com/latest/dex/search?q=robinhood", timeout=10)
        if r.status_code == 200:
            data = r.json()
            for pair in data.get("pairs", []):
                if pair.get("chainId") == "robinhood":
                    mc = pair.get("marketCap") or 0
                    created = pair.get("pairCreatedAt") or 0
                    age_min = (time.time() * 1000 - created) / 1000 / 60
                    
                    liq = pair.get("liquidity", {}).get("usd", 0) or 0
                    ca = pair["baseToken"]["address"]
                    
                    has_socials = False
                    if pair.get("info"):
                        if pair["info"].get("websites") or pair["info"].get("socials"):
                            has_socials = True
                    
                    if (8000 < mc < 300000 and 
                        liq > 5000 and 
                        2 < age_min < 240 and 
                        has_socials and 
                        ca not in seen):
                        
                        seen.add(ca)
                        name = pair["baseToken"].get("symbol", "Unknown")
                        link = pair.get("url", "")
                        
                        msg = f"🚀 Early Robinhood Chain coin!\n\n{name}\n\nCA: {ca}\n\nMC: ${mc:,.0f}\nLiq: ${liq:,.0f}\nAge: {int(age_min)} min\n\nLink: {link}\n\nCopy the CA above!"
                        send_alert(msg)
                        print("Alert sent for:", ca, "MC:", mc)
    except:
        pass
    
    time.sleep(15)
