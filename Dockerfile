FROM python:3.9-alpine3.13
EXPOSE 5000
RUN mkdir app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
WORKDIR /app/api 
CMD ["python", "produce_api.py"]