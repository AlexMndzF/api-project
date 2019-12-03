from bottle import route, run, get, post, request, template
import bson
from functions.mongo import connectCollection
from bson.json_util import dumps,ObjectId, DatetimeRepresentation
from datetime import datetime
from textblob import TextBlob   
import json
import webbrowser
from nltk.tokenize import RegexpTokenizer
import pandas as pd
from nltk.corpus import stopwords
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as distance

db, coll = connectCollection('chats','messages')
db, collus = connectCollection('chats','users')
db, collchat = connectCollection('chats','chats')


@get("/test")
def test():
    return {"CONNECTED"}

@get("/")
def home():
    return template('info', title="INFORMATION")


@get("/chat/<chat_id>/list")
def getChat(chat_id):
    '''
    This function admit onlu integers
    '''
    chatid_data = list(collchat.find({'Chat_id':int(chat_id)}))
    chat_obj_id = chatid_data[0].get('_id')
    chat_data = list(coll.find({'idChat':chat_obj_id}))
    ret = {}
    for i in range(len(chat_data)):
        idmess = chat_data[i].get('idMessage')
        name = chat_data[i].get('userName')
        message = chat_data[i].get('text')
        ret[f'mess-{idmess}'] = {
            name:message

        }        
    return dumps(ret)

@get("/users")
def getusers():
    return dumps(collus.find({}))


@get("/chat/<chat_id>/sentiment")
def sentiment(chat_id):
    chat = getChat(chat_id)
    chat =  json.loads(chat)
    polarity = []
    subjectivity = []
    #labels = [] 
    for k in chat:
        #labels.append(k)
        for key in chat[k]:
            data2 = chat[k][key]
            sent = TextBlob(data2).sentiment
            polarity.append(sent.polarity)
            subjectivity.append(sent.subjectivity)
    polarityavg = sum(polarity)/len(polarity)
    subjectivityavg = sum(subjectivity)/len(subjectivity)
    chat['sentiment'] = {
    'polarity':polarityavg,
    'subjectivity':subjectivityavg
    }
    return dumps(chat)
@get('/user/create')
def insert_name():
    return template('user')
@get("/message/add")
def inser_message():
    return template('message')
@get('/chat/create')
def inser_chat():
    return template('chat')
    

@post('/user/create')
def newUser():
    new_id = max(collus.distinct("User_id")) + 1
    name = str(request.forms.get("userName",f"User-{new_id}"))
    new_user = {
        "User_id": new_id,
        "name": name
    }
    collus.insert_one(new_user)
    userid_obj = list(collus.find({"User_id":new_id}))[0].get('_id')
    return userid_obj

@post('/chat/create')
def newChat():
    new_id = max(collchat.distinct("Chat_id")) + 1
    name = str(request.forms.get("name",f"chat-{new_id}"))
    new_chat = {
        "Chat_id": new_id,
        "name": name
    }
    collchat.insert_one(new_chat)
    chatid_obj = list(collchat.find({ "Chat_id": new_id}))[0].get('_id')
    return dumps(chatid_obj)

@post("/message/add")
def add():
    user = list(collus.find({'User_id':int(request.forms.get('idUser'))}))
    chat = list(collchat.find({'Chat_id':int(request.forms.get('idChat'))}))
    if len(user) == 0:
    #create user
        idu = newUser()
        print(idu)
    else:
        userid = user[0].get('User_id')
        idu = list(collus.find({'User_id':userid}))[0].get('_id')
        print(idu)
    if len(chat) ==0:
        idChat = newChat()
        print(idChat)
    else:
        chatid = chat[0].get('Chat_id')
        idChat = list(collchat.find({'Chat_id':chatid}))[0].get('_id')
        print(idChat)
    print(ObjectId(idu))
    params = {'idUser': idu ,
    'userName': list(collus.find({"_id":idu}))[0].get('name'),
    'idMessage': max(coll.distinct('idMessage')) + 1,
    'idChat': idChat,
    'datetime':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'text': request.forms.get('text')}
    coll.insert_one(params)
    return dumps(params)


@get("/user/<name>/recommend")
def recomenduser(name):
    n=name
    data = list(coll.find({}))
    if name not in list(set([e['userName'] for e in data])):
        error = 'Sorry, this user does not exist in the database'
        print({'Exception':error}) 
    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = set(stopwords.words('english'))       
    TokensDict = {}
    for name in list(set([e['userName'] for e in data])):
        usersData = list(coll.find({'userName': name}))
        usersTokens = [tokenizer.tokenize(e['text']) for e in usersData]
        usersTokens_clean = [word for message in usersTokens for word in message if word not in stop_words]
        TokensDict[name] = ' '.join(usersTokens_clean)
    count_vectorizer = CountVectorizer()
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(TokensDict.values())
    Tokens_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(Tokens_term_matrix,columns=count_vectorizer.get_feature_names(),index=TokensDict.keys())
    similarity_matrix = distance(df, df)
    sim_df = pd.DataFrame(similarity_matrix, columns=TokensDict.keys(), index=TokensDict.keys())
    np.fill_diagonal(sim_df.values, 0)
    return {'recommended_users': [e for e in list(sim_df[n].sort_values(ascending=False)[0:3].index)]}





run(host='0.0.0.0', port=8080)
