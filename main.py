import os

import event_handler

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

print("LAUNCHING SARA-SYSTEM")
client = event_handler.SARA_SYSTEM()
client.run(TOKEN)
