# firebase.py
import os
from django.conf import settings
import firebase_admin
from firebase_admin import credentials

# We check if it's already running so Django doesn't crash when it auto-reloads
if not firebase_admin._apps:
    # This automatically finds the exact path to your project root
    key_path = os.path.join(settings.BASE_DIR, 'serviceAccountKey.json')
    
    if os.path.exists(key_path):
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase initialized from separate file!")
    else:
        print(f"❌ Could not find the JSON key at: {key_path}")