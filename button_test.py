import tkinter as tk
import pandas as pd
import random
import math

#creating the application for the user interface where users will be able to 
#find movies and TV shows (titles) on Netflix based on their selections, along with
#information about those Netflix titles based on the Kaggle dataset
class Application(tk.Frame):
    
    def __init__(self, dataFrame, ran_list, button_identities, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH,expand=True)
        counter=0
        self.create_quit()
        #total_values = len(ran_list)
        for i in range(0,42):
            x = ran_list[i]
            self.create_genre_widgets(str(x), counter, button_identities)
            counter = counter+1
        self.create_inc(button_identities)
        self.create_exc(button_identities)
        self.create_refresh(ran_list,button_identities)
            
    #this function creates an output list of Netflix titles that fit the
    #selection made and then turns the button that was clicked red
    def genre_clicked(self, m_title, button_identities, counter):
        user_input = str(m_title)
        output_list = []
        for x in range(0,7787):
            text = df.iat[x,country_col]
            if user_input in text:
                output_list.append(df.iat[x,2])
            
        button_name = (button_identities[counter])
        button_name.configure(bg="red")
    
    #creates the "Inclusive" button which is clicked when the user wants to 
    #find titles that include either of the buttons clicked            
    def create_inc(self, button_identity):
        self.button = tk.Button(self,text="Inclusive",fg="blue",command =lambda: self.inc_clicked(button_identity))
        
        self.button.grid(row = 9, column=2, pady=100)
    
    #this function is called when the "Inclusive" button is clicked, then the 
    #function will create a new window that shows all of the Netflix titles
    #that contain ANY of the items that were selected by the user
    def inc_clicked(self, but_id):
        new_list = []
        
        for x in but_id:
            if x.cget("bg") == 'red':
                new_list.append(x.cget("text"))
                
        output_list = [] 
        
        for x in new_list:
            for y in range(0,7787):
                
                text = df.iat[y,country_col]
                if (x in text) and (df.iat[y,2] not in output_list):
                    output_list.append(df.iat[y,2])
        self.show_titles(output_list)
    
    #this function creates the "Exclusive" button which is clicked when the 
    #user wants to find titles that include every button that was clicked
    def create_exc(self, button_identity):
        self.button = tk.Button(self,text="Exclusive",fg="green",command =lambda: self.exc_clicked(button_identity))
        
        self.button.grid(row = 9, column=3, pady=100)     
    
    #this function is called when the "Exclusive" button is clicked, then the
    #function will create a new window that shows all of the Netflix titles 
    #that contain ALL of the items that were selected by the user
    def exc_clicked(self, but_id):
        new_list = []
        
        for x in but_id:
            if x.cget("bg") == 'red':
                new_list.append(x.cget("text"))
                
        output_list = []         
      
        for y in range(0,7787):
            
            text = df.iat[y,country_col]
            if all(x in text for x in new_list):
                output_list.append(df.iat[y,2])
        self.show_titles(output_list)
    
    #this function creates the buttons/widgets for the category the user is 
    #searching by (genre, year released, etc.). It also places the location of
    #each button on the grid so they look pretty.
    def create_genre_widgets(self, m_title, counter, button_identities):
        self.button = tk.Button(self,text=str(m_title),command =lambda: self.genre_clicked(m_title,button_identities,counter))        
        self.button.grid(row=counter%6, column=counter%7)
        button_identities.append(self.button)
                    
    #the creation of the quit button is in this function. the quit button just
    #allows the user to exit from the recommendation system. we may need to 
    #create a new quit button for each frame once we put them in frames
    def create_quit(self):
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row = 9, column = 4, pady=100)
        
    def create_refresh(self,ran_list,button_identities):
        self.refresh = tk.Button(self, text='REFRESH', font=('Helvetica', 18, "bold"), fg = 'purple', command =lambda: self.refresh_list(ran_list, button_identities))
        self.refresh.grid(row = 8, column = 3, pady=20)

    def refresh_list(self,ran_list,button_identities):
        remaining_list = ran_list
        for x in button_identities:
           existing_button = x.cget("text")
           for y in remaining_list:
               if (y == existing_button) and (isinstance(y,str) == True):
                   remaining_list.remove(y)
           x.destroy()
        
        new_counter = 0
        for i in range(0,42):
            x = remaining_list[i]
            if (isinstance(x,str) == True) or (isinstance(x,int) == True):
                self.create_genre_widgets(str(x), new_counter, button_identities)
                new_counter += 1
           
            self.refresh.destroy()
            self.refresh = tk.Button(self, text='REFRESH', font=('Helvetica', 18, "bold"), fg = 'purple', command =lambda: self.refresh_list(ran_list, button_identities))
            self.refresh.grid(row = 8, column = 3, pady=20)
        
    #this function displays 10 random movie and tv show titles from the 
    #shows_list based on the categories selected and whether it was inclusive
    #or exclusive. we use a counter because if there are 0 movies that match
    #the user's selection, we need to tell them to make a new selection. 
    def show_titles(self,shows_list):
        newWindow = tk.Toplevel(self.master)
        newWindow.title("10 Random Movies/TV Shows of Selected Items")
        new_counter = 0
        new_button_identities = []
        if (len(shows_list) == 0):
            tk.Label(newWindow,text="There are no Netflix titles that match your selections. Please try a different combination. ").grid(row=0,column=0,pady=10)
        else:
            tk.Label(newWindow,text="Here are your shows").grid(row=0,column=0,pady=10)
        rand_list = random.sample(shows_list,10)
        for x in rand_list:
            self.create_show_titles(newWindow,x,new_counter,new_button_identities)
            new_counter +=1
    
    #this function creates a new window to display the movie/tv info. we do
    #this by calling the show_title_info function and passing in the newWindow,
    #counter, and button_identity
    def create_show_titles(self,newWindow,show_title,counter,button_identity):
            newWindow.button = tk.Button(newWindow,text=str(show_title), command=lambda: self.show_title_info(newWindow,counter,button_identity))         
            newWindow.button.grid(row=(counter%2+1), column=counter%5)
            button_identity.append(newWindow.button)
    
    #this is to display the information of the title selected (all categories
    #are shown including actors, genres, year released, director, description,
    #and more). we used a for loop to search the entire list of titles and 
    #compare each to the button_identity to find the correct title to display.
    def show_title_info(self,newWindow,counter,button_identity):
        button_name = (button_identity[counter])
        button_name.configure(bg="red")
        info_text = ""
        
        for i in range(0,7787):
            title = df.iat[i,2]
            if (button_identity[counter].cget('text') == title):
                row = df.loc[i,:]
                for index, col in row.iteritems():
                    info_text = info_text + (str(index) + ': ' + str(col) + '\n')
                    
        infoWindow = tk.Toplevel(self.master)
        infoWindow.title("Information on Selected Show")
        tk.Label(infoWindow,text=("Here is your information:\n" + info_text)).pack()
        
