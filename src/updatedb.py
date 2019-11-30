import json
from functions.mongo import connectCollection
from bson.objectid import ObjectId
# connecting to database and charging the original database
db, coll = connectCollection('chats','messages')

with open('../input/chats.json') as f:
    chats_json = json.load(f)
coll.insert_many(chats_json)

# Making users collection
data = list(coll.find({}))
namelst=[]
for i in range(len(data)):
    name = data[i]['userName']
    userid = data[i]['idUser']
    tup = (userid,name)
    namelst.append(tup)
namelst = set(namelst)
lst = []
for e in namelst:
    uid = e[0]
    name= e[1]
    dictionary = {
        'User_id':uid,
        'name': name
    }
    lst.append(dictionary)
db, collus = connectCollection('chats','users')
with open('../output/users.json', 'w') as fp:
    json.dump(lst, fp)

with open('../output/users.json') as f:
    users_json = json.load(f)
collus.insert_many(users_json)

#Make id, objectid dictionary
usersdata = list(collus.find({}))
dic_ids = {}
for i in range(len(usersdata)):
    user = usersdata[i].get('User_id')
    objid = usersdata[i].get('_id')
    dic_ids[user]=objid


 #Update objets userid in chats collection messages  
for i in range(len(data)):
    idu = dic_ids.get(data[i]['idUser'])
    value = {"$set":{'idUser':idu}}
    coll.update_one(data[i],value)

#crating Chats collection:
chatlst = []
for i in range(len(data)):
    idc = data[i]['idChat']
    name = f'chat-{idc}'
    chatlst.append((name,idc))
chatlst=list(set(chatlst))
chatlst
lst = []
for e in chatlst:
    idc = e[1]
    name= e[0]
    dictionary = {
        'Chat_id':idc,
        'name': name
    }
    lst.append(dictionary)
db, collchat = connectCollection('chats','chats')
with open('./output/chats_id.json', 'w') as fp:
    json.dump(lst, fp)
with open('./output/chats_id.json') as f:
    chats_json = json.load(f)
collchat.insert_many(chats_json)
datachat = list(collchat.find({}))

#diccionario de chats y objid chats:
dic_ids_chat={}
for i in range(len(datachat)):
    chat = datachat[i].get('Chat_id')
    objid_chat = datachat[i].get('_id')
    dic_ids_chat[chat]=objid_chat
dic_ids_chat

 #Actualizacion de registros de la base de datos:
for i in range(len(data)):
    idu = dic_ids_chat.get(data[i]['idChat'])
    value = {"$set":{'idChat':idu}}
    coll.update_one(data[i],value)