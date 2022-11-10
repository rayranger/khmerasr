FROM ubuntu

RUN apt update 
RUN apt install python3 -y
RUN apt install nodejs -y
RUN apt install npm -y
RUN apt install python3-pyaudio -y
RUN apt install python3-pip -y 
RUN pip3 install psycopg2-binary

WORKDIR /khmerasr

COPY requirements.txt requirements.txt
COPY package.json package.json

RUN pip3 install -r requirements.txt
RUN npm install

COPY . .

EXPOSE 5000

CMD [ "python3", "run.py" ]