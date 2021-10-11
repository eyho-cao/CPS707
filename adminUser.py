import user

class AdminUser(User):
    def create(self, username, userType):
        if(len(username) > 25):
            print("Username must not exceed 25 character")
        if(checkUnique(username)):
            match userType:
                case 'admin':
                    #add admin account to database
                    print("New Account Created - Username: " +"Username")
                case 'full-standard':
                    #add FS account to db
                    print("New Account Created - Username: " +"Username")
                case 'buy-standard':
                    #add BS account to db
                    print("New Account Created - Username: " +"Username")
                case 'sell-standard':
                    #add SS account to db
                    print("New Account Created - Username: " +"Username")
                case _:
                    print("Username already taken")
        else:
            print("username has been taken")

    def buy(self, title, numTickets, sellName):
        return 0

    def delete(self, username):
        return 0

    def refund(self, buyName, sellName, amount):
        return 0

    def addCredit(self, username, amount):
        return 0

    def checkUnique(username):
        return 0