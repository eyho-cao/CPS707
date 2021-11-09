from user import User
from BuySUser import BSUser
from SellSUser import SSUser
from fullSUser import FSUser
from admin import Admin
from login import Login
import pymongo
import os
import shlex

client = pymongo.MongoClient("mongodb+srv://ADMIN:ukdkXvAUbfYBFezo@cluster0.0eg8l.mongodb.net/cps707?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["cps707"] 
collection = db["users"]

def main():
    os.system('cls')
    command = ""
    loggedIn = False
    run = True
    user = None
    print("Welcome to the 'Totally Legit' Movie Ticketing System!\n\nEnter your command:")
    while(run):

        command = input()
        comList = shlex.split(command)
        if(len(command) > 0):

            #commands run while user logged in
            if(loggedIn):
                com = comList[0]
                comLen = len(comList)

                if(com == "login"):
                    print("Already Logged in")

                elif(com == "logout" or com == "Logout"):
                    user.addEventsDB()
                    user.logout()
                    user = None
                    loggedIn = False
                    print("User logged out")

                elif(com == "create" or com == "Create"):
                    if(comLen == 3):
                        user.createUser(comList[1], comList[2])
                    elif(comLen == 4):
                        user.createUser(comList[1], comList[2], float(comList[3]))
                    else:
                        print("Expected Usage: 'create (username) (type) (credit[optional])")

                elif(com == "delete" or com == "Delete"):
                    if(comLen == 2):
                        user.deleteUser(comList[1])
                    else:
                        print("Expected Usage: 'delete (username)'")

                elif(com =="sell" or com == "Sell"):
                    if(comLen == 4):
                        user.sell(comList[1], float(comList[2]), float(comList[3]))
                    else:
                        print("Expected Usage: 'sell (event name) (num. tickets) (sale price)'")

                elif(com == "buy" or com =="Buy"):
                    if(comLen == 4):
                        user.buy(comList[1], float(comList[2]), comList[3])
                    else:
                        print("Expected Usage: 'buy (event name) (num. tickets) (seller name)'")

                elif(com == "refund" or com == "Refund"):
                    if(comLen == 4):
                        user.refund(comList[2], comList[2], float(comList[3]))
                    else:
                        print("Expected Usage: 'refund (buyer) (seller) (amount)'")

                elif(com == "addcredit" or com == "Addcredit"):
                    if(user.getType() != "AA"):
                        if(comLen == 2):
                            user.addCredit(float(comList[2]))
                        else:
                            print("Expected Usage: 'addcredit (credit)'")
                    else:
                        if(comLen == 3):
                            user.addCredit(comList[1], float(comList[2]))
                        else:
                            print("Expected Usage: 'addcredit (username) (credit)'")
                elif(com == "close" or com == "Close"):
                    if(user.getType() == "AA"):
                        #EOD methods
                        user.endDay()
                    else:
                        print("Access Denied: Insufficient Permissions")


                elif(com == "help" and user.getType() == "AA"):
                    print("------------------\nList of Commands: \n------------------\nLogin\nLogout\nCreate\nDelete\nSell\nBuy\nRefund\nAddcredit\n------------------")
                elif(com == "help"):
                    print("------------------\nList of Commands: \n------------------\nLogin\nLogout\nSell\nBuy\nAddcredit\n------------------")
                else:
                    print("Invalid command, type 'help' for a list of commands")

            #wait for user login
            if(not loggedIn and (comList[0] == "login" or comList[0] == "Login")):
                if(len(comList) > 1):
                    user = Login.login(comList[1])
                    if(not user == 0 and not user == 1):
                        print("Successful Login || User: " +user.getUsername() +" Type: " +user.getType() +"\nEnter command:")
                        loggedIn = True
                    else:
                        print("Username not found")
                        user = None
                else:
                    print("Expected Usage: 'login (username)'")
            elif(not loggedIn and command == "exit"):
                run = False
                print("Quitting System......")
            elif(not loggedIn and not (comList[0] == "login" or comList[0] == "Login")):
                print("Please Login with 'login (username)'")
     
if __name__ == "__main__":
    main()

            
