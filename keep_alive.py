from flask import Flask,jsonify
from threading import Thread
import admin
import time
import logging
app = Flask('')
uptime_start = time.time()
@app.route('/uptime')
def uptime():
    uptime_seconds = int(time.time() - uptime_start)
    days = uptime_seconds // (24 * 3600)
    hours = (uptime_seconds % (24 * 3600)) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    if days > 0:
       uptime_text = f"{days}d:{hours}h:{minutes}m:{seconds}s"
    else:
       uptime_text = f"{hours}h:{minutes}m:{seconds}s"
    return jsonify({'uptime': uptime_text})
@app.route('/test')
async def levelupdate():
   await admin.updateleaderboard()
   return "UPDATED"
@app.route('/')
def home():
  return "I'm alive @MiningArenaBot"

def run():
  log = logging.getLogger('werkzeug')
  log.disabled = True   
  app.logger.disabled = True
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()
  