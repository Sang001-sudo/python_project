from user import user as us


banner = """
####################
#   Skynet Bank    #
####################
"""

first_menu = """
[R] Register
[L] Login
[Q] Quit
"""


while True:
    print(banner)
    print(first_menu)
    option = str(input("Choose an option: ")).strip().upper()
    
    if option == "R":
        pass
    elif option == "L":
        pass
    elif option == "Q":
        print("Thank you for using Skynet Bank. Goodbye!")
        break
    else:
        print("Invalid option. Please try again.")
        continue
    