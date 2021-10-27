import pymongo
from admin import Admin
from BuySUser import BSUser
from SellSUser import SSUser
from fullSUser import FSUser
from user import User


client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]
eventCollection = db["events"]

class Login():
    def login(username):
        query = {"username": username} 
        result = collection.find_one(query)
        if(result != None):
            #logged in
            user = username
            userType = result.get('type')
            if(userType == "AA"):
                #admin login
                userObj = Admin(user)
                return userObj
            elif(userType == "FS"):
                #full S login
                userObj = FSUser(user)
                return userObj
            elif(userType == "BS"):
                #buy S login
                userObj = BSUser(user)
                return userObj
            elif(userType == "SS"):
                #sell S login
                userObj = SSUser(User)
                return userObj
            else:
                return 0 #account type not found exit
        else:
            return 1 #account not found exit
