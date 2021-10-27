import unittest 
import pymongo
import os
import filecmp
import sys
sys.path.insert(1, '../')
from admin import Admin

client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]


class TestAdmin(unittest.TestCase):

    def setUp(self):
        """
        setUp(self) is a function that runs before every test case, 
        in this case I wanted to make a new user everytime 
        """
        self.user = Admin("oldboy")
    
    def tearDown(self):
        """
        tearDown(self) is a function that runs after every test case,
        in this case I wanted to delete the user from setUp()
        if()
        not required, but just fyi 
        """
        if(os.path.exists('./daily_transaction_file.txt')):
            os.remove("daily_transaction_file.txt")
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

    def test_addcredit_admin_valid(self):
        self.user.addCredit("billy", 20)
        self.user.logout()
        testf = "C:/Users/Eyho Cao/Documents/GitHub/CPS707/modules/admin/daily_transaction_file.txt"
        expectedf = "../ExpectedOutput/addcredit_admin_valid.txt"
        self.assertTrue(filecmp.cmp(testf, expectedf))
    def test_create_valid_admin(self):
        adminUser= "adminTest"
        self.user.createUser(adminUser, "AA")
        self.user.logout()
        testf = "C:/Users/Eyho Cao/Documents/GitHub/CPS707/modules/admin/daily_transaction_file.txt"
        expectedf = "../ExpectedOutput/create_valid_admin.txt"
        self.assertTrue(filecmp.cmp(testf, expectedf))

    def test_create_username_taken(self):
        fsUser = "billy4"
        try:
            self.user.createUser(fsUser, "FS")
        except ValueError as e:
            self.assertEqual(type(e), ValueError)

    def test_create_valid_full_standard(self):
        fsUser= "FSTest"
        self.user.createUser(fsUser, "FS")
        self.user.logout()
        testf = "C:/Users/Eyho Cao/Documents/GitHub/CPS707/modules/admin/daily_transaction_file.txt"
        expectedf = "../ExpectedOutput/create_valid_full_standard.txt"
        self.assertTrue(filecmp.cmp(testf, expectedf))

    def test_create_username_long(self):
        fsUser = "thisusernameistoolongtouse"
        try:
            self.user.createUser(fsUser, "FS")
        except ValueError as e:
            self.assertEqual(type(e), ValueError)


    def test_create_incorrect_param(self):
        fsUser = "Donny"
        try:
            self.user.createUser(fsUser, "SA")
        except ValueError as e:
            self.assertEqual(type(e), ValueError)

    def test_delete_invalid_username(self):
        fsUser = "NotUser"
        try:
            self.user.deleteUser(fsUser)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)

    def test_delete_logged_in(self):
        try:
            self.user.deleteUser(self.user.getUsername())
        except ValueError as e:
            self.assertEqual(type(e), ValueError)

    def test_delete_success(self):
        testName = "adminTest"
        self.user.deleteUser(testName)
        self.user.logout()
        testf = "C:/Users/Eyho Cao/Documents/GitHub/CPS707/modules/admin/daily_transaction_file.txt"
        expectedf = "../ExpectedOutput/delete_success.txt"
        self.assertTrue(filecmp.cmp(testf, expectedf))

    #sell tests skipped as it is covered in SellSUser(literally the same tests to be run)

    def test_buy_admin_ticket_count_exceeded(self):
        try:
            self.user.buy1("The Rumble in the Jungle", 5, "trinh")

        except ValueError as e:
            self.assertEqual(type(e), ValueError)


    def test_buy_admin_out_of_tickets(self):
        try:
            self.user.buy1("The Rumble in the Jungle", 9999999, "trinh")
        except ValueError as e:
            self.assertEqual(type(e), ValueError)

    def test_refund_invalid_amount(self):
        try:
            self.user.refund1("billy", "trinh", 9999999999)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)

    def test_refund_invalid_seller(self):
        try:
            self.user.refund1("billy", "notaUser", 10)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)

    def test_refund_invalid_buyer(self):
        try:
            self.user.refund1("notaUser", "trinh", 10)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)

    def test_refund_valid(self):
        self.user.refund1("billy", "trinh", 1)
        self.user.logout()
        testf = "C:/Users/Eyho Cao/Documents/GitHub/CPS707/modules/admin/daily_transaction_file.txt"
        expectedf = "../ExpectedOutput/refund_valid.txt"
        self.assertTrue(filecmp.cmp(testf, expectedf))

    def test_addcredit_admin_user_invalid(self):
        try:
            self.user.addCredit("notaUser", 100)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)

    def test_addcredit_admin_amount_invalid(self):
        try:
            self.user.addCredit("billy", 1001)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)

    def test_addcredit_admin_valid(self):
        self.user.addCredit("billy", 20)
        self.user.logout()
        testf = "C:/Users/Eyho Cao/Documents/GitHub/CPS707/modules/admin/daily_transaction_file.txt"
        expectedf = "../ExpectedOutput/addcredit_admin_valid.txt"
        self.assertTrue(filecmp.cmp(testf, expectedf))

if __name__ == '__main__':
    unittest.main()
