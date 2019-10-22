# ada
Ada is a telegram bot that tells the status of our CI/CD.

### To develop

This repository contains submodules: after cloning, run

```
git submodule init
git submodule update
```

You'll need a `.env` file in the root folder _at least_ containing the following:

```
TELEGRAM_API_TOKEN=... (create a bot with botfather and insert its token here)
GITHUB_SECRET=... (ask us for this)
```

You'll probably want to run Ada in a python virtual environment. For this,
source a file in `venv` folder, depending on your shell:

```bash
source venv/bin/activate # for bash/zsh
# OR
source venv/bin/activate.fish # for fish
# etc.
```

After that, install the python requirements.

```bash
pip3 install -r requirements.txt
```

You're now ready to develop Ada. To run her in the terminal, run

```bash
gunicorn app:app
```