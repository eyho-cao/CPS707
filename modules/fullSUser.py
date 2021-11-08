from user import User
from event import Event
import pymongo 


client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]
eventCollection = db["events"]

class FSUser(User):
    def sell(self, title, numTickets, price):
        """
        create new event to sell
        """
        eventObj = Event.getEvent(title)
        if(eventObj != None):
            raise ValueError("ERROR: FSUser sell: Event name already used!")
        if(price > 999.99):
            raise ValueError("ERROR: FSUser sell: Sell Price cannot exceed $999.99")
        if(price < 0):
            raise ValueError("ERROR: FSUser sell: Sell Price cannot be a negative number")
        if(len(title) > 25):
            raise ValueError("ERROR: FSUser sell: Event Title cannot exceed 25 characters")
        if(numTickets > 100):
           raise ValueError("ERROR: FSUser sell: Event cannot have more than 100 tickets")
        if(numTickets < 0):
            raise ValueError("ERROR: FSUser sell: Event cannot have a negative number of tickets")

        #format of vars for list: [title, numtickets, price]
        self.appendEvent([title, numTickets, price])
        transaction = "03 " + str(self.getUsername() + (" " * (15 - len(self.getUsername())))) + " " + str(title + (" " * (25 - len(title)))) + " " + ("0" * (3 - len(str(numTickets))) + str(str(numTickets))) + " " + str(("0" * (6 - len(str(price)))) + str(price)) +"\n"
        f = open("daily_transaction_file_" +str(self.getUsername()) +".txt", "a") 
        f.write(transaction) 
        f.close()
        print("Event Created - " +"Event Name: " +title +" Ticket Price: " +str(price) +" Number of tickets to be sold: " +str(numTickets))

    def buy(self, title, numTickets, sellName):
        sellerQuery = {"username:": sellName}
        eventQuery = {"events": title}
        sellObj = User.getUser(self, sellName)
        if(sellObj is None):
            raise ValueError("ERROR: FSUser buy: Invalid Seller")

        event = Event(title)

        if(event is None):
            raise ValueError("ERROR: FSUser buy: Invalid Title")

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
                    f = open("daily_transaction_file_" +str(self.getUsername()) +".txt", "a") 
                    f.write(transaction) 
                    f.close()
                    print("Transaction Confirmed")
                else:
                    print("Transaction Cancelled")
        else:
            raise ValueError("ERROR: FSUser buy: Cannot buy more than 4 tickets at a time")
