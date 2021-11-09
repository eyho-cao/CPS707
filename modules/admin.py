import sys
import pymongo
import os
import shutil
import glob
sys.path.insert(1,'../CPS707/modules')
from user import User
from event import Event
from datetime import date



# initialize connection to mongoDB 

client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]
eventCollection = db["events"]

class Admin(User):
    def createUser(self, username, type, credit=0):
        """
        Create a User object 
        Default credit value to zero, unless other value is specified 
        """
        if(len(username) > 25):
            raise ValueError("ERROR: Admin createUser: Username exceeds 25 character limit")

        query = {"username": username} 
        result = collection.find_one(query) 

        if(result == None):
            #Check if username is unique 
            if((type in ['AA', 'FS', 'BS', 'SS'])):
                #Check if type is valid
                if(credit >= 0 and credit < 999999):
                    #Check if credit is valid

                    #add the user to the database
                    user = {"username": username, "type": type, "credit": credit}
                    collection.insert_one(user) 
                    
                    #TODOOOOO
                    
                    #add this transaction to the daily transaction file 
                    transaction = "01 " + str(self.username) + " " + self.type + " " + str(str(self.credit))+"\n"
                    f = open("..\\modules\\TransactionFiles\\daily_transaction_file_" +str(self.getUsername()) +".txt", "a") 
                    f.write(transaction) 
                    f.close()
                    

                else:
                    raise ValueError("ERROR: Admin createUser: Value for credit is not valid")
            else:
                raise ValueError("ERROR: Admin createUser: User type is invalid") 
        else:
            raise ValueError('ERROR: Admin createUser: Username is not unique')

    def buy(self, title, numTickets, sellName):
        sellerQuery = {"username:": sellName}
        eventQuery = {"events": title}
        sellObj = User.getUser(self, sellName)
        if(sellObj is None):
            raise ValueError("ERROR: Admin buy: Invalid Seller")

        event = Event(title)

        if(event is None):
            raise ValueError("ERROR: Admin buy: Invalid Title")

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
                f = open("..\\modules\\TransactionFiles\\daily_transaction_file_" +str(self.getUsername()) +".txt", "a") 
                f.write(transaction) 
                f.close()
                print("Transaction Confirmed")
            else:
                print("Transaction Cancelled")

    def sell(self, title, numTickets, price):
        """
        create new event to sell
        """
        eventObj = Event.getEvent(title)
        if(eventObj != None):
            raise ValueError("ERROR: Admin sell: Event name already used!")
        if(price > 999.99):
            raise ValueError("ERROR: Admin sell: Sell Price cannot exceed $999.99")
        if(price < 0):
            raise ValueError("ERROR: Admin sell: Sell Price cannot be a negative number")
        if(len(title) > 25):
            raise ValueError("ERROR: Admin sell: Event Title cannot exceed 25 characters")
        if(numTickets > 100):
            raise ValueError("ERROR: Admin sell: Event cannot have more than 100 tickets")
        if(numTickets < 0):
            raise ValueError("ERROR: Admin sell: Event cannot have a negative number of tickets")

        #format of vars for list: [title, numtickets, price]
        self.appendEvent([title, numTickets, price])
        transaction = "03 " + str(self.getUsername() + (" " * (15 - len(self.getUsername())))) + " " + str(title + (" " * (25 - len(title)))) + " " + ("0" * (3 - len(str(numTickets))) + str(str(numTickets))) + " " + str(("0" * (6 - len(str(price)))) + str(price)) +"\n"
        f = open("..\\modules\\TransactionFiles\\daily_transaction_file_" +str(self.getUsername()) +".txt", "a") 
        f.write(transaction) 
        f.close()
        print("Event Created - " +"Event Name: " +title +" Ticket Price: " +str(price) +" Number of tickets to be sold: " +str(numTickets))

    def deleteUser(self,username):
        """
        Deletes user from database
        """
        if(username == self.getUsername()):
            raise ValueError("ERROR: Admin deleteUser: Cannot delete, logged in as user")
        elif(User.getUser(self, username)):
            #delete the user from the database 
            collection.delete_one({"username": username})

            #add this transaction to the daily transaction file 
            transaction = "02 " + str(self.username) + " " + self.type + " " + str(str(self.credit)) +"\n"
            f = open("..\\modules\\TransactionFiles\\daily_transaction_file_" +str(self.getUsername()) +".txt", "a") 
            f.write(transaction)
            f.close()
        else:
            raise ValueError("ERROR: Admin deleteUser: User not found")

    def deleteTicket(ticket):
        """
        Delete a ticket from the DB 
        """
        pass

    def refund(self, buyer, seller, credit):
        buyerObj = Admin.getUser(self,buyer)
        sellerObj = Admin.getUser(self,seller)
        if(buyerObj is not None and sellerObj is not None and credit > 0):
            if(sellerObj.getCredit() - credit >= 0):
                if(buyerObj.getCredit() + credit < 999999):
                    #Check if transaction will cause seller to exceed maximum credit limit 
                    buyerQuery = {"username:": buyer}
                    sellerQuery = {"username:": self.username}
                    sellerCredit = { "$set": {
                        "credit": sellerObj.getCredit() - credit
                    }}
                    buyerCredit = { "$set": {
                        "credit": buyerObj.getCredit() + credit
                    }}
                    collection.update_one(buyerQuery, buyerCredit)
                    collection.update_one(sellerQuery, sellerCredit)
                    transaction = '05' + " " + buyer + " " + seller + " " + str(credit)+"\n"
                    f = open("..\\modules\\TransactionFiles\\daily_transaction_file_" +str(self.getUsername()) +".txt", "a") 
                    f.write(transaction)
                    f.close()
                else:
                    raise ValueError("ERROR: Admin refund: Seller is over credit limit")
            else:
                raise ValueError("ERROR: Admin refund: Seller does not have sufficient funds")
        elif(buyerObj is None):
            raise ValueError("ERROR: Admin refund: Buyer does not exist")
        elif(sellerObj is None):
            raise ValueError("ERROR: Admin refund: Seller does not exist")
        elif(credit < 0):
            raise ValueError("ERROR: Admin refund: Invalid value for credit")


       
    def addCredit(self, username, credit):
        """
        Add credit to user's account 
        """

        user = self.getUser(username)
        if(user is None):
            raise ValueError("ERROR: Admin addCredit: Username Not Found")

        if(credit >= 0):
            if(user.getCredit() + credit <= 999999):
                #update credit in database
                balance = user.getCredit() + credit 
                query = {"username:": user.getUsername()}
                newCredit = { "$set": {
                    "credit": balance
                }}
                collection.update_one(query, newCredit)

                #add the transaction to the daily transaction file 
                transaction = '06' + " " + str(user.getUsername()) + " " + user.getType() + " " + str(user.getCredit()+credit)+"\n"
                f = open("..\\modules\\TransactionFiles\\daily_transaction_file_" +str(self.getUsername()) +".txt", "a") 
                f.write(transaction) 
                f.close()
            else:
                raise ValueError("ERROR: Admin addCredit: Exceeds credit limit")
        else:
            raise ValueError("ERROR: Admin addCredit: Value must be greater than zero")

    def updateCurrentUsers(self):
        """
        Updates current_users.txt, the current users file 
        """

        f = open('../files/current_users.txt', "w")

        for user in collection.find(): 
            line = user.get("username") + " " + user.get("type") + " " + str(user.get("credit")) + "\n"
            f.write(line)

        f.write("END")
        f.close() 

    def updateAvailableTickets(self):
        """
        updates the avaible tickets file 
        """

        f = open('../files/available_tickets.txt', "w") 

        for event in eventCollection.find():
            line = event.get("name") + " " + event.get("owner") + " " + str(event.get("quantity")) + " " + str(event.get("price")) + "\n"
            f.write(line)
        
        f.write("END")
        f.close()


    def endDay(self):
        self.updateCurrentUsers()
        self.updateAvailableTickets()
        self.transFileEOD()
        print("-----------------------------\nDay Closed - User and Ticket files updated - Daily Transaction files merged\nFind merged file in 'MergedDailyTransactionFiles' folder\n-----------------------------")

    def transFileEOD(self):
        today = date.today()
        day = today.strftime("%b-%d-%Y")
        file = "..\\modules\\MergedDailyTransactionFiles\\daily_transaction_file_" +str(day) +".txt"
        if(os.path.isfile(file)):
            os.remove(file)
        #merge transaction files
        self.dailyTransMerge(file)
        #purge old transaction files
        self.purgetransFiles()
    
    def dailyTransMerge(self, file):
        transFilespath = "..\\modules\\TransactionFiles"
        with open(file, 'wb') as outfile:
            for filename in glob.glob(transFilespath +'\\*.txt'):
                with open(filename, 'rb') as readfile:
                    shutil.copyfileobj(readfile, outfile)
        f = open(file, "a")
        f.write("00")
        f.close()
    def purgetransFiles(self):
        transFilespath = "..\\modules\\TransactionFiles"
        for filename in glob.glob(transFilespath +'\\*.txt'):
            os.remove(filename)



