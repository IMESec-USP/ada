FROM python:alpine

RUN apk update
RUN apk add python3 gcc python3-dev libc-dev musl-dev libffi-dev openssl-dev ansible
RUN python3 -m ensurepip
RUN pip3 install --upgrade pip

WORKDIR /ada
COPY requirements.txt /ada
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]