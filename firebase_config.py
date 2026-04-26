import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv

load_dotenv()

# Firebase se connection
cred = credentials.Certificate('serviceAccountKey.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv('FIREBASE_URL')
})

# Yeh function database ka reference deta hai
def get_db():
    return db