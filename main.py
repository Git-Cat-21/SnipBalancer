from flask import Flask, render_template, request
import pyshorteners
import os 
import time
from redis.sentinel import Sentinel
import redis

redis_sentinels=os.environ.get('REDIS_SENTINELS')
redis_master_name=os.environ.get('REDIS_MASTER_NAME')
redis_password=os.environ.get('REDIS_PASSWORD')


app=Flask(__name__)

sentinels=[]

for s in redis_sentinels.split(","):
  sentinels.append((s.split(":")[0], s.split(":")[1]))

redis_sentinel = Sentinel(sentinels, socket_timeout=5,port=5000)
redis_master = redis_sentinel.master_for(redis_master_name,password = redis_password, socket_timeout=5)


def redis_command(command, *args):
  max_retries = 3
  count = 0
  backoffSeconds = 5
  while True:
    try:
      return command(*args)
    except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
        count += 1
        if count > max_retries:
            raise e
        print('Retrying in {} seconds'.format(backoffSeconds))
        time.sleep(backoffSeconds)

@app.route("/",methods=['POST','GET'])
def url_short():
    short_url=None
    if request.method == 'POST':
        url=request.form['url']
        s=pyshorteners.Shortener()
        short_url=s.tinyurl.short(url)
        redis_command(redis_master.set,short_url,url)
    return render_template('index.html',short=short_url)
    

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True,port=5000)