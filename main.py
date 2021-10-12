from user import User
from BuySUser import BSUser
from SellSUser import SSUser
from fullSUser import FSUser
from adminUser import Admin
from login import Login
import pymongo

client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]

def main():
    command = ""
    loggedIn = False
    # wait for user to attempt to login
    while (command != "login"):
        print("1")
        command = input()
        if (command == "login"):
            break
    
    # check to see if user is logging in with a valid username
    while (not loggedIn):
        print("2")
        username = input("Username: ")
        Login.login(username)
        if (Login.login(username) == 0):
            print("successful login")
            break
    # user can attempt transactions or logout
    while (command != "logout"):
        print("3")
        command = input("")
        if (command == "logout"):
            break
        elif (command == "buy"):
            # buy method
            print("execute buy method")


        
if __name__ == "__main__":
    main()

            