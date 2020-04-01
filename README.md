# ada
Ada is a telegram bot that tells the status of our CI/CD.

### To develop

1. Install `pipenv`:
```
pip install pipenv
```

2. Synchronize the Pipfile with your computer:
```
pipenv sync
```

3. Spawn a shell inside the virtual environment:
```
pipenv shell
```

4. You should be able to run ada by starting the `gunicorn` server:
```
gunicorn -b 0.0.0.0:8000
```

5. Now try checking ada's health! On another shell type:
```
curl localhost:8000/_healthcheck
```

### FAQ

If you get an error saying `Environment variable "TELEGRAM_API_TOKEN" not set`, you need to add a
telegram bot API token to your environment. Go to telegram, [talk to BotFather](https://core.telegram.org/bots#3-how-do-i-create-a-bot)
and get an API token. With it, run
```
export TELEGRAM_API_TOKEN=000000.xxxxxxxxxxxxxxxx
```
and try running step 4 again.

If you get an error about the `Environment variable "GITHUB_SECRET" not set`: If you're not testing
the real ada, just exporting anything on this environment variable should work.
```
export GITHUB_SECRET=doesnt_matter
```
try running step 4 again.