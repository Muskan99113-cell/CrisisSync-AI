import firebase_admin
from firebase_admin import credentials, db
import os
import json
from dotenv import load_dotenv

load_dotenv()

if os.getenv('GOOGLE_CREDENTIALS'):
    cred_dict = json.loads(os.getenv('GOOGLE_CREDENTIALS'))
    cred = credentials.Certificate(cred_dict)
else:
    cred = credentials.Certificate('serviceAccountKey.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv('FIREBASE_URL')
})

def get_db():
    return db