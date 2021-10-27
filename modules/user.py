import pymongo 


# initialize connection to mongoDB 

client = pymongo.MongoClient("mongodb+srv://trinh:mvh5sYgCX1pXo08y@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]

class User():

    def __init__(self, username): 
        """
        Constructor for User object 
        Default credit value to zero, unless other value is specified 
        """

        #check if the username is unique
        query = {"username": username} 
        result = collection.find_one(query) 
        #check if usename exceeds character limit 
        
        if(result != None):
            self.username = username
            self.type = result.get('type')
            self.credit = result.get('credit')
        else:
            raise ValueError("User does not exist")

    def __str__(self):
        """
        string formatting for instances of User object
        u = User('trinh','admin')
        print(u)
        >>> User(username='trinh', type='AA', credit=0)
        """
        return f'User(username={self.username}, type={self.type}, credit={self.credit})'

    def __repr__(self):
        return f'User(username={self.username}, type={self.type}, credit={self.credit})'

    def getUser(self, username):
        """
        Return User object based on unique username
        """
        query = {"username": username}
        result = collection.find_one(query)
        if(result is not None):
            user = User(result.get('username'))
        
            return user
        else:
            return None

    def getUsername(self):
        """
        Return a User instance's username 
        """
        return self.username

    def addCredit(self, credit):
        """
        #delete the user from the database 
        collection.delete_one({"username": self.username})
        #add this transaction to the daily transaction file 
        transaction = "02" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + self.type + "_" + str(str(self.credit) + ("_" * (9 - len(str(self.credit)))))
        f = open("daily_transaction_file.txt", "a") 
        f.write(transaction) 
        """
        pass

    def getCredit(self):
        """
        Return a User instance's credit 
        """
        return self.credit

    def getType(self):
        """
        Return a User instance's type
        """
        return self.type

    def logout(self): 
        """
        Logout of current session
        """
        """
        #Set user's status to offline in db 
        if(self.status == "online"):
            query = {"username:", self.username}
            newCredit = { "$set": {
            "status": "offline"
            }}
            collection.update_one(query, newCredit)
        else:
            raise ValueError('User status error')
        """

        #add the transaction to the daily transaction file 
        transaction = '00' + " " + str(self.username) + " " + self.type + " " + str(str(self.credit))+"\n"
        f = open("daily_transaction_file.txt", "a") 
        f.write(transaction) 
        f.close()

    def refund(self, seller, buyer, credit):
        raise ValueError("Insufficient Permissions")

    def createUser(self, username, userType, credit=0):
        raise ValueError("Insufficient Permissions")

    def sell(self, title, price, numTickets):
        raise ValueError("Insufficient Permissions")

    def buy(self, title, numTickets, seller):
        raise ValueError("Insufficient Permissions")

    def deleteUser(self, username):
        raise ValueError("Insufficient Permissions")
