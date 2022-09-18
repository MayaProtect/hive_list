FROM python:3.10-bullseye

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV MONGO_HOST=localhost
ENV MONGO_PORT=27017
ENV MONGO_DB=mayaprotect
ENV DEFAULT_LIMIT=25

EXPOSE 8080

CMD python run.py
