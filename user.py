import pymongo 


# initialize connection to mongoDB 

client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]


class User():

    def __init__(self, username, type, credit=0): 
        """
        Constructor for User object 

        Default credit value to zero, unless other value is specified 
        """

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

    def __str__(self):
        """
        string formatting for instances of User object 

        u = User('trinh','admin')
        print(u)

        >>> User(username='trinh', type='admin', credit=0)
        """
        return f'User(username={self.username}, type={self.type}, credit{self.credit}'

    def __repr__(self):
        return f'User(username={self.username}, type={self.type}, credit{self.credit}'

    def getUser(username):
        """
        Return User object based on unique username
        """
        query = {"username": username}
        result = collection.find(query) 

        return result 
        
    def deleteUser(self):
        """
        Deletes user from database
        """
        collection.delete_one({"username": self.username})

    def addCredit(self, credit):
        """
        Add credit to user's account 
        """

        self.credit += credit 
        query = {"username:", self.username}
        newCredit = { "$set": {
            "credit": self.credit + credit
        }}
        collection.update_one(query, newCredit)


