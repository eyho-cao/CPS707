import pymongo 
import datetime
from user import User


# initialize connection to mongoDB 

client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["events"]
users = db["users"]



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

class Event(): 
    
    def __init__(self, name, price, quantity, date, time, owner): 
        """
        Constructor for Ticket objects 

        name: name of event
        price: price per ticket of event
        quantity: tickets available
        date: date of event, format date like this: YYYY/MM/DD
        time: time of event on date, format time like this:  HH:MM(AM/PM) or HH:MM in 24hr notation 
        """

        query = {"name": name}
        result = collection.find_one(query)

        #Check for validity of inputs 
        if(result == None):
            if(price > 0):
                if(quantity > 0):
                    if(isValidDate(date)):
                        if(findUser(owner)):
                            self.name = name 
                            self.price = price
                            self.quantity = quantity
                            if("AM" in time.upper() or "PM" in time.upper()): time = formatTime(time)
                            self.dateTime = formatDate(date, time) 
                            self.owner = owner
                            

                            #add the user to the database
                            event = {
                                "name": self.name,
                                "price": self.price,
                                "quantity": self.quantity,
                                "datetime": self.dateTime,
                                "owner": self.owner
                            }

                            collection.insert_one(event)

                            #add this transaction to an output file... 
                        else:
                            raise ValueError("The owner does not exist")
                    else:
                        raise ValueError("The date entered is not valid")
                else:
                    raise ValueError("The quantity cannot be less than zero")
            else:
                raise ValueError("The price is invalid")
        else:
            raise ValueError("An event of the same name already exists")

    def getName(self):
        """
        Return name of event
        """
        return self.name 

    def getPrice(self):
        """
        Return price of event
        """
        return self.price

    def getQuantity(self):
        """
        Return quantity of tickets available for event
        """
        return self.quantity

    def getDateTime(self):
        """
        Return DateTime object related to the event 
        """
        return self.date

    def sellTicket(self, amount):
        """
        Decreases quantity by amount sold 
        """
        self.quantity -= amount
        
        query = {"name", self.name}
        update = { "$set": {
            "quantity": self.quantity
        }}

        collection.update_one(query, update)
    
    def returnTicket(self, amount):
        """
        Add quantity of tickets 
        """
        self.quantity += amount 

        query = {"name", self.name}
        update = { "$set": {
            "quantity": self.quantity
        }}

        collection.update_one(query, update)

    
