import os
from _database import db_col
from pathlib import Path
from time import sleep
import math
import json
import datetime
ids=[]
fs=[
    'ds_apk:',
    'ds_apk2:',
    'ds_apk3:',
    'ds_apk4:'
    ]
    
lim=len(fs)
n=0
quit_file='res/quit_apk.txt'
slp_file='res/sleep_apk.txt'
ip_file='res/ipmongo_apk.txt'
base_url="https://www.apkmirror.com/wp-content/themes/APKMirror/download.php?id="

server=f"nohup ./rclone rcd --log-file=res/rapk_log.txt --rc-job-expire-duration=1ms --rc-job-expire-interval=1ms --rc-addr=0.0.0.0:5572 --retries=1 --log-level=DEBUG --rc-user=z --rc-pass=z &"

folder="apkmirror"

def get_val_from_file(f):
    return open(f).readlines()[0].strip()
def get_ctr():
  try:
    j=os.popen('./rclone rc --rc-user=z --rc-pass=z job/list').read()
    jl=json.loads(j)
  except Exception as e:
    print(str(e))
    return 2
  return math.log(len(jl['jobids']),2)

def set_limit(ctr):
    mux=2
    try:
        mux=int(get_val_from_file(slp_file))
    except Exception as e:
        print(str(e))
        print("ERROR IN READING SLEEP.txt")
        print(2,file=open(slp_file,'w'),end='')
    return mux*ctr
 
try:
    os.system(server)
    sleep(2)
except Exception as e:
    print("ERROR!!! UNABLE TO CREATE SERVER",str(e))
    pass
    
def get_def_cl():
    return db_col(folder,db='apks',host=get_val_from_file(ip_file))
def get_cl():
    return db_col(folder,db='apks')
def update_db(ids):
    try:
        get_cl().update_many({'id':{'$in':ids}},{"$set":{'ctr':1}})
        ids=[]
    except Exception as e:
        get_def_cl().update_many({'id':{'$in':ids}},{"$set":{'ctr':1}})
        print(str(e))
        ids=[]
    return ids
f_filter={'ctr':0}
project={'id':1,'_id':0}
try:
    jobs=[i for i in get_cl().find(f_filter,project)]
except Exception as e:
    jobs=[i for i in get_def_cl().find(f_filter,project)]


for job in jobs:
    dest=f"{job['id']}.apk"
    task = f'./rclone rc operations/copyurl fs={fs[n]} remote="{dest}" url="{base_url}{job["id"]}" _async=true --retries=1 --rc-user=z --rc-pass=z'
    ids.append(job['id'])
    try:
        # while len(queries)>0:
        ids=update_db(ids)
            # queries.pop()
    except Exception as e:
        print("ERROR CONNECTING TO DB",str(e))
    # print(task)
    os.system(task)
    try:
        if int(get_val_from_file(quit_file)):
            break
    except Exception as e:
        print("ERROR IN READING quit.txt")
        print(str(e))
        print(0,file=open(quit_file,'w'))

    n=(n+1)%lim
    if n==0:
        try:
            ctr=set_limit(get_ctr())
        except Exception as e:
            print("ERROR GETTING CTR!!!")
            print(str(e))
            ctr=5
        print(f"SLEEPING FOR {ctr} seconds, until {datetime.datetime.now()+datetime.timedelta(seconds=ctr)}")
        sleep(ctr)
while 1:
    try:
        ids=update_db(ids)
        break
    except Exception as e:
        print("ERROR: ",str(e))
        sleep(1000)


print(0,file=open(quit_file,'w'),end='')