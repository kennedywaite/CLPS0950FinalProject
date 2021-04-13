#trying to test out creating new users and doing similarity indexes between
#users to make an algorithm for a Netflix recommendation engine

user_matrix = []
new_user = input("Are you a new user? [Yes/No]")

if (new_user == "Yes"):
    #add new row to user_matrix
elif (new_user == "No"):
    #ask for username
else: 
    new_user = input("Are you a new user? [Yes/No]")