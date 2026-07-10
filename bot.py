TELEGRAM_TOKEN = "8840027780:AAFel6SFEpNIpgK4gN6FrXv_plbtMNegSxQ"
CHAT_ID = "5985490720"
# ===================================

def send_alert(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})

print("Bot starting...")

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
                    ca = pair["baseToken"]["address"]
                    
                    if mc < 500000 and age_min < 120 and ca not in seen:
                        seen.add(ca)
                        name = pair["baseToken"].get("symbol", "Unknown")
                        link = pair.get("url", "")
                        msg = f"🚀 New Robinhood Chain coin!\n\n{name}\n\nCA: <code>{ca}</code>\n\nMC: ${mc:,.0f}\n\nLink: {link}\n\nCopy the CA above!"
                        send_alert(msg)
                        print("Alert sent:", ca)
    except:
        pass
    time.sleep(15)
