FROM python:3-alpine3.10
WORKDIR /certifyme
COPY . /certifyme
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./app.py
