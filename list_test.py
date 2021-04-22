"""
DO NOT RUN THIS FILE
This file was used as a test to look at the unique lists for each category.
We used a lot of this code in the main file.
"""
import pandas as pd
import math

df = pd.read_csv (r'https://raw.githubusercontent.com/kennedywaite/CLPS0950FinalProject/main/netflix_titles.csv')
df.dropna()
#this function makes a list of all the different unique types of a category
#listed in
def category_extraction(dataF, col_num):
#loop through pandas DataFrame column "col_num" and make a list of all entries
    list_items = []
    for x in range(0,7787):
        list_items.append(dataF.iat[x,col_num])
    
#creates a list of all the unique items from list of entries in col_num column
    category_list = []
    for x in range(0,len(list_items)):
        if (type(list_items[x]) == str) and (list_items[x] != ''):
            text = list_items[x]
            phrases = text.split(",")
            for y in range(0,len(phrases)):
                phrases[y] = phrases[y].lstrip()
                if phrases[y] not in category_list:
                    category_list.append(phrases[y])
        else:
            if (list_items[x] not in category_list):
                category_list.append(list_items[x])
    
    category_list = [x for x in category_list if x == x]
    for x in category_list:
        if (x == ''):
            category_list.remove(x)
    
    return(category_list)

#these variables represent the length of ... why am i forgettin !?!?1 lol
genres_col = 10
director_col = 3
actor_col = 4
country_col = 5
release_col = 7
duration_col = 9


genre_list = category_extraction(df,genres_col)
director_list = category_extraction(df,director_col)
actor_list = category_extraction(df,actor_col)
country_list = category_extraction(df,country_col)
empty_entry = country_list[74]
release_list = category_extraction(df,release_col)
len_genre = len(genre_list)
len_director = len(director_list)
len_actor = len(actor_list)
len_country = len(country_list)
len_year = len(release_list)
print(len_year)
#len_release = len(release_list)

#for x in range(0,7787):
   # text = df.iat[x,genres_col]
    #if *user's input* in text:
      # print(df.iat[x,2])