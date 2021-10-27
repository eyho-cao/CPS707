from user import User
from event import Event

import pymongo


client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]
eventCollection = db["events"]

class SSUser(User):
    def sell(self, title, numTickets, price):
        if(price > 999.99):
            raise ValueError("Sell Price cannot exceed $999.99")
        if(len(title) > 25):
            raise ValueError("Event Title cannot exceed 25 characters")
        eventQuery ={"events": title}
        if(not (len(eventCollection.find_one(eventQuery)) == 1)):
            raise ValueError("Event name already used")
        if(numTickets > 100):
           raise ValueError("Event cannot have more than 100 tickets")
        #do stuff
        #add to transaction file NOTE: since the event cant sell tickets until after the seller user logs off i think it might be best if we run a routine right before logging out that then adds the event
        transaction = "03 " + str(self.username + (" " * (15 - len(self.username)))) + " " + str(title + (" " * (19 - len(title)))) + " " + ("0" * (3 - len(str(numTickets))) + str(str(numTickets))) + " " + str(("0" * (6 - len(str(titlePrice)))) + str(titlePrice)) +"\n"
        f = open("daily_transaction_file.txt", "a") 
        f.write(transaction) 
        print("Event Created - " +"Event Name: " +title +"Ticket Price: " +price +" Number of tickets to be sold: " +numTickets)
