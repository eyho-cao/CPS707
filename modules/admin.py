from user import User
import pymongo 



# initialize connection to mongoDB 

client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]


class Admin(User):

    def __init__(self):
        pass 


    def createUser(self, username, type, credit=0):
        """
        Create a User object 
        Default credit value to zero, unless other value is specified 
        """
        if(len(username) > 25):
            raise ValueError("Username exceeds 25 character limit")

        query = {"username": username} 
        result = collection.find_one(query) 

        if(result == None):
            #Check if username is unique 
            if((type in ['AA', 'FS', 'BS', 'SS'])):
                #Check if type is valid
                if(credit >= 0 and credit < 999999):
                    #Check if credit is valid

                    #add the user to the database
                    user = {"username": username, "type": type, "credit": credit}
                    collection.insert_one(user) 
                    
                    #TODOOOOO
                    """
                    #add this transaction to the daily transaction file 
                    transaction = "01" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + self.type + "_" + str(str(self.credit) + ("_" * (9 - len(str(self.credit)))))
                    f = open("daily_transaction_file.txt", "a") 
                    f.write(transaction) 
                    """

                else:
                    raise ValueError("Value for credit is not valid")
            else:
                raise ValueError("User type is invalid") 
        else:
            raise ValueError('Username is not unique')


    def buy(self, title, numTickets, sellName):
        return 0

    def deleteUser(username):
        """
        Deletes user from database
        """

        #delete the user from the database 
        collection.delete_one({"username": username})

        #add this transaction to the daily transaction file 
        transaction = "02" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + self.type + "_" + str(str(self.credit) + ("_" * (9 - len(str(self.credit)))))
        f = open("daily_transaction_file.txt", "a") 
        f.write(transaction) 

    def deleteTicket(ticket):
        """
        Delete a ticket from the DB 
        """
        pass 

    def refund(self, buyName, sellName, amount):
        return 0

    def refund(self, buyer, seller, credit):
        """
        Issue a refund from seller to buyer of amount credit 
        buyer:  buyer username 
        seller: seller username 
        NOTE: do not pass through user objects, just their usernames 
        """

        #Check if buyer exists 
        buyerQuery = {"username:", buyer}
        if(len(collection.find_one(buyerQuery) == 1) and credit > 0):
            #Make appropriate changes to each respective users' accounts 
            if(self.credit + credit < 999999):
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


    def addCredit(self, username, credit):
        """
        Add credit to user's account 
        """

        user = self.getUser(username)
        

        if(credit >= 0):
            if(user.getCredit() + credit <= 999999):
                #update credit in database
                balance = user.getCredit() + credit 
                query = {"username:", user.getUsername()}
                newCredit = { "$set": {
                    "credit": balance
                }}
                collection.update_one(query, newCredit)

                #add the transaction to the daily transaction file 
                transaction = '06' + "_" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + self.type + "_" + str(str(self.credit) + ("_" * (9 - len(str(self.credit)))))
                f = open("daily_transaction_file.txt", "a") 
                f.write(transaction) 
            else:
                raise ValueError("Exceeds credit limit")
        else:
            raise ValueError("Value must be greater than zero")

    def checkUnique(username):
        #uneeded, this is handled in the User object constructor
        return 0
