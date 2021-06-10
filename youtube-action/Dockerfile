FROM python:3.7.10-alpine3.13
RUN apk update && apk add libressl-dev postgresql-dev libffi-dev gcc musl-dev p$
COPY . .
RUN pip install wheel setuptools
RUN npm install -g bespoken-tools
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
