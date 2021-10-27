import unittest 
import pymongo
from user import User
from fullSUser import FSUser

client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]

class TestFSUser(unittest.TestCase):
    
    def setUp(self):
        """
        setUp(self) is a function that runs before every test case, 
        in this case I wanted to make a new user everytime 
        """
        self.fullSUser = FSUser("oldboy")

    def tearDown(self):
        """
        tearDown(self) is a function that runs after every test case,
        in this case I wanted to delete the user from setUp()

        not required, but just fyi 
        """
        pass 

    def test_str(self):
        """
        self.assertEqual(x,y) returns true, and is considered a passed test if 
        x == y

        should compare what you get from methods, vs what you expect to get 
        """

        self.assertEqual(
            str(self.fullSUser),
            "User(username=oldboy, type=AA, credit=0)"
        )

    def test_get_user(self):
        tempUser = self.fullSUser.getUser('trinh')
        self.assertEqual(
            str(tempUser),
            "User(username=trinh, type=AA, credit=5000)"
        )

    def test_get_username(self):
        self.assertEqual(
            self.fullSUser.getUsername(), 
            'oldboy'
        )

    def test_get_credit(self):
        self.assertEqual(
            self.fullSUser.getCredit(), 
            0
        )

    def test_get_type(self):
        self.assertEqual(
            self.fullSUser.getType(),
            "AA"
        )

    def test_sell_invalid_price(self):
        """
        this test passes if a ValueError is returned after giving an invalid ticket price
        """
        try:
            self.fullSUser.sell("Among Us: The Movie", 2, 1000)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)

    def test_sell_invalid_title(self):
        """
        this test passes if a ValueError is returned after giving an invalid ticket title
        """
        try:
            self.fullSUser.sell("Among Us 2: The Sequel to Among Us: The Movie", 2, 20)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)

    def test_sell_invalid_numTickets(self):
        """
        this test passes if a ValueError is returned after giving an invalid number of tickets
        """
        try:
            self.fullSUser.sell("Among Us: The Movie", 101, 15)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)

    def test_sell_success(self):
        """
        this test passes if all passed arguements are valid
        """
        result = self.fullSUser.sell("Among Us: The Movie", 2, 20)
        self.assertEqual(result, "03 oldboy__________Among Us: The Movie_2___20____")

    def test_buy_invalid_numTickets(self):
        try:
            self.fullSUser.buy("Among Us: The Movie", 10, "trinh")

        except ValueError as e:
            self.assertEqual(type(e), ValueError)


    def test_buy_invalid_remainingTickets(self):
        try:
            self.fullSUser.buy("Among Us: The Movie", 10000, "trinh")
        except ValueError as e:
            self.assertEqual(type(e), ValueError)



if __name__ == '__main__':
    unittest.main()
