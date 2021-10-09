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
            self.status = "online"

            #shorthand symbol for account type, for use of daily transaction file
            match self.type:
                case 'admin':
                    self.typeShort = 'AA'
                case 'full-standard':
                    self.typeShort = 'FS'
                case 'buy-standard':
                    self.typeShort = 'BS'
                case 'sell-standard':
                    self.typeShort = 'SS'

            #add the user to the database
            user = {"username": self.username, "type": self.type, "credit": self.credit, "status": self.status}
            collection.insert_one(user) 

            #add this transaction to the daily transaction file 
            transaction = "01" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + self.typeShort + "_" + str(self.credit + ("_" * (9 - len(str(self.credit)))))
            f = open("daily_transaction_file.txt", "a") 
            f.write(transaction) 

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

        #delete the user from the database 
        collection.delete_one({"username": self.username})

        #add this transaction to the daily transaction file 
        transaction = "02" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + self.typeShort + "_" + str(self.credit + ("_" * (9 - len(str(self.credit)))))
        f = open("daily_transaction_file.txt", "a") 
        f.write(transaction) 


    def addCredit(self, credit):
        """
        Add credit to user's account 
        """

        if(credit > 0):
            if(self.credit + credit > 999999):
                #update credit in database
                self.credit += credit 
                query = {"username:", self.username}
                newCredit = { "$set": {
                    "credit": self.credit + credit
                }}
                collection.update_one(query, newCredit)

                #add the transaction to the daily transaction file 
                transaction = '06' + "_" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + self.typeShort + "_" + str(self.credit + ("_" * (9 - len(str(self.credit)))))
                f = open("daily_transaction_file.txt", "a") 
                f.write(transaction) 
            else:
                raise ValueError("Exceeds credit limit")
        else:
            raise ValueError("Value must be greater than zero")

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

    def refund(self, other, credit):
        """
        Issue a refund from self (seller) to other (buyer) of amount credit 
        """

        #Check if other user exists 
        buyerQuery = {"username:", other.username}
        if(len(collection.find_one(buyerQuery) == 1) and credit > 0):
            #Make appropriate changes to each respective users' accounts 
            if(self.credit + credit > 999999):
                #Check if transaction will cause seller to exceed maximum credit limit 
                sellerQuery = {"username:", self.username}
                sellerCredit = { "$set": {
                    "credit": self.credit + credit
                }}
                buyerCredit = { "$set": {
                    "credit": self.credit - credit
                }}
                collection.update_one(buyerQuery, buyerCredit)
                collection.update_one(sellerQuery, sellerCredit)
            else:
                raise ValueError("Seller is over credit limit")
        elif(len(collection.find_one(buyerQuery) == 0)):
            raise ValueError("Buyer does not exist")
        elif(credit < 0):
            raise ValueError("Invalid value for credit")


