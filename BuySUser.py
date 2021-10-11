import user

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
                print("Transaction Confirmed")
                doStuff = 0
            else:
                print("Transaction Cancelled")