# dapro
dapro = Dipanshu Agarwal Programs

## Installation
```bash
pip install dapro
```
## Usage
```bot.py
from dapro.telegram.telethon import daeval, daopen

OWNERS = "OWNER_ID"

@client.on(events.NewMessage(pattern=".eval"))
async def eval(event):
    await daeval(event, client, OWNERS)

@client.on(events.NewMessage(pattern=".open"))
async def open_file(event):
    await daopen(event, client)
```
---
