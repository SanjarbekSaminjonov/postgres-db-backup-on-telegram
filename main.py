import os

import environs
import requests

env = environs.Env()
env.read_env()

bot_token = env.str("BOT_TOKEN")
chat_id = env.str("CHAT_ID")
current_dir = env.str("CURRENT_DIR")
db_name = env.str("DB_NAME")
db_user = env.str("DB_USER")
backup_name = f"{db_name}_{db_user}.sql.gz"

os.chdir(current_dir)
command = f"docker exec -t {db_name} pg_dumpall -c -U {db_user} | gzip > {backup_name}"
os.system(command)

file_path = os.path.join(current_dir, backup_name)
with open(file_path, "rb") as file:
    res = requests.post(
        url=f"https://api.telegram.org/bot{bot_token}/sendDocument",
        data={"chat_id": chat_id},
        files={"document": (file.name, file)},
    )

os.remove(file_path)
