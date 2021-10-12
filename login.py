import pymongo
from adminUser import Admin
from BuySUser import BSUser
from SellSUser import SSUser
from fullSUser import FSUser


client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]
eventCollection = db["events"]

class Login():
    def login(username):
        query = {"username": username} 
        result = collection.find_one(query)
        if(len(result) == 1):
            #logged in
            user = getUser(username)
            userType = user.getType()
            if(userType == "AA"):
                #admin login
                
            elif(userType == "FS"):
                #full S login

            elif(userType == "BS"):
                #buy S login

            elif(userType == "SS"):
                #sell S login

            else:
                raise ValueError("Account type not found")
