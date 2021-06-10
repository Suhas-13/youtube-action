FROM python:3.8-slim-buster
RUN apt-get update && apt-get install -y git nodejs npm nano wget curl net-tools unzip supervisor procps
COPY . .
RUN pip3 install -r requirements.txt
RUN npm install -g bespoken-tools
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]