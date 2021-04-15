#trying to test out creating new users and doing similarity indexes between
#users to make an algorithm for a Netflix recommendation engine
import numpy as np

user_matrix = np.zeros((4,7787))
print(user_matrix)

new_user = input("Are you a new user? [Yes/No]")

if (new_user == "Yes"):
    #add new row to user_matrix
    user_matrix.append((np.zeros(1,7787)))
elif (new_user == "No"):
    user_matrix.append(1)
    #ask for username
else: 
    new_user = input("Are you a new user? [Yes/No]")