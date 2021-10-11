import user

class AdminUser(User):
    def create(self, username, userType):
        if(len(username) > 25):
            print("Username must not exceed 25 character")
            """
            if(checkUnique(username)):
                match userType:
                    case 'admin':
                        #add admin account to database
                        #print("New Account Created - Username: " +"Username")
                    case 'full-standard':
                        #add FS account to db
                        #print("New Account Created - Username: " +"Username")
                    case 'buy-standard':
                        #add BS account to db
                        #print("New Account Created - Username: " +"Username")
                    case 'sell-standard':
                        #add SS account to db
                        #print("New Account Created - Username: " +"Username")
                    case _:
                        #print("Username already taken")
            else:
                print("username has been taken")
            """

    def buy(self, title, numTickets, sellName):
        #check if sellname exists
        #insert db check for sell name
        validSN = True
        validTitle = True
        titlePrice = 19.99
        if(not validSN):
            print("Invalid Seller");
        if(not validTitle):
            print("Invalid Title");
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
                doStuff = 0
            else:
                print("Transaction Cancelled")



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
        transaction = "03" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + title + "_" + str(numTickets + ("_" * (3 - len(str(numTickets))))) + "_" + str(titlePrice + ("_" * (6 - len(str(titlePrice)))))
        f = open("daily_transaction_file.txt", "a") 
        f.write(transaction) 
        print("Event Created - " +"Event Name: " +title +"Ticket Price: " +price +" Number of tickets to be sold: " +numTickets)

    def delete(self, username):
        userQuery = {"username:", username}
        if(not len(collection.find_one(buyerQuery) == 1)):
           raise ValueError("User not found")
        else:
            collection.delete_one(userQuery)
            print("User Removed")
            #add this transaction to the daily transaction file 
            transaction = "02" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + self.typeShort + "_" + str(self.credit + ("_" * (9 - len(str(self.credit)))))
            f = open("daily_transaction_file.txt", "a") 
            f.write(transaction) 

    def refund(self, buyer, seller, amount):
        """
        Issue a refund from self (seller) to other (buyer) of amount credit 
        """

        #Check if other user exists 
        buyerQuery = {"username:", buyer.username}
        sellerQuery = {"username:", seller.username}
        if(len(collection.find_one(buyerQuery) == 1) and credit > 0 and len(collection.find_one(sellerQuery) == 1)):
            #Make appropriate changes to each respective users' accounts 
            if(self.credit + amount > 999999):
                #Check if transaction will cause seller to exceed maximum credit limit 
                sellerCredit = { "$set": {
                    "credit": seller.credit + amount
                }}
                buyerCredit = { "$set": {
                    "credit": seller.credit - amount
                }}
                collection.update_one(buyerQuery, buyerCredit)
                collection.update_one(sellerQuery, sellerCredit)
                transaction = "05" + str(buyer.username + ("_" * (15 - len(buyer.username)))) + "_" + seller.username + ("_" * (15 - len(seller.username)))) + "_" + str(amount + ("_" * (9 - len(str(amount)))))
                f = open("daily_transaction_file.txt", "a") 
                f.write(transaction) 
            else:
                raise ValueError("Seller is over credit limit")
        elif(len(collection.find_one(buyerQuery) == 0)):
            raise ValueError("Buyer does not exist")
        elif(len(collection.find_one(sellerQuery) == 0)):
             raise ValueError("Seller does not exist")
        elif(credit < 0):
            raise ValueError("Invalid value for credit")

    def addCredit(self, user, credit):
            """
            Add credit to user's account 
            """
            userQuery = {"username": user}
            if(len(collection.find_one(buyerQuery) == 1)):
                if(credit > 0):
                    if(user.credit + credit > 999999):
                        #update credit in database
                        user.credit += credit 
                        query = {"username:", user}
                        newCredit = { "$set": {
                            "credit": user.credit + credit
                        }}
                        collection.update_one(query, newCredit)

                        #add the transaction to the daily transaction file 
                        transaction = '06' + "_" + str(user + ("_" * (15 - len(user)))) + "_" + user.typeShort + "_" + str(user.credit + ("_" * (9 - len(str(user.credit)))))
                        f = open("daily_transaction_file.txt", "a") 
                        f.write(transaction) 
                    else:
                        raise ValueError("Exceeds credit limit")
                else:
                    raise ValueError("Value must be greater than zero")
            else:
                raise ValueError("User not found")

    def checkUnique(username):
        query = {"username": username} 
        result = collection.find(query) 
        if(len(result) == 0):
            return True
        else:
            return False

    def uniqueTitle(title):
        query = {"eventName": title} 
        result = collection.find(query) 
        if(len(result) == 0):
            return True
        else:
            return False