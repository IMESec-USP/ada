from python:alpine

run apk update
run apk add python3 gcc python3-dev libc-dev musl-dev libffi-dev openssl-dev
run python3 -m ensurepip
run pip3 install --upgrade pip
run pip3 install pipenv

workdir /ada
copy Pipfile Pipfile.lock ./
run pipenv sync

copy . .
expose 8000
cmd ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]