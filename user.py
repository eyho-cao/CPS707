import pymongo 


# initialize connection to mongoDB 

client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]


class User():

    def __init__(self, username, type, credit=0): 

        #check if the username is unique
        query = {"username": username} 
        result = collection.find(query) 

        if(len(result) == 0):
            #if the search yields no results, the username is unique
            self.username = username 
            self.type = type 
            self.credit = credit 

            #add the user to the database
            user = {"username": self.username, "type": self.type, "credit": self.credit}
            collection.insert_one(user) 
        else:
            raise ValueError('Username is not unique')

    def getUser(self, username):
        # get a user 
        query = {"username": username}
        result = collection.find(query) 

        return result 
        
    def deleteUser(self):
        #delete user from database 
        collection.delete_one({"username": self.username})

    def addCredit(self, credit):
        #add more credit to user's account

        self.credit += credit 
        query = {"username:", self.username}
        newCredit = { "$set": {
            "credit": self.credit + credit
        }}
        collection.update_one(query, newCredit)
