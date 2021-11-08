from user import User
from event import Event
import pymongo 


client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]
eventCollection = db["events"]

class BSUser(User):
    """
    Check if sellname exists
        else throw error
    check if sellName has title
        else throw error
    Check if numTickets <= 4
        else deny transaction
    check how many tickets remaining and if can sell numTickets to user
        else throw error
    display $/ticket
    display total $
    ask for confirmation of transaction
    wait for response
    decrease num ticket if user buys
    """
    def buy(self, title, numTickets, sellName):
        """
        buy tickets
        """
        sellerQuery = {"username:": sellName}
        eventQuery = {"events": title}
        sellObj = User.getUser(self, sellName)
        if(sellObj is None):
            raise ValueError("ERROR: BSUser buy: Invalid Seller")

        event = Event(title)

        if(event is None):
            raise ValueError("ERROR: BSUser buy: Invalid Title")

        if(numTickets < 4):
            remainingTick = event.getQuantity()-numTickets #get number of tickets left in event ##NOTE: IM NOT SURE IF THIS IS HOW ITS ACTUALLY DONE
            titlePrice = event.getPrice()
            if(remainingTick >=0):
                print("Price per Ticket: " +str(titlePrice) +"\nTotal Price: " +str(titlePrice*numTickets))
                userInput = input("Confirm Transaction Y/N")
                if(userInput == "Y" or userInput == "yes" or userInput == "Yes" or userInput == "y"):
                    ticketsLeft = { "$set": {
                        "quantity": remainingTick
                    }}

                    eventCollection.update_one(eventQuery, ticketsLeft)
                    transaction = "04 " + str(self.username + (" " * (15 - len(self.username)))) + " " + str(title + (" " * (19 - len(title)))) + " " + ("0" * (3 - len(str(numTickets))) + str(str(numTickets))) + " " + str(("0" * (6 - len(str(titlePrice)))) + str(titlePrice)) +"\n"
                    f = open("daily_transaction_file " +self.getUsername() +".txt", "a") 
                    f.write(transaction) 
                    f.close()
                    print("Transaction Confirmed")
                else:
                    print("Transaction Cancelled")
        else:
            raise ValueError("ERROR: BSUser buy: Cannot buy more than 4 tickets at a time")
