To install the package, use poetry:

```bash
poetry install telegram_message
```

Сreate file ".env":
"
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
TELEGRAM_START_HOUR=11
TELEGRAM_END_HOUR=18
"

Example of use:
"
from telegram_message import send
import os

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

message = "HELLO"

send(bot_token, chat_id, message)
"
