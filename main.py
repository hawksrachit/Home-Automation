from flask import Flask,redirect,render_template,jsonify,request
from PowerUsage import PowerUsage
import serial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
import aiml
import sys
import os
from nltk.stem import WordNetLemmatizer
import nltk
import json


cred = credentials.Certificate('admin.json')
default_app = firebase_admin.initialize_app(cred,{'databaseURL' : 'https://rajasthanhack-4c007.firebaseio.com/'})
database_ref = db.reference('/IOTdata')
## ----------BOT-------------##

os.chdir('E:\IOT-power-master (3)\IOT-power-master')
mybot = aiml.Kernel()
#Learn startup.xml
mybot.learn('startup.xml')
#Calling load aiml b for loading all AIML files
mybot.respond('load aiml b')
stopwords = set(w.rstrip() for w in open('E:\IOT-power-master (3)\IOT-power-master\stopwords.txt'))
def my_tokenizer(s):
    s=s.lower()
    wordnet_lemmatizer = WordNetLemmatizer()
    tokens = nltk.tokenize.word_tokenize(s)
    tokens=[t for t in tokens if len(t) >1]
    tokens=[wordnet_lemmatizer.lemmatize(t) for t in tokens]
    #tokens=[t for t in tokens if t not in stopwords]
    return tokens

prediction_request_keyword = ['predict','future','power','prediction']
past_usage_request = ['past','history','power']
turn_on = ['start', 'on']
turn_off = ['off','shutdown']
appliances = ['lightBulb','light','bulb','fan','computer','exhaust']
option = ['on','off','pred','past']

def checker(user_in):

    fut = 0
    past = 0
    on = 0
    off = 0
    list = my_tokenizer(user_in)

    for word in list:
        if word in prediction_request_keyword:
             fut = fut + 1

    for word in list:
        if word in past_usage_request:
             past = past + 1

    for word in list:
        if word in turn_on:
             on = on + 1

    for word in list:
        if word in turn_off:
             off = off + 1

    if (fut == 0 and past ==0 and on == 0 and off ==0) :
        return mybot.respond(user_in)
    elif (fut > past and fut > on and fut > off):
        return option[2]
    elif (past > fut and past > on and past > off) :
        return option[3]
    elif (on > past and on > fut and on > off):
        return option[0],getting_appliance(list)
    else:
        return option[1],getting_appliance(list)

def getting_appliance(list):
    for word in list:
        if word in appliances:
             return word

## ----------BOTEND-------------##


app = Flask(__name__)

@app.route('/')
def index():
    return "welcome to Power Usage api go to /api for refrence"

sample_api_output =  [
    {
        "roomid":1,
        "applianceid":'123',
        "status":"1",
        "timestamp_UNIX":""
    },
       {
        "roomid":2,
        "noOfPeople":PowerUsage().getData()
    }
]
"""@app.route('/api',methods=['GET'])
def api():
    return jsonify({'data':sample_api_output})
"""

arg1,arg2,arg3="","",""
@app.route('/lightturnedon')
def lightturnedon():
    ts = time.time()
    arg1= request.args['arg1']
    arg2= request.args['arg2']
    arg3= request.args['arg3']
    database_ref.push(
        {
        "roomid":arg1,
        "applianceid":arg2,
        "status":arg3,
        "timestamp_UNIX":ts
    }
    )
    args = arg2+","+arg1+","+arg3
    with open('file.txt', 'w') as fh:
        fh.write(args)
    return redirect('http://localhost:5000/esp')

@app.route('/lightturnedoff')
def lightturnedoff():
    ts = time.time()
    arg1= request.args['arg1']
    arg2= request.args['arg2']
    arg3= request.args['arg3']
    database_ref.push(
        {
        "roomid":arg1,
        "applianceid":arg2,
        "status":arg3,
        "timestamp_UNIX":ts
    }
    )
    args = arg2+","+arg1+","+arg3
    with open('file.txt', 'w') as fh:
        fh.write(args)
    return redirect('http://localhost:5000/esp')

@app.route('/esp', methods=['GET'])
def esp():
    with open('file.txt') as f:
        return f.read()
@app.route('/bot')
def bot():
    arg1= request.args['arg1']
    print(checker(arg1))
    return "botsuccess"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
