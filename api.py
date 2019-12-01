from bottle import route, run, get, post, request
import bson
from functions.mongo import connectCollection
from bson.json_util import dumps
db, coll = connectCollection('chats','messages')
db, collus = connectCollection('chats','users')
db, collchat = connectCollection('chats','chats')

@get("/test")
def test():
    return {"CONNECTED"}


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
        name = chat_data[i].get('userName')
        message = chat_data[i].get('text')
        date = chat_data[i].get('datetime')
        ret[f'{name}_{date}'] = message        
    return ret

@get("/users")
def getusers():
    return dumps(collus.find({}))

@post('/user/create')
def newUser():
    new_id = max(collus.distinct("User_id")) + 1
    name = str(request.forms.get("userName",f"User-{new_id}"))
    new_user = {
        "User_id": new_id,
        "name": name
    }
    '''collus.insert_one(new_user)
    userid_obj = list(collus.find({"User_id":new_id}))[0].get('_id')
    return userid_obj'''

@post('/chat/create')
def newChat():
    new_id = max(collchat.distinct("Chat_id")) + 1
    name = str(request.forms.get("name",f"chat-{new_id}"))
    new_chat = {
        "Chat_id": new_id,
        "name": name
    }
    '''collchat.insert_one(new_chat)
    chatid_obj = list(collchat.find({ "Chat_id": new_id}))[0].get('_id')
    return chatid_obj'''

@post("/message/add")
def add():
    '''
    This is the supported data structure, the idUser is a field that take the objetid from the user collection.
    {'idUser': ,
    'userName': 'John Wick',
    'idMessage': 0,
    'idChat': 0,
    'datetime': '2019-10-17 10:15:41',
    'text': 'Hey Mike, whats up??'}
    
    '''
    user = list(collus.find({'User_id':int(request.forms.get('idUser'))}))
    chat = list(collchat.find({'Chat_id':int(request.forms.get('idChat'))}))
    if len(user) == 0:
    #create user
        idu = newUser()
    else:
        userid = user[0].get('User_id')
        idu = list(collus.find({'User_id':userid}))[0].get('_id')
    if len(chat):
        idChat = newChat()
    else:
        chatid = chat[0].get('Chat_id')
        idChat = list(collchat.find({'Chat_id':chatid}))[0].get('_id')
    
    name=request.forms.get("userName")
    idmess = request.forms.get('idMessage')
    time = request.forms.get('datetime')
    text = request.forms.get('text')
    return {'idUser': idu ,
    'userName': name,
    'idMessage': idmess,
    'idChat': idChat,
    'datetime': time,
    'text': text}




'''
def addChat(self,chat):
    
    This is the supported data structure, the idUser is a field that take the objetid from the user collection.
    {'idUser': ,
    'userName': 'John Wick',
    'idMessage': 0,
    'idChat': 0,
    'datetime': '2019-10-17 10:15:41',
    'text': 'Hey Mike, whats up??'}
    
    coll
    if chat['userName']
    a=collection.insert_one(chat)
    print("Inserted", a.inserted_id)
    return a.inserted_id
    '''


run(host='0.0.0.0', port=8080)
