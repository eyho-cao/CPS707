import pymongo
from datetime import datetime

# initialize connection to mongoDB 

client = pymongo.MongoClient("mongodb+srv://trinh:mvh5sYgCX1pXo08y@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]
eventCollection = db["events"]

class User():
    def __init__(self, username): 
        """
        Constructor for User object 
        Default credit value to zero, unless other value is specified 
        """


        #check if the username is unique
        query = {"username": username} 
        result = collection.find_one(query) 
        #check if usename exceeds character limit 
        
        if(result != None):
            self.username = username
            self.type = result.get('type')
            self.credit = result.get('credit')
            self.newEventList = []
        else:
            raise ValueError("ERROR: User __init_:User does not exist")

    def __str__(self):
        """
        string formatting for instances of User object
        u = User('trinh','admin')
        print(u)
        >>> User(username='trinh', type='AA', credit=0)
        """
        return f'User(username={self.username}, type={self.type}, credit={self.credit})'

    def __repr__(self):
        return f'User(username={self.username}, type={self.type}, credit={self.credit})'

    def getUser(self, username):
        """
        Return User object based on unique username
        """
        query = {"username": username}
        result = collection.find_one(query)
        if(result is not None):
            user = User(result.get('username'))
        
            return user
        else:
            return None

    def getUsername(self):
        """
        Return a User instance's username 
        """
        return self.username

    def addCredit(self, credit):
        """
        #delete the user from the database 
        collection.delete_one({"username": self.username})
        #add this transaction to the daily transaction file 
        transaction = "02" + str(self.username + ("_" * (15 - len(self.username)))) + "_" + self.type + "_" + str(str(self.credit) + ("_" * (9 - len(str(self.credit)))))
        f = open("daily_transaction_file.txt", "a") 
        f.write(transaction) 
        """
        if(credit >= 0):
            if(self.getCredit() + credit <= 999999):
                #update credit in database
                balance = self.getCredit() + credit 
                query = {"username:": self.getUsername()}
                newCredit = { "$set": {
                    "credit": balance
                }}
                collection.update_one(query, newCredit)

                #add the transaction to the daily transaction file 
                transaction = '06' + " " + str(self.getUsername()) + " " + self.getType() + " " + str(str(self.credit+credit))+"\n"
                f = open("daily_transaction_file.txt", "a") 
                f.write(transaction) 
                f.close()
            else:
                raise ValueError("ERROR: User addCredit: Exceeds credit limit")
        else:
            raise ValueError("ERROR: User addCredit: Value must be greater than zero")

    def appendEvent(self, event):
        """
        append new event object to newEventList
        """
        self.newEventList.append(event)

    def getEventList(self):
        """
        return newEventList object
        """
        return self.newEventList

    def addEventsDB(self):
        """
        add stored events to DB
        """
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        date = now.date()
        for i in self.newEventList:
            self.createEvent(str(i[0]), float(i[1]), float(i[2]), date, time)

    def createEvent(self, name, price, quantity, date, time):
        """
        insert Event in DB
        """
        query = {"name": name}
        result = collection.find_one(query)
        owner = self.getUsername()
        #Check for validity of inputs 
        if(result == None):
            if(price > 0):
                if(quantity > 0):
                #if(isValidDate(date)):
                    if(self):
                            
                        #if("AM" in time.upper() or "PM" in time.upper()): time = formatTime(time)
                        #dateTime = formatDate(date, time) 
                           
                            
                        #add the user to the database
                        event = {
                            "name": name,
                            "price": price,
                            "quantity": quantity,
                            #"datetime": dateTime,
                            "date" : datetime.now(),
                            "owner": self.getUsername()
                        }

                        eventCollection.insert_one(event)
                    else:
                        raise ValueError("ERROR: User createEvent: The owner does not exist")
                #else:
                 #   raise ValueError("ERROR: User createEvent: The date entered is not valid")
                else:
                    raise ValueError("ERROR: User createEvent: The quantity cannot be less than zero")
            else:
                raise ValueError("ERROR: User createEvent: The price is invalid")
        else:
            raise ValueError("ERROR: User createEvent: An event of the same name already exists")

    def getCredit(self):
        """
        Return a User instance's credit 
        """
        return self.credit

    def getType(self):
        """
        Return a User instance's type
        """
        return self.type

    def logout(self): 
        """
        Logout of current session
        """
        """
        #Set user's status to offline in db 
        if(self.status == "online"):
            query = {"username:", self.username}
            newCredit = { "$set": {
            "status": "offline"
            }}
            collection.update_one(query, newCredit)
        else:
            raise ValueError('User status error')
        """

        #add the transaction to the daily transaction file 
        transaction = '00' + " " + str(self.username) + " " + self.type + " " + str(str(self.credit))+"\n"
        f = open("daily_transaction_file.txt", "a") 
        f.write(transaction) 
        f.close()

    def refund(self, seller, buyer, credit):
        raise ValueError("ERROR: User refund: Insufficient Permissions")

    def createUser(self, username, userType, credit=0):
        raise ValueError("ERROR: User refund: Insufficient Permissions")

    def sell(self, title, price, numTickets):
        raise ValueError("ERROR: User refund: Insufficient Permissions")

    def buy(self, title, numTickets, seller):
        raise ValueError("ERROR: User refund: Insufficient Permissions")

    def deleteUser(self, username):
        raise ValueError("ERROR: User refund: Insufficient Permissions")

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