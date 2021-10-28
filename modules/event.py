import pymongo 
import datetime


# initialize connection to mongoDB 

client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["events"]
users = db["users"]




class Event(): 
    
    def __init__(self, name): 
        """
        Constructor for Ticket objects 
        """

        query = {"name": name} 
        result = collection.find_one(query) 
        
        if(result):
            self.name = name
            self.price = result.get('price')
            self.quantity = result.get('quantity')
            self.dateTime = result.get('date')
            self.owner = result.get('owner')
        else:
            raise ValueError("Event does not exist")


    def getName(self):
        """
        Return name of event
        """
        return self.name 

    def setName(self, name):
        self.name = name

    def getPrice(self):
        """
        Return price of event
        """
        return self.price

    def setPrice(self, price):
        self.price = price

    def getQuantity(self):
        """
        Return quantity of tickets available for event
        """
        return self.quantity

    def setQuantity(self, quantity):
        self.quantity = quantity

    def getDateTime(self):
        """
        Return DateTime object related to the event 
        """
        return self.dateTime

    def sellTicket(self, amount):
        """
        Decreases quantity by amount sold 
        """
        self.quantity -= amount
        
        query = {"name": self.name}
        update = { "$set": {
            "quantity": self.quantity
        }}

        collection.update_one(query, update)
    
    def returnTicket(self, amount):
        """
        Add quantity of tickets 
        """
        self.quantity += amount 

        query = {"name": self.name}
        update = { "$set": {
            "quantity": self.quantity
        }}

        collection.update_one(query, update)

    def getEvent(eventName):
        """
        Return Event object based on unique event name
        """
        query = {"events:": eventName}
        result = collection.find_one(query)
        if(result):
            event = Event(result.get('name'))
            return event
        return None

    def __str__(self): 
        """
        String method 
        """
        return  f'Event(name={self.name}, price={self.price}, quantity={self.quantity}, dateTime={self.dateTime}, owner={self.owner})'

    
