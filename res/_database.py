from pymongo import MongoClient

# def init_db():
#     global mclient
#     url = "115.248.191.18"
#     url = "localhost"
#     mclient = MongoClient(url)["CCB"]

def db_col(col='apkmirror',host='10.105.72.43',db='apks'):
    return MongoClient(host)[db][col]

# init()
# def hpc_db_col(collection_name):
#     return MongoClient("115.248.191.18")["CCB"][collection_name]
