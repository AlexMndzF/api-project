# Api chat sentiments:

Para este proyecto nos han pedido realizar una api que nos devuelva varios parametros:

## - Introduccion de informacion:
La api esta preparada para recibir usuarios, chats y mensajes, esto va a una base de datos de MongoDB y se reparte en tres colecciones:
 - Chats: Almacena el nombre de los chats y su ID
 - Users: Almacena el nombre de los usuarios y su ID.
 - Messages: Almacena los mensajes y une las dos colecciones anteriores con sus object id.

## - Análisis de sentimiento:
El primer requisito de la api es analizar el sentimiento de un chat, para hacer esto se accede de la siguiente manera:
http://api-chat-sentiment.herokuapp.com/chat/chat_id/sentiment, donde chat_id es un entero qu ehace referencia al chat que queremos analizar.

Si accedemos al chat [0](http://api-chat-sentiment.herokuapp.com/chat/0/sentiment) obtenemos los siguientes datos:

{"mess-0": {"John Wick": "Hey Mike, whats up??"},<br/>"mess-1": {"Mike Wazowski": "Dude!!! \ud83d\ude00\ufe0f Did you watch the game last night?"}, <br/>
"mess-2": {"John Wick": "No, had to work. How was it?"},<br/> "mess-3": {"Mike Wazowski": "Awesome! Boyander scored 3 goals!"}, <br/>
"mess-4": {"John Wick": "No way! \ud83d\ude2e\ufe0f"},<br/>"mess-5": {"Mike Wazowski": "Way..."},<br/>
"mess-6": {"John Wick": "I bet people went crazy"},<br/> "mess-7": {"Mike Wazowski": "For sure. We stayed at KuboLoco until 6AM."},<br/> 
"mess-8": {"John Wick": "Motherfucker! Hungover? \ud83d\ude35\ufe0f"},<br/> 
"mess-9": {"Mike Wazowski": "Dead, burried and still suffering! \ud83e\udd2e\ufe0f"},<br/> 
"sentiment": {"polarity": 0.045000000000000005, "subjectivity": 0.3422222222222222}}<br/>

El formato de salida de la api es JSON, los elementes mess- hacen referencia a los mensajes del chat.<br/>

 - Polarity: Devuelve un valor de coma flotante entre -1 y 1:
    - -1: Sentimiento muy negativo.
    - 0: Sentimiento neutral
    - 1: Sentimiento muy positivo.
 - Subjectivity: Devuelve un valor de coma flotante entre 0 y 1:
    - 0: Muy objetivo.
    - 1: Muy subjetivo.

    La expresion subjetiva indica sentimientos personales, puntos de vista, creencias, opiniones, alegaciones, deseos, sospechas y especulaciones.

## Sitema de recomendacion de usuarios:

El sistema recomendador de la api devuelve los tres usuarios con mayor afinidad al usuario introducido, para acceder a esto se usa el siguiente link:
http://api-chat-sentiment.herokuapp.com/chatuser/name/recommend, donde name es un string que hace referencia al usuario que queremos recomendar.<br/>

Si accedemos al usuario [Tony Stark](http://api-chat-sentiment.herokuapp.com/user/Tony%20Stark/recommend) obrtenemos los siguientes datos:<br/>
{"recommended_users": ["John Wick", "J. Jonah Jameson", "Leia Organa"]}<br/>
El formato de salida de la api es JSON, devuelve una lista con los tres usuarios recomendados.

## Librerias:
 - bottle
 - pymongo
 - nltk
 - pandas
 - numpy
 - sklearn