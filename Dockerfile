FROM python:3.13-slim

COPY . .

RUN pip install -r repositories.txt

CMD ["CMD", "main:app", "--host", "0.0.0.0", "--port", "80"]