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
        sellerQuery = {"username:", sellName}
        eventQuery = {"events", title}
        if(not len(collection.find_one(sellerQuery) == 1)):
            raise ValueError("Invalid Seller");
        event = getEvent(title)
        if(None):
            raise ValueError("Invalid Title");
        remainingTick = event.getQuantity()-numTickets #get number of tickets left in event ##NOTE: IM NOT SURE IF THIS IS HOW ITS ACTUALLY DONE
        titlePrice = event.price('price')
        if(numTickets < 4):
            if(remainingTick >=0):
                print("Price per Ticket: " +titlePrice +"\nTotal Price: " +titlePrice*numTickets)
                userInput = input("Confirm Transaction Y/N")
                if(userInput == "Y" or userInput == "yes" or userInput == "Yes"):
                    ticketsLeft = { "$set": {
                        "quantity": remainingTick
                    }}

                    eventCollection.update_one(eventQuery, remainingTick)
                    transaction = "04" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + title + "_" + str(str(numTickets) + ("_" * (3 - len(str(numTickets))))) + "_" + str(str(titlePrice) + ("_" * (6 - len(str(titlePrice)))))+"\n"

                    f = open("daily_transaction_file.txt", "a") 
                    f.write(transaction) 
                    print("Transaction Confirmed")
                else:
                    print("Transaction Cancelled")
        else:
            raise ValueError("Cannot buy more than 4 tickets at a time")
