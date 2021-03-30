FROM python:3.9-alpine3.13
RUN mkdir app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
WORKDIR /app/api 
CMD ["nohup", "python", "produce_api.py", "&", "--host:0.0.0.0"]