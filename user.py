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

        #check if usename exceeds character limit 
        if(len(username) > 25):
            raise ValueError("Username exceeds 25 character limit")

        if(len(result) == 0):
            #if the search yields no results, the username is unique
            self.username = username 
            if((type in ['AA', 'FS', 'BS', 'SS'])):
                self.type = type 
                if(credit > 0 and credit < 999999):
                    self.credit = credit 

                    #add the user to the database
                    user = {"username": self.username, "type": self.type, "credit": self.credit}
                    collection.insert_one(user) 

                    #add this transaction to the daily transaction file 
                    transaction = "01" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + self.typeShort + "_" + str(self.credit + ("_" * (9 - len(str(self.credit)))))
                    f = open("daily_transaction_file.txt", "a") 
                    f.write(transaction) 

                else:
                    raise ValueError("Value for credit is not valid")
            else:
                raise ValueError("User type is invalid") 
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
        query = {"username:", username}
        result = collection.find_one(query)
        user = User(result.get('Username'), result.get('type'), result.get('credit'))
        
        return user

    def getUsername(self):
        """
        Return a User instance's username 
        """
        return self.username

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

        #Set user's status to offline in db 
        if(self.status == "online"):
            query = {"username:", self.username}
            newCredit = { "$set": {
            "status": "offline"
            }}
            collection.update_one(query, newCredit)
        else:
            raise ValueError('User status error')
        
        #add the transaction to the daily transaction file 
        transaction = '02' + "_" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + self.typeShort + "_" + str(self.credit + ("_" * (9 - len(str(self.credit)))))
        f = open("daily_transaction_file.txt", "a") 
        f.write(transaction) 



