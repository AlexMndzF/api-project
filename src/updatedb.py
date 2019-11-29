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