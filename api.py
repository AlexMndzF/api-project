from bottle import route, run, get, post, request
import random
import bson
from functions.mongo import connectCollection


@get("/chat/0")
def index():
    return {
        "nombre": random.choice(["Pepe", "Juan", "Fran", "Luis"])
    }


@get("/chat/<chat_id>/list")
def getChat(chat_id):
    '''
    This function admit onlu integers
    '''
    db, coll = connectCollection('chats','messages')
    db, collchat = connectCollection('chats','chats')
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



'''@post('/add')
def add():
    print(dict(request.forms))
    autor=request.forms.get("autor")
    chiste=request.forms.get("chiste")  
    return {
        "inserted_doc": str(coll.addChiste(autor,chiste))}





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
    return a.inserted_id'''


run(host='0.0.0.0', port=8080)