# def category_extraction(dataF, col_num):
# #loop through pandas DataFrame column "col_num" and make a list of all entries
#     list_items = []
#     for x in range(0,7787):
#         list_items.append(dataF.iat[x,col_num])
    
# #creates a list of all the unique items from list of entries in col_num column
#     category_list = []
#     for x in range(0,len(list_items)):
#         if (type(list_items[x]) != float):
#             text = list_items[x]
#             if (text == ''):
#                 break
#             phrases = text.split(",")
#             for y in range(0,len(phrases)):
#                 phrases[y] = phrases[y].lstrip()
#                 if phrases[y] not in category_list:
#                     category_list.append(phrases[y])

#     return(category_list)

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
                print(list_items[x])
    
    category_list = [x for x in category_list if x == x]
    for x in category_list:
        if (x == ''):
            category_list.remove(x)
    
    return(category_list)


df = pd.read_csv (r'https://raw.githubusercontent.com/kennedywaite/CLPS0950FinalProject/main/netflix_titles.csv')
        
genres_col = 10
country_col = 5
director_col = 3
        
genre_list = category_extraction(df,genres_col)
country_list = category_extraction(df, country_col)
director_list = category_extraction(df,director_col)
current_list = []
button_identities = [] 

root = tk.Tk()
app = Application(df, country_list, button_identities, master=root)
app.mainloop()