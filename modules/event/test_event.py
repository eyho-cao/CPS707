import unittest 
import datetime
import pymongo
from event import Event

client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["events"]


class TestEvent(unittest.TestCase):

    def setUp(self):

        self.event = Event('The Rumble in the Jungle')

    def tearDown(self):
        """
        After every test, restore to default 
        """

        query = {"name": 'The Rumble in the Jungle'}
        update = {
            "$set":{
                "quantity": 50
            }
        }
        collection.update_one(query, update)

    def test_get_name(self):

        self.assertEqual(
            self.event.getName(),
            "The Rumble in the Jungle"
        )

    def test_get_price(self):

        self.assertEqual(
            self.event.getPrice(),
            5000
        )

    def test_get_quantity(self):

        self.assertEqual(
            self.event.getQuantity(), 
            50 
        )

    def test_get_datetime(self):

        self.assertEqual(
            self.event.getDateTime(),
            datetime.datetime(1974,10,30,5)
        )

    def test_sell_ticket(self):

        self.event.sellTicket(25)


        self.assertEqual(
            self.event.getQuantity(),
            25
        )

    def test_return_ticket(self):
        
        self.event.returnTicket(25)

        self.assertEqual(
            self.event.getQuantity(),
            75
        )

    def test_str(self):

        self.assertEqual(
            str(self.event),
            "Event(name=The Rumble in the Jungle, price=5000.0, quantity=50, dateTime=1974-10-30 05:00:00, owner=trinh)"
        )


if __name__ == '__main__':
    unittest.main()