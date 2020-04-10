from environs import Env

CHAT_ID_LIGHTNING_HACKS = -1001342903759
CHAT_ID_IMESEC_CORE     = -1001284501077
CHAT_ID_RAZGRIZONE      = 131845033
CHAT_ID_R0ZBOT          = 211525815

ADA_URL = 'https://ada.imesec.ime.usp.br/_healthcheck'

env = Env()
env.read_env()

TELEGRAM_API_TOKEN = env('TELEGRAM_API_TOKEN')
GITHUB_SECRET = env('GITHUB_SECRET')

# Dict of conversations IDs followed by regex to match agains repository names
default_conversations = {
    CHAT_ID_RAZGRIZONE: '.*',
    CHAT_ID_LIGHTNING_HACKS: '^((?!dockerhub).)*lightning-hacks.*$',
    CHAT_ID_IMESEC_CORE: '^((?!lightning-hacks).)*$',
    CHAT_ID_R0ZBOT: '.*'
}


def __conversation_subcast(s: str):
    try:
        return int(s)
    except:
        return s


CONVERSATIONS = env.dict('CONVERSATIONS', default_conversations, subcast=__conversation_subcast)

HEALTHCHECK_SERVICES = {'lightning-hacks Website': 'https://lh.imesec.ime.usp.br',
                        'lightning-hacks API': 'https://api.lh.imesec.ime.usp.br/hacks',
                        'lightning-hacks Timer': 'https://timer.imesec.ime.usp.br',
                        'IMEsec wiki': 'https://wiki.imesec.ime.usp.br',
                        'IMEsec Website': 'https://imesec.ime.usp.br'
                        }

HEALTHCHECK_SLEEP_AMOUNT = 2 * 60
HEALTHCHECK_ANOMALY_THRESHOLD = 3
