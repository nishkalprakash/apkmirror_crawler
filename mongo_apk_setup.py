from _database import db_col

# cl=db_col()
folder='apkmirror'
limit=10**6
docs=[{'id':i,'ctr':0} for i in range(limit)]
def get_def_cl():
    return db_col(folder,db='apks',host=open('ipmongo_apk.txt').read().strip())
def get_cl():
    return db_col(folder,db='apks')
try:
    i=get_cl().create_index([('id',1)],unique=True)
except Exception as e:
    i=get_def_cl().create_index([('id',1)],unique=True)

try:
    i=get_cl().insert_many(docs,ordered=False)
except Exception as e:
    i=get_def_cl().insert_many(docs,ordered=False)
print(len(i.inserted_ids))