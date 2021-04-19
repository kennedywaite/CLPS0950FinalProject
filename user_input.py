#trying to test out creating new users and doing similarity indexes between
#users to make an algorithm for a Netflix recommendation engine
import numpy as np

user_matrix = np.zeros((4,7787))
username_list = ['Ashley', 'Kennedy', 'Bryan', 'Erik']
print(user_matrix)

new_user = input("Are you a new user? [Yes/No] ")

if (new_user == "Yes"):
    #add new row to user_matrix
    user_matrix = np.vstack((user_matrix,(np.zeros((1,7787)))))
    user_name = input("Input a username: ")
    if isinstance(user_name, str) == True:
        username_list.append(user_name)
    else:
        user_name = input("Input a username: ")
elif (new_user == "No"):
    user_name = input("What is your user name? ")
    #ask for username
else: 
    new_user = input("Are you a new user? [Yes/No] ")
    
print(user_matrix)
print(username_list)