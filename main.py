"""
RUN THIS FILE!!
This is the main file for the Netflix organizer program. You can run this
file and go through the program on the user interface. You will first be
prompted to start the program on a Welcome Page, and then you can choose
a category that you would like know more about. Then, you will be shown
42 different items of this category. You can choose to refresh if you would
like to see more options. If you select an option(s), it will show you a
list of 10 random Netflix titles for the criteria you selected. Clicking on
one of these shows will open up a window with the information of that Netflix
title. 
""" 

import tkinter as tk
import pandas as pd
import random
import math
import numpy

#creating the application for the user interface where users will be able to 
#find movies and TV shows (titles) on Netflix based on their selections, along with
#information about those Netflix titles based on the Kaggle dataset. This 
#application is also called when switching pages between the Welcome Page
#and this first page

class Application(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Netflix Recommendation Program")
        self._frame = None
        self.switch_frame(WelcomePage)
    
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        
#first we want to have a welcome page that displays "Welcome" along with a
#Start button. This is within a class because it is the first frame.
class WelcomePage(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        self.configure(bg = 'black')
        tk.Label(self, text="Welcome to Netflix Recommendations!", bg = 'black', fg = 'red', font=('Helvetica', 14, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Start",font=('Comic Sans MS',12), bg='white',fg = 'black' ,command=lambda: master.switch_frame(PageOne)).pack()

#the second frame and class is PageOne. Here there are buttons for users to 
#search by category. User can choose to search by genre, release year, etc.
#Clicking on a button will direct the user to the appropriate page for that
#category.
class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='white')
        tk.Label(self, text="Choose what category to search by.", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Genres",font=('Helvetica', 12),command=lambda: master.switch_frame(PageTwo)).pack()
        tk.Button(self, text="Country",font=('Helvetica', 12),command=lambda: master.switch_frame(PageThree)).pack()
        tk.Button(self, text="Year Released",font=('Helvetica', 12),command=lambda: master.switch_frame(PageFour)).pack()
        tk.Button(self, text="Director",font=('Helvetica', 12),command=lambda: master.switch_frame(PageFive)).pack()
        tk.Button(self, text="Go Back ",font=('Helvetica', 14, 'bold'),command=lambda: master.switch_frame(WelcomePage)).pack()

#the third frame and class is PageTwo. Here there are buttons for user to 
#search for items in the Genre category. This is where buttons are added to
#the window and where the functionality for each of the buttons is created
class PageTwo(tk.Frame):

    #this function is called when the PageTwo function is called to display
    #show titles by genre. It calls all the functions that are defined in
    #this class to make buttons for the genre portion of the program
    def __init__(self, master): 
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='red')
        tk.Label(self, text="Search by Genre", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH,expand=True)
        counter=0
        self.create_quit(master)
        button_identities = []
        for x in genre_list:
            self.create_genre_widgets(str(x), counter, button_identities)
            counter = counter+1
        self.create_inc(button_identities)
        self.create_exc(button_identities)
        self.create_refresh(genre_list,button_identities)
        
    #this function creates an output list of Netflix titles that fit the
    #selection made and then turns the button that was clicked red
    def genre_clicked(self, m_title, button_identities, counter):
        user_input = str(m_title)
        output_list = []
        for x in range(0,7787):
            text = df.iat[x,genres_col]
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
                text = df.iat[y,genres_col]
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
            text = df.iat[y,genres_col]
            if all(x in text for x in new_list):
                output_list.append(df.iat[y,2])
        self.show_titles(output_list)
    
    #this function creates the buttons/widgets for the category the user is 
    #searching by (genre, year released, etc.). It also places the location of
    #each button on the grid so they look pretty.
    def create_genre_widgets(self, m_title, counter, button_identities):
        self.button = tk.Button(self,text=str(m_title),command =lambda: self.genre_clicked(m_title,button_identities,counter))
        self.button.grid(row= counter%6, column=counter%7)
        button_identities.append(self.button)
                    
    #the creation of the quit button is in this function. the quit button just
    #allows the user to exit from the organization system. 
    def create_quit(self, master):
        self.quit = tk.Button(self, text="QUIT", fg="red",command=self.master.destroy)
        self.quit.grid(row = 9, column = 4, pady=100)
    
    #this function creates a refresh button that can be used to change the
    #the buttons for the category page
    def create_refresh(self,ran_list,button_identities):
        self.refresh = tk.Button(self, text='REFRESH', font=('Helvetica', 18, "bold"), fg = 'purple', command =lambda: self.refresh_list(ran_list, button_identities))
        self.refresh.grid(row = 8, column = 3, pady=20)
    
    #this function is called when the refresh button is clicked. It goes 
    #through the text of each of the existing buttons and goes through
    #a list of all items to create a remaining_list. The existing buttons
    #are then destroyed, and new buttons are made from remaining_list. The
    #refresh and ok buttons are then updated as well.
    def refresh_list(self,ran_list,button_identities):
        remaining_list = ran_list
        for x in button_identities:
           existing_button = x.cget("text")
           for y in remaining_list:
               if (y == existing_button) and (isinstance(y,str) == True):
                   remaining_list.remove(y)
           x.destroy()
        
        if (len(remaining_list) != 0):
            button_identities = []
            new_counter = 0
            if (len(remaining_list) >= 42):
                needed_range = 42
            else:
                needed_range = len(remaining_list)
            #print(needed_range)
            for i in range(0,needed_range):
                x = remaining_list[i]
                if (isinstance(x,str) == True) or (isinstance(x,int) == True):
                    self.create_genre_widgets(str(x), new_counter, button_identities)
                    new_counter += 1
               
                self.refresh.destroy()
                self.refresh = tk.Button(self, text='REFRESH', font=('Helvetica', 18, "bold"), fg = 'purple', command =lambda: self.refresh_list(ran_list, button_identities))
                self.refresh.grid(row = 8, column = 3, pady=20)
        else:
            tk.Label(self,text="You've seen all the options. Press quit to restart program.").grid(row=0,column=3,pady=10)
            self.refresh.destroy()
            self.refresh = tk.Button(self, text='REFRESH', font=('Helvetica', 18, "bold"), fg = 'purple', command = self.master.destroy)
            self.refresh.grid(row = 8, column = 3, pady=20)

            print("seen all the options")

    #this function displays 10 random movie and tv show titles from the 
    #shows_list based on the genres selected and whether it was inclusive
    #or exclusive. We use a counter because if there are 0 movies that match
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

#This new page class is for the country column of the dataset. So once this
#page is called, it will display buttons for multiple different countries
#that Netflix titles are offered in            
class PageThree(tk.Frame):
    
    def __init__(self, master): 
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='red')
        tk.Label(self, text="Search by Country", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH,expand=True)
        counter=0
        self.create_quit()
        button_identities = []
        for i in range(0,42):
            x = country_list[i]
            self.create_country_widgets(str(x), counter, button_identities)
            counter = counter+1
        self.create_ok(button_identities)
        self.create_refresh(country_list, button_identities)
        
        
    #this function creates an output list of Netflix titles that fit the
    #selection made and then turns the button that was clicked red
    def country_clicked(self, m_title, button_identities, counter):
        user_input = str(m_title)
        output_list = []
        for x in range(0,7787):
            text = str(df.iat[x,country_col])
            if user_input in text:
                output_list.append(df.iat[x,2])
            
        button_name = (button_identities[counter])
        button_name.configure(bg="red")
    
    #creates the "OK" button which is clicked when the user wants to 
    #find titles that include either of the buttons clicked            
    def create_ok(self, button_identity):
        self.ok = tk.Button(self,text="OK",fg="blue",command =lambda: self.ok_clicked(button_identity))
        self.ok.grid(row = 9, column=2, pady=100)
    
    #this function is called when the "OK" button is clicked, then the 
    #function will create a new window that shows all of the Netflix titles
    #that contain ANY of the countries that were selected by the user
    def ok_clicked(self, but_id):
        new_list = []
        for x in but_id:
            if x.cget("bg") == 'red':
                new_list.append(x.cget("text"))
                
        output_list = [] 
        for x in new_list:
            for y in range(0,7787):
                text = str(df.iat[y,country_col])
                if (str(x) in text) and (df.iat[y,2] not in output_list):
                    output_list.append(df.iat[y,2])
        self.show_titles(output_list)
        
    #this function creates the buttons/widgets for countries. It also places 
    #the location of each button on the grid so they look pretty.
    def create_country_widgets(self, m_title, counter, button_identities):
        self.button = tk.Button(self,text=str(m_title),command =lambda: self.country_clicked(m_title,button_identities,counter))
        row_num = math.floor(counter/7)
        col_num = counter%7
        if col_num == 0:
            self.button.grid(row=row_num,column=col_num,sticky=tk.SW)
        else:
            self.button.grid(row=row_num,column=col_num,sticky=tk.NE)
        button_identities.append(self.button)
                    
    #the creation of the quit button is in this function. the quit button just
    #allows the user to exit from the recommendation system.
    def create_quit(self):
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row = 9, column = 4, pady=100)
    
    #this function creates a refresh button that can be used to change the
    #the buttons for the category page
    def create_refresh(self,ran_list,button_identities):
        self.refresh = tk.Button(self, text='REFRESH', font=('Helvetica', 18, "bold"), fg = 'purple', command =lambda: self.refresh_list(ran_list, button_identities))
        self.refresh.grid(row = 8, column = 3, pady=20)
        
    #this function is called when the refresh button is clicked. It goes 
    #through the text of each of the existing buttons and goes through
    #a list of all items to create a remaining_list. The existing buttons
    #are then destroyed, and new buttons are made from remaining_list. The
    #refresh and ok buttons are then updated as well.
    def refresh_list(self,ran_list,button_identities):
        remaining_list = ran_list
        for x in button_identities:
           existing_button = x.cget("text")
           for y in remaining_list:
               if (y == existing_button) and (isinstance(y,str) == True):
                   remaining_list.remove(y)
           x.destroy()
        
        if (len(remaining_list) != 0):
            new_button_identities = []
            new_counter = 0
            if (len(remaining_list) >= 42):
                needed_range = 42
            else:
                needed_range = len(remaining_list)
            for i in range(0,needed_range):
                x = remaining_list[i]
                if (isinstance(x,str) == True) or (isinstance(x,int) == True):
                    self.create_country_widgets(str(x), new_counter, new_button_identities)
                    new_counter += 1
                self.refresh.destroy()
                self.refresh = tk.Button(self, text='REFRESH', font=('Helvetica', 18, "bold"), fg = 'purple', command =lambda: self.refresh_list(ran_list, new_button_identities))
                self.refresh.grid(row = 8, column = 3, pady=20)
            self.ok.destroy()
            self.create_ok(new_button_identities)
        else:
            tk.Label(self,text="You've seen all the options. Press quit to restart program.").grid(row=0,column=3,pady=10)
            self.refresh.destroy()
            self.refresh = tk.Button(self, text='REFRESH', font=('Helvetica', 18, "bold"), fg = 'purple', command = self.master.destroy)
            self.refresh.grid(row = 8, column = 3, pady=20)
            print("seen all the options")
             
    #this function displays 10 random movie and tv show titles from the 
    #shows_list based on the countries selected and whether it was inclusive
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
        
        if (len(shows_list) >= 10):
            rand_list = random.sample(shows_list,10)
        else:
            rand_list = shows_list
            
        for x in rand_list:
            self.create_show_titles(newWindow,str(x),new_counter,new_button_identities)
            new_counter +=1
            
    #this function creates a new window to display the movie/tv info. We do
    #this by calling the show_title_info function and passing in the newWindow,
    #counter, and button_identity     
    def create_show_titles(self,newWindow,show_title,counter,button_identity):
            newWindow.button = tk.Button(newWindow,text=str(show_title), command=lambda: self.show_title_info(newWindow,counter,button_identity))         
            newWindow.button.grid(row=(counter%2+1), column=counter%5)
            button_identity.append(newWindow.button)
    
    #this is to display the information of the title selected (all categories
    #are shown including actors, genres, year released, director, description,
    #and more). We used a for loop to search the entire list of titles and 
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

#This page is for the year released category. The years are sorted in 
#ascending order.
class PageFour(tk.Frame):

    def __init__(self, master): 
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='red')
        master.rowconfigure(0,weight=1)
        master.columnconfigure(0,weight=1)
        tk.Label(self, text="Search by Year Released", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to Search by Categories",command=lambda: master.switch_frame(PageOne)).pack()
        
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH,expand=True)
        counter=0
        self.create_quit()
        button_identities = []
        for i in range(0,42):
            x = year_list[i]
            self.create_year_widgets(str(x), counter, button_identities)
            counter = counter+1
        self.create_ok(button_identities)
        self.create_refresh(year_list, button_identities)
        
    #this function creates an output list of Netflix titles that fit the
    #selection made and then turns the button that was clicked red
    def year_clicked(self, m_title, button_identities, counter):
        user_input = str(m_title)
        output_list = []
        for x in range(0,7787):
            text = str(df.iat[x,release_col])
            if user_input in text:
                output_list.append(df.iat[x,2])
        button_name = (button_identities[counter])
        button_name.configure(bg="red")
    
    #creates the "OK" button which is clicked when the user wants to 
    #find titles that include either of the buttons clicked            
    def create_ok(self, button_identity):
        self.ok = tk.Button(self,text="OK",fg="blue",command =lambda: self.ok_clicked(button_identity))
        
        self.ok.grid(row = 9, column=2, pady=100)
    
    #this function is called when the "Inclusive" button is clicked, then the 
    #function will create a new window that shows all of the Netflix titles
    #that contain ANY of the items that were selected by the user
    def ok_clicked(self, but_id):
        new_list = []
        for x in but_id:
            if x.cget("bg") == 'red':
                new_list.append(x.cget("text"))
                
        output_list = [] 
        for x in new_list:
            for y in range(0,7787):
                text = str(df.iat[y,release_col])
                if (x in text) and (str(df.iat[y,2]) not in output_list):
                    output_list.append(df.iat[y,2])
        self.show_titles(output_list)
        
    #this function creates the buttons/widgets for the year released category. 
    #It also places the location of each button on the grid so they look pretty.
    def create_year_widgets(self, m_title, counter, button_identities):
        self.button = tk.Button(self,text=str(m_title),command =lambda: self.year_clicked(m_title,button_identities,counter))
        row_num = math.floor(counter/7)
        col_num = counter%7
        if col_num == 0:
            self.button.grid(row=row_num,column=col_num,sticky=tk.SW)
        else:
            self.button.grid(row=row_num,column=col_num,sticky=tk.NE)
        button_identities.append(self.button)
                    
    #the creation of the quit button is in this function. the quit button just
    #allows the user to exit from the recommendation system. 
    def create_quit(self):
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row = 9, column = 4, pady=100)
    
    #this function creates a refresh button that can be used to change the
    #the buttons for the category page
    def create_refresh(self,ran_list,button_identities):
        self.refresh = tk.Button(self, text='REFRESH', font=('Helvetica', 18, "bold"), fg = 'purple', command =lambda: self.refresh_list(ran_list, button_identities))
        self.refresh.grid(row = 8, column = 3, pady=20)
    
    #this function is called when the refresh button is clicked. It goes 
    #through the text of each of the existing buttons and goes through
    #a list of all items to create a remaining_list. The existing buttons
    #are then destroyed, and new buttons are made from remaining_list. The
    #refresh and ok buttons are then updated as well.
    def refresh_list(self,ran_list,button_identities):
        remaining_list = ran_list
        for x in button_identities:
           existing_button = x.cget("text")
           for y in remaining_list:
               if (str(y) == str(existing_button)) and ((isinstance(y,str) == True) or (isinstance(y,numpy.int64) == True)):
                   remaining_list.remove(y)
           x.destroy()
        if (len(remaining_list) != 0):
            button_identities = []
            new_counter = 0
            if (len(remaining_list) >= 42):
                needed_range = 42
            else:
                needed_range = len(remaining_list)
            #print(needed_range)
            for i in range(0,needed_range):
                x = remaining_list[i]
                if (isinstance(x,str) == True) or (isinstance(x,numpy.int64) == True):
                    self.create_year_widgets(str(x), new_counter, button_identities)
                    new_counter += 1
               
                self.refresh.destroy()
                self.refresh = tk.Button(self, text='REFRESH', font=('Helvetica', 18, "bold"), fg = 'purple', command =lambda: self.refresh_list(ran_list, button_identities))
                self.refresh.grid(row = 8, column = 3, pady=20)
            
            self.ok.destroy()
            self.create_ok(button_identities)
        else:
            tk.Label(self,text="You've seen all the options. Press quit to restart program.").grid(row=0,column=3,pady=10)
            self.refresh.destroy()
            self.refresh = tk.Button(self, text='REFRESH', font=('Helvetica', 18, "bold"), fg = 'purple', command = self.master.destroy)
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
        
        if (len(shows_list) >= 10):
            rand_list = random.sample(shows_list,10)
        else:
            rand_list = shows_list
            
        for x in rand_list:
            self.create_show_titles(newWindow,x,new_counter,new_button_identities)
            new_counter +=1
            
    #this function creates a new window to display the movie/tv info. We do
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
            title = str(df.iat[i,2])
            if (button_identity[counter].cget('text') == title):
                row = df.loc[i,:]
                for index, col in row.iteritems():
                    info_text = info_text + (str(index) + ': ' + str(col) + '\n')
                    
        infoWindow = tk.Toplevel(self.master)
        infoWindow.title("Information on Selected Show")
        tk.Label(infoWindow,text=("Here is your information:\n" + info_text)).pack()
    
