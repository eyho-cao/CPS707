from user import User
import pymongo 

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
            print("Invalid Seller");
        eventQResult = eventCollection.find_one(eventQuery)
        if(not len(eventQResult == 1)):
            print("Invalid Title");
        remainingTick = eventQResult.get('quantity')-numTickets #get number of tickets left in event
        titlePrice = eventQResult.get('price')
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
                doStuff = 0
            else:
                print("Transaction Cancelled")
