from user import User
from event import Event
import pymongo 


client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]
eventCollection = db["events"]

class FSUser(User):
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
        transaction = "03" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + title + "_" + str(str(numTickets) + ("_" * (3 - len(str(numTickets))))) + "_" + str(str(titlePrice) + ("_" * (6 - len(str(titlePrice)))))
        f = open("daily_transaction_file.txt", "a") 
        f.write(transaction) 
        print("Event Created - " +"Event Name: " +title +" Ticket Price: " +price +" Number of tickets to be sold: " +numTickets)


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
                    transaction = "04" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + title + "_" + str(str(numTickets) + ("_" * (3 - len(str(numTickets))))) + "_" + str(str(titlePrice) + ("_" * (6 - len(str(titlePrice)))))
                    f = open("daily_transaction_file.txt", "a") 
                    f.write(transaction) 
                    print("Transaction Confirmed")
                else:
                    print("Transaction Cancelled")
        else:
            raise ValueError("Cannot buy more than 4 tickets at a time")
