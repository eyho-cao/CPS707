import pymongo 

client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]

query = {"username": "a"}
z = collection.find_one(query) 

print(z)
print(z == None)