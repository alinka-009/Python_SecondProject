from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
MAIN_ADMINS = env.list('MAIN_ADMINS')
IP = env.str("ip")
