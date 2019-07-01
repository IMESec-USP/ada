from python:alpine

run apk update
run apk add python3 gcc python3-dev libc-dev musl-dev libffi-dev openssl-dev
run python3 -m ensurepip
run pip3 install --upgrade pip

workdir /ada
copy requirements.txt /ada
run pip install -r requirements.txt

copy . .
cmd ["gunicorn", "app:app"]