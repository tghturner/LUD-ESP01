import json

def load_settings():
    try:
        with open('settings.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print("Error loading settings:", str(e))
        return None

settings = load_settings()