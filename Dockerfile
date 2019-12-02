FROM python:3.7-slim
ADD . .
RUN pip3 install -r requirements.txt
RUN adduser --disabled-password myuser
USER myuser 
EXPOSE 8080
CMD ["python3","-u","api.py"]