#--------- HELPER FUNCTIONS ---------# 
def isValidDate(date):
    """
    Checks if a date, date, is valid 
    A valid date for an event will be past today's date 
    It will also follow date conventions 
    I.E. February 31st, 20__ is not a valid date 
    """

    var = date.split("/") 
    today = str(datetime.datetime.now())[:10].split('-')

    if(var[0] >= today[0]):
        #check years 
        if(var[1] >= today[1] and var[1] >= 1 and var[1] <= 12):
            #check months 
            if(var[2] >= today[2]):
                #check days
                if(var[1] in ['01','03','05','07','08','10','12']):
                    if(var[2] <= '31'):
                        return True 
                elif(var[1] in ['04', '06', '09','11']):
                    if(var[2] <= '30'):
                        return True 
                elif(var[1] == '2'):
                    if(var[0] % 4 == 0 and var[2] <= '29'):
                        #handles leap years 
                        return True 
                    if(var[2] <= '28'):
                        return True 
    return False 

def formatTime(time):
    """
    Formats time into 24hr time 
    """

    ampm = time[:-3:-1][::-1]
    _time = time.replace(" ","")
    
    if(ampm == 'am'):
        return [int(_time[:-5]), int(time[-4:-2])]
    else:
        return [int(_time[:-5]) + 12, int(time[-4:-2])]

def formatDate(date, time):
    """
    Formats a string representation of a date in the form "YYYY/MMM/DD" 
    into a datetime object 
    """

    _date = date.split("/")
    _time = formatTime(time)
    return datetime.datetime(int(_date[0]), int(_date[1]), int(_date[2]), _time[0], _time[1])

def findUser(username):
    """
    Check if a user with username exists
    """
    query = {"username": username}
    
    return collection.find_one(query)
