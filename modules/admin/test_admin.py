import unittest 
import pymongo
import sys
sys.path.insert(1, '../')
from admin import Admin

client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]


class TestAdmin(unittest.TestCase):
    obj = Admin()

    def setUp(self):
        """
        setUp(self) is a function that runs before every test case, 
        in this case I wanted to make a new user everytime 
        """
        self.user = obj.User("oldboy")
    
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
            str(self.user),
            "User(username=oldboy, type=AA, credit=0)"
        )

    def test_get_user(self):
        tempUser = self.user.getUser('trinh')
        self.assertEqual(
            str(tempUser),
            "User(username=trinh, type=AA, credit=5000)"
        )

    def test_get_username(self):
        self.assertEqual(
            self.user.getUsername(), 
            'oldboy'
        )

    def test_get_credit(self):
        self.assertEqual(
            self.user.getCredit(), 
            0
        )

    def test_get_type(self):
        self.assertEqual(
            self.user.getType(),
            "AA"
        )

    def test_create_valid_admin(self):
        adminUser= "adminTest"
        self.createUser(adminUser, admin)
        self.assertEqual(true, true)
if __name__ == '__main__':
    unittest.main()
