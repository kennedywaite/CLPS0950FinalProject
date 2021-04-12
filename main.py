#main file to call table extraction functions

import pandas as pd

df = pd.read_csv (r'https://raw.githubusercontent.com/kennedywaite/CLPS0950FinalProject/main/netflix_titles.csv')
print(df)

#this function makes a list of all the different unique types of a category
#listed in
def category_extraction(dataF, col_num):
#loop through pandas DataFrame "listedin" column of genres and add genres
#to netflix_genres list
    netflix_genres = []
    for x in range(0,7787):
        netflix_genres.append(dataF.iat[x,col_num])
    
#creates a list of all the unique genres from the Netflix titles dataset
    category_list = []
    for x in range(0,len(netflix_genres)):
        text = netflix_genres[x]
        phrases = text.split(",")
        for y in range(0,len(phrases)):
            phrases[y] = phrases[y].lstrip()
            if phrases[y] not in category_list:
                category_list.append(phrases[y])

    return(category_list)


genres_col = 10
director_col = 3
actor_col = 4
country_col = 5
release_col = 7
duration_col = 9

genre_list = category_extraction(df,genres_col)
