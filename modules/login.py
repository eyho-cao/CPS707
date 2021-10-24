import pymongo
from admin import Admin
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
        userObj
        if(result != None):
            #logged in
            user = getUser(username)
            userType = user.getType()
            if(userType == "AA"):
                #admin login
                userObj = Admin()
                return 0
            elif(userType == "FS"):
                #full S login
                userObj = FSUser(user)
                return 0
            elif(userType == "BS"):
                #buy S login
                userObj = BSUser(user)
                return 0
            elif(userType == "SS"):
                #sell S login
                userObj = SSUser(User)
                return 0
            else:
                raise ValueError("Account type not found")
        else:
            return 1
