# sso_callback_server.py
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from sso.sso_connect import get_tokens_from_code, get_character_info

load_dotenv()
app = FastAPI()

@app.get("/callback", response_class=HTMLResponse)
async def callback(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code:
        return HTMLResponse("<h2>Error: No code provided.</h2>", status_code=400)

    try:
        tokens = get_tokens_from_code(code)
        character = get_character_info(tokens['access_token'])

        return f"""
        <h2>SSO Login Successful!</h2>
        <p><strong>Character:</strong> {character['CharacterName']} ({character['CharacterID']})</p>
        <p><strong>Access Token:</strong> {tokens['access_token'][:40]}...</p>
        <p><strong>Refresh Token:</strong> {tokens['refresh_token'][:40]}...</p>
        """
    except Exception as e:
        return HTMLResponse(f"<h2>Failed:</h2><p>{str(e)}</p>", status_code=500)
