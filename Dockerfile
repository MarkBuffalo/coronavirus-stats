FROM python:3.7.4

ADD coronavirus-stats-discord.py
ADD requirements.txt
ADD .env
RUN pip3 install -r requirements.txt

CMD [ "python3", "./coronavirus-stats-discord.py" ]
