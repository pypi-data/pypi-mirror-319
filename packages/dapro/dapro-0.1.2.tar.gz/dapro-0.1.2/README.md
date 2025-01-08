# dapro
DATOE simplifies handling `.eval` and `.open` commands in Python Telegram bots.

## Installation
```bash
pip install dapro
```
## Usage
```bot.py
from dapro import daeval, daopen

OWNERS = "OWNER_ID"

@client.on(events.NewMessage(pattern=".eval"))
async def eval(event):
    await daeval(event, client, OWNERS)

@client.on(events.NewMessage(pattern=".open"))
async def open_file(event):
    await daopen(event, client)
```
---
