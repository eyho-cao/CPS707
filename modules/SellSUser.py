from user import User
from event import Event

import pymongo


client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]
eventCollection = db["events"]

class SSUser(User):
    def sell(self, title, numTickets, price):
        """
        create new event to sell
        """
        eventObj = Event.getEvent(title)
        if(eventObj != None):
            raise ValueError("ERROR: SSUser sell: Event name already used!")
        if(price > 999.99):
            raise ValueError("ERROR: SSUser sell: Sell Price cannot exceed $999.99")
        if(price < 0):
            raise ValueError("ERROR: SSUser sell: Sell Price cannot be a negative number")
        if(len(title) > 25):
            raise ValueError("ERROR: SSUser sell: Event Title cannot exceed 25 characters")
        if(numTickets > 100):
           raise ValueError("ERROR: SSUser sell: Event cannot have more than 100 tickets")
        if(numTickets < 0):
            raise ValueError("ERROR: SSUser sell: Event cannot have a negative number of tickets")

        #format of vars for list: [title, numtickets, price]
        self.appendEvent([title, numTickets, price])
        transaction = "03 " + str(self.getUsername() + (" " * (15 - len(self.getUsername())))) + " " + str(title + (" " * (25 - len(title)))) + " " + ("0" * (3 - len(str(numTickets))) + str(str(numTickets))) + " " + str(("0" * (6 - len(str(price)))) + str(price)) +"\n"
        f = open("daily_transaction_file_" +str(self.getUsername()) +".txt", "a") 
        f.write(transaction) 
        f.close()
        print("Event Created - " +"Event Name: " +title +" Ticket Price: " +str(price) +" Number of tickets to be sold: " +str(numTickets))
