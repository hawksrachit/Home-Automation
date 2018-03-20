
import aiml
import sys
import os
from nltk.stem import WordNetLemmatizer
import nltk
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




while True: 
    user_in = input()
    #bot_response = mybot.respond(user_in)
    print(checker(user_in))


