FROM python:3.7.4

ADD coronavirus-stats-discord-bot.py /tmp
ADD requirements.txt /tmp
ADD .env /tmp
RUN pip3 install -r /tmp/requirements.txt

CMD [ "python3", "./tmp/coronavirus-stats-discord-bot.py" ]
