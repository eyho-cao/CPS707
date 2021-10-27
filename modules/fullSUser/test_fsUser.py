"""
    def test_delete_insufficient_credentials(self): #move this to FSUser
        fsUserObj = FSUser("billy")
        testFSName = "billytoo"
        try:
            fsUserObj.deleteUser(testFSName)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)

    def test_create_not_privilaged(self): #move this to FSUser
        fsUserObj = FSUser("billy")
        testFSName = "nagakabouros"
        try:
            fsUserObj.createUser(testFSName, "FS")
        except ValueError as e:
            self.assertEqual(type(e), ValueError)

"""