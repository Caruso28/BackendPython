# Descarga version community: https://www.mongodb.com/try/download
# Instalacion: https://www.mongodb.com/docs/manual/tutorial
# Modulo conexion MongoDB: pip install pymongo
# Ejecucion: sudo mongod --dbpath "/path/a/la/base/de/datos/"
# Conexion: mongodb://localhost

from pymongo import MongoClient

db_cient = MongoClient().local

