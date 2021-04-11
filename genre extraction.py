import pandas as pd

df = pd.read_csv (r'https://raw.githubusercontent.com/kennedywaite/CLPS0950FinalProject/main/netflix_titles.csv')
#print(df)

#loop through pandas DataFrame "listedin" column of genres and add genres
#to netflix_genres list
netflix_genres = []
for x in range(0,7787):
    netflix_genres.append(df.iat[x,10])
    
#creates a list of all the unique genres from the Netflix titles dataset
category_list = []
for x in range(0,len(netflix_genres)):
    text = netflix_genres[x]
    phrases = text.split(",")
    for y in range(0,len(phrases)):
        phrases[y] = phrases[y].lstrip()
        if phrases[y] not in category_list:
            category_list.append(phrases[y])

print(category_list)


