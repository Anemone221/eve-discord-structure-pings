# EVE SSO OAuth2 Authorization Flow for Discord Bot
import os
import urllib.parse
import requests
from requests.auth import HTTPBasicAuth

# --- Step 1: Build the EVE authorization URL ---
def build_auth_url(state: str) -> str:
    base_url = "https://login.eveonline.com/v2/oauth/authorize/"
    params = {
        "response_type": "code",
        "redirect_uri": os.getenv("ESI_CALLBACK_URL"),
        "client_id": os.getenv("ESI_CLIENT_ID"),
        "scope": "esi-characters.read_corporation_roles.v1 esi-universe.read_structures.v1",
        "state": state
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"

# --- Step 2: Exchange code for tokens ---
def get_tokens_from_code(code: str) -> dict:
    response = requests.post(
        "https://login.eveonline.com/v2/oauth/token",
        auth=HTTPBasicAuth(
            os.getenv("ESI_CLIENT_ID"),
            os.getenv("ESI_SECRET_KEY")
        ),
        data={
            "grant_type": "authorization_code",
            "code": code,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    response.raise_for_status()
    return response.json()

# --- Step 3: Verify the access token and get character info ---
def get_character_info(access_token: str) -> dict:
    response = requests.get(
        "https://login.eveonline.com/oauth/verify",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    response.raise_for_status()
    return response.json()

# --- Step 4: Store tokens and character info in DB ---
# This will depend on your model, assuming function exists:
# store_esi_token(character_id, character_name, access_token, refresh_token, scopes, token_expiry)

# You'd call something like this after verification:
# info = get_character_info(access_token)
# store_esi_token(info['CharacterID'], info['CharacterName'], access_token, refresh_token, info['Scopes'], info['ExpiresOn'])
