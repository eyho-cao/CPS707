import user

class SSUser(User):
    def sell(self, title, price, numTickets):
        """
        check price is <= 999.99
        check even title is of length <=25
        check max ticket <= 100
        ticket must not begin selling until after user logs out
        """
        if(price > 999.99):
            print("Sell Price cannot exceed $999.99")
        if(len(title) > 25):
            print("Event Title cannot exceed 25 characters")
        if(numTickets > 100):
           print("Event cannot have more than 100 tickets")
        #do stuff
        #add to transaction file NOTE: since the event cant sell tickets until after the seller user logs off i think it might be best if we run a routine right before logging out when then adds the event
        print("Event Created - " +"Event Name: " +title +"Ticket Price: " +price +" Number of tickets to be sold: " +numTickets)
