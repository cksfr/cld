# ------------------ DEPENDENCIES ------------------
# pip install Flask Authlib

from flask import Flask, session, redirect
from authlib.integrations.flask_client import OAuth
from authlib.integrations.base_client.errors import MismatchingStateError

# ------------------ FLASK SETUP ------------------
app = Flask(__name__)
app.secret_key = "super_random_secret"

# Fix session cookies for local dev to prevent CSRF state error
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # True if using HTTPS

# ------------------ AUTH0 CONFIG ------------------
CLIENT_ID = "KkcYiW7G0eixl5ydUxZeI63gFphykUNt"
CLIENT_SECRET = "AYjXIn0k78AA6pJqjkVkb1XYyMyUJRaH6SrJE4OmWQrfPdqk6HN10HkE4ZtE0MtP"
DOMAIN = "dev-to8wba1eer5am20j.us.auth0.com"
CALLBACK_URL = "http://localhost:5000/callback"

oauth = OAuth(app)
auth0 = oauth.register(
    "auth0",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f"https://{DOMAIN}/.well-known/openid-configuration"
)

# ------------------ ROUTES ------------------
@app.route("/")
def home():
    user = session.get("user")
    if user:
        return f"Welcome, {user['name']}! <a href='/logout'>Logout</a>"
    return "<a href='/login'>Login with Auth0</a>"

@app.route("/login")
def login():
    # Redirect user to Auth0 login page
    return auth0.authorize_redirect(redirect_uri=CALLBACK_URL)

@app.route("/callback")
def callback():
    try:
        # Get user info from Auth0 after login
        token = auth0.authorize_access_token()
        session["user"] = token["userinfo"]
        return redirect("/")
    except MismatchingStateError:
        # If CSRF mismatch happens, clear session and redirect to /login
        session.clear()
        return redirect("/login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ------------------ RUN APP ------------------
if __name__ == "__main__":
    app.run(debug=True)
