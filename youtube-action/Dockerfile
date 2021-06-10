FROM python:3.7.10-alpine3.13
RUN apk update && apk add py-pip libressl-dev libffi-dev gcc python3-dev git nodejs npm nano wget curl net-tools unzip supervisor screen
COPY . .
RUN pip install wheel setuptools
RUN pip install -r requirements.txt
RUN npm install -g bespoken-tools
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
