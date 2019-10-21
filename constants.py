from environs import Env

env = Env()
env.read_env()

TELEGRAM_API_TOKEN = env('TELEGRAM_API_TOKEN')
GITHUB_SECRET = env('GITHUB_SECRET')

# Dict of conversations IDs followed by regex to match agains repository names
convs_default = {
	131845033: ".*",
	-1001342903759: ".*lightning-hacks.*",
	-388287091: "^((?!lightning-hacks).)*$",
	211525815: ".*"
}

CONVERSATIONS = env.dict('CONVERSATIONS', convs_default)