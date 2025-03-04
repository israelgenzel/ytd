import re
import requests
import os

import urllib

# כתובת השרת שלך ב-Railway (עדכן בהתאם ל-URL שקיבלת)
RAILWAY_SERVER_URL = "https://ytd-production.up.railway.app/search"
LOCAL_SERVER_URL = "http://127.0.0.1:8080/search"

def searchyoutube(query):
    """שולח בקשת חיפוש לשרת ומחזיר את התוצאות"""
    params = {"query": query}
    response = requests.get(LOCAL_SERVER_URL, params=params)

    

    if response.status_code == 200:
        results = response.json()
        if not results:
            print("❌ לא נמצאו תוצאות")
            return
        for i, result in enumerate(results, start=1):
            print(f"{i}. {result['title']} ({result['duration']}) - {result['url']}")
       
        print("search done")
    else:
        print(f"❌ שגיאה: {response.text}")

# דוגמה לשימוש
query = "שלמה ארצי"
searchyoutube(query)
