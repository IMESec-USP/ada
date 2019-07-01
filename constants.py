from environs import Env

env = Env()
env.read_env()

TELEGRAM_API_TOKEN = env('TELEGRAM_API_TOKEN')
GITHUB_SECRET = env('GITHUB_SECRET')

CONVERSATIONS = [131845033]