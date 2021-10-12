from user import User
import pymongo 



# initialize connection to mongoDB 

client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]
eventCollection = db["events"]

class Admin(User):

    def __init__(self):
        pass 


    def create(self, username, type, credit=0):
        """
        Create a User object 

        Default credit value to zero, unless other value is specified 
        """
        try:
            user = User(username, type, credit)
        except ValueError:
            print("Value error")

    def buy(self, title, numTickets, sellName):
        sellerQuery = {"username:", sellName}
        eventQuery = {"events", title}
        if(not len(collection.find_one(sellerQuery) == 1)):
            print("Invalid Seller");
        eventQResult = eventCollection.find_one(eventQuery)
        if(not len(eventQResult == 1)):
            print("Invalid Title");
        remainingTick = eventQResult.get('quantity')-numTickets #get number of tickets left in event ##NOTE: IM NOT SURE IF THIS IS HOW ITS ACTUALLY DONE
        titlePrice = eventQResult.get('price')
        if(remainingTick >=0):
            print("Price per Ticket: " +titlePrice +"\nTotal Price: " +titlePrice*numTickets)
            userInput = input("Confirm Transaction Y/N")
            if(userInput == "Y" or userInput == "yes" or userInput == "Yes"):
                ticketsLeft = { "$set": {
                    "quantity": remainingTick
                }}

                eventCollection.update_one(eventQuery, remainingTick)
                transaction = "04" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + title + "_" + str(numTickets + ("_" * (3 - len(str(numTickets))))) + "_" + str(titlePrice + ("_" * (6 - len(str(titlePrice)))))
                f = open("daily_transaction_file.txt", "a") 
                f.write(transaction) 
                print("Transaction Confirmed")
                doStuff = 0
            else:
                print("Transaction Cancelled")

    def sell(self, title, numTickets, price):
        if(price > 999.99):
            raise ValueError("Sell Price cannot exceed $999.99")
        if(len(title) > 25):
            raise ValueError("Event Title cannot exceed 25 characters")
        eventQuery ={"events", title}
        if(not len(collection.find_one(eventQuery) == 1)):
            raise ValueError("Event name already used")
        if(numTickets > 100):
           raise ValueError("Event cannot have more than 100 tickets")
        #do stuff
        #add to transaction file NOTE: since the event cant sell tickets until after the seller user logs off i think it might be best if we run a routine right before logging out that then adds the event
        transaction = "03" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + title + "_" + str(numTickets + ("_" * (3 - len(str(numTickets))))) + "_" + str(titlePrice + ("_" * (6 - len(str(titlePrice)))))
        f = open("daily_transaction_file.txt", "a") 
        f.write(transaction) 
        print("Event Created - " +"Event Name: " +title +"Ticket Price: " +price +" Number of tickets to be sold: " +numTickets)

    def deleteUser(username):
        """
        Deletes user from database
        """

        #delete the user from the database 
        collection.delete_one({"username": username})

        #add this transaction to the daily transaction file 
        transaction = "02" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + self.typeShort + "_" + str(self.credit + ("_" * (9 - len(str(self.credit)))))
        f = open("daily_transaction_file.txt", "a") 
        f.write(transaction) 

    def deleteTicket(ticket):
        """
        Delete a ticket from the DB 
        """
        pass 

    #def refund(self, buyName, sellName, amount):
     #   return 0

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
            sellerUser = getUser(seller)
            buyerUser = getUser(buyer)
            #Make appropriate changes to each respective users' accounts 
            if(buyerUser.getCredit() + credit <= 999999):
                #Check if transaction will cause seller to exceed maximum credit limit 
                sellerQuery = {"username:", sellerUser} ##NOTE:COMPARE THIS
                sellerCredit = { "$set": {
                    "credit": sellerUser.getCredit() - credit
                }}
                buyerCredit = { "$set": {
                    "credit": buyerSeller.getCredit() + credit ##NOTE:COMPARE THIS
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
                transaction = '06' + "_" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + self.typeShort + "_" + str(self.credit + ("_" * (9 - len(str(self.credit)))))
                f = open("daily_transaction_file.txt", "a") 
                f.write(transaction) 
            else:
                raise ValueError("Exceeds credit limit")
        else:
            raise ValueError("Value must be greater than zero")
