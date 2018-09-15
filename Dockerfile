# Base docker image
FROM python:3.6-alpine

# Create service directory
WORKDIR /service

# Create user to run service under.   It's name is Snake Pliskin.
RUN adduser -S -h /service -H snake

# Copy requirements
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
# Install service requirements
&& pip install -r requirements.txt --upgrade

# Application code
COPY service.py service.py
COPY unchat_bot/ unchat_bot/

RUN chmod -R a+r unchat_bot

# Run as Snake
USER snake

# Start the bot
CMD [ "python", "./service.py" ]
