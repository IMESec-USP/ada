from environs import Env

env = Env()
env.read_env()

TELEGRAM_API_TOKEN = env('TELEGRAM_API_TOKEN')
GITHUB_SECRET = env('GITHUB_SECRET')

CONVERSATIONS = env.list('CONVERSATIONS', [519013710], subcast=int)

HEALTHCHECK_SERVICES = {'LH website':'https://lh.imesec.ime.usp.br',
                        'LH API':'https://api.lh.imesec.ime.usp.br/hacks'}

HEALTHCHECK_SLEEP_AMOUNT = 2 * 60
HEALTHCHECK_ANOMALY_THRESHOLD = 5