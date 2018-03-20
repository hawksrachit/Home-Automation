import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
cred = credentials.Certificate('admin.json')
default_app = firebase_admin.initialize_app(
    cred, {'databaseURL': 'https://rajasthanhack-4c007.firebaseio.com/'})
database_ref = db.reference('/IOTdata')

url = "http://192.168.43.82/lightstatus"

response = requests.get(url)
str1=response.text.split(";")


previousResponse = []

for i in range(len(str1)):
    previousResponse.append("0")

while True:
    
    str2= []
    for i in range(len (str1)):
        str2.append(str1[i].split(","))
        if str1[i] != previousResponse[i]:
            ts = time.time()
            database_ref.push(
                {
                    "roomid": str2[i][1],
                    "applianceid": str2[i][0],
                    "status": str2[i][2],
                    "timestamp_UNIX": ts
                })
            print("status changed")
        previousResponse[i] = str1[i]
    time.sleep(1);
    print(response.text)
    response = requests.get(url)
    str1=response.text.split(";")
    