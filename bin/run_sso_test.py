# scripts/run_sso_test.py
import os
from dotenv import load_dotenv
from sso.sso_connect import build_auth_url

if __name__ == "__main__":
    load_dotenv()
    state = "localteststate123"
    url = build_auth_url(state)
    print("🔗 Open this URL in your browser to authenticate via EVE SSO:")
    print(url)
