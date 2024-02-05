import aiofiles
import json

async def find_uid(username:str):
   username = username.replace('@','')
   file_name = "json_data/usernames.json"
   async with aiofiles.open(file_name, 'r') as f:
     usernames = json.loads(await f.read())
   if username in usernames:
     return usernames[username]
   else:
     return False

async def save_uid(username:str,uid:int):
   print(f"{username} || {uid}")
   username = username.replace('@','')
   file_name = "json_data/usernames.json"
   async with aiofiles.open(file_name, 'r') as f:
     usernames = json.loads(await f.read())
   if username not in usernames:
     usernames[username] = uid
     async with aiofiles.open(file_name, 'w') as f:
       await f.write(json.dumps(usernames))
     return True
   else:
     return False