#This last page class is for the directors column of the data set. This is the
#largest list of the four pages.
class PageFive(tk.Frame):

    def __init__(self, master): 
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='red')
        tk.Label(self, text="Search by Director", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to Search by Categories",command=lambda: master.switch_frame(PageOne)).pack()
        
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH,expand=True)
        counter=0
        self.create_quit()
        button_identities = []
        for i in range(0,42):
            x = director_list[i]
            self.create_director_widgets(str(x), counter, button_identities)
            counter = counter+1
        self.create_ok(button_identities)
        self.create_refresh(director_list, button_identities)
        
    #this function creates an output list of Netflix titles that fit the
    #selection made and then turns the button that was clicked red
    def director_clicked(self, m_title, button_identities, counter):
        user_input = str(m_title)
        output_list = []
        for x in range(0,7787):
            text = str(df.iat[x,director_col])
            if user_input in text:
                output_list.append(df.iat[x,2])
            
        button_name = (button_identities[counter])
        button_name.configure(bg="red")
    
    #creates the "OK" button which is clicked when the user wants to 
    #find titles that include either of the buttons clicked            
    def create_ok(self, button_identity):
        self.ok = tk.Button(self,text="OK",fg="blue",command =lambda: self.ok_clicked(button_identity))
        self.ok.grid(row = 9, column=2, pady=100)
    
    #this function is called when the "OK" button is clicked, then the 
    #function will create a new window that shows all of the Netflix titles
    #that contain ANY of the items that were selected by the user
    def ok_clicked(self, but_id):
        new_list = []
        for x in but_id:
            if x.cget("bg") == 'red':
                new_list.append(x.cget("text"))
                
        output_list = [] 
        for x in new_list:
            for y in range(0,7787):
                text = str(df.iat[y,director_col])
                if (x in text) and (str(df.iat[y,2]) not in output_list):
                    output_list.append(df.iat[y,2])
        self.show_titles(output_list)
    
    #this function creates the buttons/widgets for the directors category. 
    #It also places the location of each button on the grid so they look pretty.
    def create_director_widgets(self, m_title, counter, button_identities):
        self.button = tk.Button(self,text=str(m_title),command =lambda: self.director_clicked(m_title,button_identities,counter))
        self.button.grid(row= counter%6, column=counter%7)
        button_identities.append(self.button)
                    
    #the creation of the quit button is in this function. 
    def create_quit(self):
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row = 9, column = 4, pady=100)
    
    #this function creates a refresh button that can be used to change the
    #the buttons for the category page
    def create_refresh(self,ran_list,button_identities):
        self.refresh = tk.Button(self, text='REFRESH', font=('Helvetica', 18, "bold"), fg = 'purple', command =lambda: self.refresh_list(ran_list, button_identities))
        self.refresh.grid(row = 8, column = 3, pady=20)
        
    #this function is called when the refresh button is clicked. It goes 
    #through the text of each of the existing buttons and goes through
    #a list of all items to create a remaining_list. The existing buttons
    #are then destroyed, and new buttons are made from remaining_list. The
    #refresh and ok buttons are then updated as well.
    def refresh_list(self,ran_list,button_identities):
        remaining_list = ran_list
        for x in button_identities:
           existing_button = x.cget("text")
           for y in remaining_list:
               if (y == existing_button) and (isinstance(y,str) == True):
                   remaining_list.remove(y)
           x.destroy()
        
        if (len(remaining_list) != 0):
            button_identities = []
            new_counter = 0
            if (len(remaining_list) >= 42):
                needed_range = 42
            else:
                needed_range = len(remaining_list)
            #print(needed_range)
            for i in range(0,needed_range):
                x = remaining_list[i]
                if (isinstance(x,str) == True) or (isinstance(x,int) == True):
                    self.create_director_widgets(str(x), new_counter, button_identities)
                    new_counter += 1
               
                self.refresh.destroy()
                self.refresh = tk.Button(self, text='REFRESH', font=('Helvetica', 18, "bold"), fg = 'purple', command =lambda: self.refresh_list(ran_list, button_identities))
                self.refresh.grid(row = 8, column = 3, pady=20)
            self.ok.destroy()
            self.create_ok(button_identities)
        else:
            tk.Label(self,text="You've seen all the options. Press quit to restart program.").grid(row=0,column=3,pady=10)
            self.refresh.destroy()
            self.refresh = tk.Button(self, text='REFRESH', font=('Helvetica', 18, "bold"), fg = 'purple', command = self.master.destroy)
            self.refresh.grid(row = 8, column = 3, pady=20)
            print("seen all the options")
             
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
            
        if (len(shows_list) >= 10):
            rand_list = random.sample(shows_list,10)
        else:
            rand_list = shows_list
            
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
    #and more). We used a for loop to search the entire list of titles and 
    #compare each to the button_identity to find the correct title to display.
    def show_title_info(self,newWindow,counter,button_identity):
        button_name = (button_identity[counter])
        button_name.configure(bg="red")
        info_text = ""
        
        for i in range(0,7787):
            title = str(df.iat[i,2])
            if (button_identity[counter].cget('text') == title):
                row = df.loc[i,:]
                for index, col in row.iteritems():
                    info_text = info_text + (str(index) + ': ' + str(col) + '\n')
                    
        infoWindow = tk.Toplevel(self.master)
        infoWindow.title("Information on Selected Show")
        tk.Label(infoWindow,text=("Here is your information:\n" + info_text)).pack()
    
#this function is used to create a unique list of all the items in a 
#particular category. It takes all of the entries in the data set for a
#specific column and loops for repeats or empty entries.
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

#initializing the Kaggle Netflix data set 
df = pd.read_csv (r'https://raw.githubusercontent.com/kennedywaite/CLPS0950FinalProject/main/netflix_titles.csv')

#initializing the column numbers for each category  
genres_col = 10
director_col = 3
actor_col = 4
country_col = 5
release_col = 7
duration_col = 9

#calling category_extraction to get a unique list of items for each category
genre_list = category_extraction(df,genres_col)
director_list = category_extraction(df,director_col)
actor_list = category_extraction(df,actor_col)
country_list = category_extraction(df,country_col)
year_list = sorted(category_extraction(df,release_col))

#calling the class Application to create the window for the interface
if __name__ == "__main__":
    app = Application()
    app.mainloop()