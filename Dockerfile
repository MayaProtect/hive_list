FROM python:latest

WORKDIR /app

COPY . .

CMD [ "python" "show_all_lists.py" ]
