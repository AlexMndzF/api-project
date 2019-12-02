FROM python:3.7

ADD . .

RUN pip install -r requirements.txt

RUN adduser --disabled-password myuser
USER myuser 

CMD ["python3","-u","api.py"]