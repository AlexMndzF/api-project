from bottle import route, run, get, post, request
import bson
from functions.mongo import connectCollection
from bson.json_util import dumps,ObjectId, DatetimeRepresentation
from datetime import datetime
from textblob import TextBlob
import json
import matplotlib.pyplot as plt
import webbrowser


db, coll = connectCollection('chats','messages')
db, collus = connectCollection('chats','users')
db, collchat = connectCollection('chats','chats')

@get("/test")
def test():
    return {"CONNECTED"}
@get("/")
def info():
    params = '''
<html>
    <body style="background-color: rgb(221, 221, 221);">
        <div style="display: flex;justify-content: center;margin-top: 10vh;">
            <table border="3", cellspacing="5" width='700vw'style='background-color: yellowgreen'>
                <tr><th><h1>INFORMATION:</h1></th></tr>             
                <tr><td style="text-align: center;"><h3>Structure for make a message post in the api:</h3></td></tr>                
                <tr><td style="padding-left: 20px;"><p>{'idUser': <strong>#integer</strong> ,</p>
                <p>'userName': 'John Wick', <strong>#String</strong></p>
                <p>'idChat': 0, <strong>#integer</strong></p>
                <p>'text': 'Hey Mike, whats up??'}<p></td></tr>
                <tr><td style="text-align: center;"><h3>Structure for make user post: </h3></td></tr>
                <tr><td style="padding-left: 20px;"><p>{'userName':'Toni stark'} #The name is optional </p></td></tr>             
                <tr><td style="text-align: center;"><h3>Structure for make a chat post:</h3></td></tr>
                <tr><td style="padding-left: 20px;"><p>{'name': 'Jon Snow-khaleesi'} #The name is optional</p></td></tr>
            </table>
        </div>
    </body>
</html>
    '''
    return params


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
    for k in chat:
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
    plt.plot(polarity)
    plt.savefig('polarity.png')
    html = '<img src=\'polarity.png\'>'
    with open('polarity.html','w') as f:
        f.write(html)
    webbrowser.open('./polarity.html', new=2)
    return dumps(chat)
    

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
    return dumps(userid_obj)

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
    '''
    This is the supported data structure, the idUser is a field that take the objetid from the user collection.
    {'idUser': ,
    'userName': 'John Wick',
    'idMessage': 0,
    'idChat': 0,
    'text': 'Hey Mike, whats up??'}
    
    '''
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
        print(chat)
        chatid = chat[0].get('Chat_id')
        idChat = list(collchat.find({'Chat_id':chatid}))[0].get('_id')
        print(idChat)
    
    params = {'idUser': idu ,
    'userName': list(collus.find({'_id':idu}))[0].get('name'),
    'idMessage': max(coll.distinct('idMessage')) + 1,
    'idChat': idChat,
    'datetime':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'text': request.forms.get('text')}
    coll.insert_one(params)
    return dumps(params)




run(host='0.0.0.0', port=8080)
