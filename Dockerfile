FROM python:3.7.10-alpine3.13
EXPOSE 5387
COPY . .
RUN pip install wheel setuptools
RUN npm install -g bespoken-tools
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
