# tests/test_sso.py
import os
from sso.sso_connect import build_auth_url

def test_build_auth_url_contains_state():
    state = "pyteststatetest123"
    url = build_auth_url(state)
    assert "state=pyteststatetest123" in url
    assert "https://login.eveonline.com" in url
