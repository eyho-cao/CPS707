import user

class FSUser(User):
    def sell(self, title, price, numTickets):
        """
        check price is <= 999.99
        check even title is of length <=25
        check max ticket <= 100
        ticket must not begin selling until after user logs out
        """
        if(price > 999.99):
            raise ValueError("Sell Price cannot exceed $999.99")
        if(len(title) > 25):
            raise ValueError("Event Title cannot exceed 25 characters")
        if(not uniqueTitle(title)):
            raise ValueError("Event name already used")
        if(numTickets > 100):
           raise ValueError("Event cannot have more than 100 tickets")
        #do stuff
        #add to transaction file NOTE: since the event cant sell tickets until after the seller user logs off i think it might be best if we run a routine right before logging out that then adds the event
        print("Event Created - " +"Event Name: " +title +"Ticket Price: " +price +" Number of tickets to be sold: " +numTickets)
        transaction = "03" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + title + "_" + str(numTickets + ("_" * (3 - len(str(numTickets))))) + "_" + str(titlePrice + ("_" * (6 - len(str(titlePrice)))))
        f = open("daily_transaction_file.txt", "a") 
        f.write(transaction) 
        print("Transaction Confirmed")


    def buy(self, title, numTickets, sellName):
        #check if sellname exists
        #insert db check for sell name
        validSN = True
        validTitle = True
        titlePrice = 19.99
        if(not validSN):
            raise ValueError("Invalid Seller");
        if(not validTitle):
            raise ValueError("Invalid Title");
        if(numTickets > 4):
            raise ValueError("Number of tickets bought cannot exceed 4")
        remainingTick = 999-numTickets #999 needs to be replaced with remaining tickets from db
        if(remainingTick >=0):
            print("Price per Ticket: " +titlePrice +"\nTotal Price: " +titlePrice*numTickets)
            userInput = input("Confirm Transaction Y/N")
            #python has no switch case? switch case not implemented until 3.10
            if(userInput == "Y" or userInput == "yes" or userInput == "Yes"):
                #confirm transaction - decrease number of tickets from db - add to transaction line
                transaction = "04" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + title + "_" + str(numTickets + ("_" * (3 - len(str(numTickets))))) + "_" + str(titlePrice + ("_" * (6 - len(str(titlePrice)))))
                f = open("daily_transaction_file.txt", "a") 
                f.write(transaction) 
                print("Transaction Confirmed")
            else:
                print("Transaction Cancelled")




    def uniqueTitle(title):
        query = {"eventName": title} 
        result = collection.find(query) 
        if(len(result) == 0):
            return True
        else:
            return False