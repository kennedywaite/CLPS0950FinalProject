import tkinter as tk
import pandas as pd
import random

#creating the application for the user interface where users will be able to 
#find movies and TV shows (titles) on Netflix based on their selections, along with
#information about those Netflix titles based on the Kaggle dataset

class Application(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(WelcomePage)
    
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        
#first we want to have a welcomepage that displays "Welcome" along with a
#Start button. This is within a class because it is the first frame.
class WelcomePage(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Welcome to Netflix Recommendations!", font=('Helvetica', 14, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Start",font=('Comic Sans MS',12),command=lambda: master.switch_frame(PageOne)).pack()

#the second frame and class is PageOne. here there are buttons for user to 
#search by category. user can choose to search by genre, release year, etc.
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

#the third frame and class is PageTwo. here there are buttons for user to 
#search for items in category selected. tt is where bulk of the code is.
class PageTwo(tk.Frame):

    def __init__(self, master): #master=None might just be master
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
        
        self.button.grid(row = 8, column=2, pady=100)
    
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
        
        self.button.grid(row = 8, column=3, pady=100)     
    
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
    #allows the user to exit from the recommendation system. we may need to 
    #create a new quit button for each frame once we put them in frames
    def create_quit(self, master):
        self.quit = tk.Button(self, text="Go back to Search by Categories", fg="red", command=lambda: self.master.switch_frame(PageOne)).pack()

        #self.quit = tk.Button(self, text="QUIT", fg="red",
        #                      command=self.master.destroy)
        self.quit.grid(row = 8, column = 4, pady=100)
             
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
            
class PageThree(tk.Frame):
    
    def __init__(self, master): #master=None might just be master
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='red')
        tk.Label(self, text="Search by Country", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to Search by Categories",command=lambda: master.switch_frame(PageOne)).pack()
        
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH,expand=True)
        counter=0
        self.create_quit()
        button_identities = []
        for x in country_list:
            self.create_country_widgets(str(x), counter, button_identities)
            counter = counter+1
        self.create_inc(button_identities)
        self.create_exc(button_identities)
        
        
    #this function creates an output list of Netflix titles that fit the
    #selection made and then turns the button that was clicked red
    def country_clicked(self, m_title, button_identities, counter):
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
        
        self.button.grid(row = 8, column=2, pady=100)
    
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
        
        self.button.grid(row = 8, column=3, pady=100)     
    
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
    def create_country_widgets(self, m_title, counter, button_identities):
        self.button = tk.Button(self,text=str(m_title),command =lambda: self.country_clicked(m_title,button_identities,counter))
        self.button.grid(row= counter%6, column=counter%7)
        button_identities.append(self.button)
                    
    #the creation of the quit button is in this function. the quit button just
    #allows the user to exit from the recommendation system. we may need to 
    #create a new quit button for each frame once we put them in frames
    def create_quit(self):
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row = 8, column = 4, pady=100)
             
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
    
class PageFour(tk.Frame):

    def __init__(self, master): #master=None might just be master
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='red')
        tk.Label(self, text="Search by Year Released", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to Search by Categories",command=lambda: master.switch_frame(PageOne)).pack()
        
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH,expand=True)
        counter=0
        self.create_quit()
        button_identities = []
        for x in year_list:
            self.create_year_widgets(str(x), counter, button_identities)
            counter = counter+1
        self.create_inc(button_identities)
        self.create_exc(button_identities)
        
        
    #this function creates an output list of Netflix titles that fit the
    #selection made and then turns the button that was clicked red
    def year_clicked(self, m_title, button_identities, counter):
        user_input = str(m_title)
        output_list = []
        for x in range(0,7787):
            text = df.iat[x,release_col]
            if user_input in text:
                output_list.append(df.iat[x,2])
            
        button_name = (button_identities[counter])
        button_name.configure(bg="red")
    
    #creates the "Inclusive" button which is clicked when the user wants to 
    #find titles that include either of the buttons clicked            
    def create_inc(self, button_identity):
        self.button = tk.Button(self,text="Inclusive",fg="blue",command =lambda: self.inc_clicked(button_identity))
        
        self.button.grid(row = 8, column=2, pady=100)
    
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
                
                text = df.iat[y,release_col]
                if (x in text) and (df.iat[y,2] not in output_list):
                    output_list.append(df.iat[y,2])
        self.show_titles(output_list)
    
    #this function creates the "Exclusive" button which is clicked when the 
    #user wants to find titles that include every button that was clicked
    def create_exc(self, button_identity):
        self.button = tk.Button(self,text="Exclusive",fg="green",command =lambda: self.exc_clicked(button_identity))
        
        self.button.grid(row = 8, column=3, pady=100)     
    
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
            
            text = df.iat[y,release_col]
            if all(x in text for x in new_list):
                output_list.append(df.iat[y,2])
        self.show_titles(output_list)
    
    #this function creates the buttons/widgets for the category the user is 
    #searching by (genre, year released, etc.). It also places the location of
    #each button on the grid so they look pretty.
    def create_year_widgets(self, m_title, counter, button_identities):
        self.button = tk.Button(self,text=str(m_title),command =lambda: self.year_clicked(m_title,button_identities,counter))
        self.button.grid(row= counter%6, column=counter%7)
        button_identities.append(self.button)
                    
    #the creation of the quit button is in this function. the quit button just
    #allows the user to exit from the recommendation system. we may need to 
    #create a new quit button for each frame once we put them in frames
    def create_quit(self):
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row = 8, column = 4, pady=100)
             
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
    
class PageFive(tk.Frame):

    def __init__(self, master): #master=None might just be master
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
        for x in director_list:
            self.create_director_widgets(str(x), counter, button_identities)
            counter = counter+1
        self.create_inc(button_identities)
        self.create_exc(button_identities)
        
        
    #this function creates an output list of Netflix titles that fit the
    #selection made and then turns the button that was clicked red
    def director_clicked(self, m_title, button_identities, counter):
        user_input = str(m_title)
        output_list = []
        for x in range(0,7787):
            text = df.iat[x,director_col]
            if user_input in text:
                output_list.append(df.iat[x,2])
            
        button_name = (button_identities[counter])
        button_name.configure(bg="red")
    
    #creates the "Inclusive" button which is clicked when the user wants to 
    #find titles that include either of the buttons clicked            
    def create_inc(self, button_identity):
        self.button = tk.Button(self,text="Inclusive",fg="blue",command =lambda: self.inc_clicked(button_identity))
        
        self.button.grid(row = 8, column=2, pady=100)
    
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
                
                text = df.iat[y,director_col]
                if (x in text) and (df.iat[y,2] not in output_list):
                    output_list.append(df.iat[y,2])
        self.show_titles(output_list)
    
    #this function creates the "Exclusive" button which is clicked when the 
    #user wants to find titles that include every button that was clicked
    def create_exc(self, button_identity):
        self.button = tk.Button(self,text="Exclusive",fg="green",command =lambda: self.exc_clicked(button_identity))
        
        self.button.grid(row = 8, column=3, pady=100)     
    
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
            
            text = df.iat[y,director_col]
            if all(x in text for x in new_list):
                output_list.append(df.iat[y,2])
        self.show_titles(output_list)
    
    #this function creates the buttons/widgets for the category the user is 
    #searching by (genre, year released, etc.). It also places the location of
    #each button on the grid so they look pretty.
    def create_director_widgets(self, m_title, counter, button_identities):
        self.button = tk.Button(self,text=str(m_title),command =lambda: self.director_clicked(m_title,button_identities,counter))
        self.button.grid(row= counter%6, column=counter%7)
        button_identities.append(self.button)
                    
    #the creation of the quit button is in this function. the quit button just
    #allows the user to exit from the recommendation system. we may need to 
    #create a new quit button for each frame once we put them in frames
    def create_quit(self):
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row = 8, column = 4, pady=100)
             
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
    

def category_extraction(dataF, col_num):
#loop through pandas DataFrame column "col_num" and make a list of all entries
    list_items = []
    for x in range(0,7787):
        list_items.append(dataF.iat[x,col_num])
    
#creates a list of all the unique items from list of entries in col_num column
    category_list = []
    for x in range(0,len(list_items)):
        if (type(list_items[x]) == str):
            text = list_items[x]
            phrases = text.split(",")
            for y in range(0,len(phrases)):
                phrases[y] = phrases[y].lstrip()
                if phrases[y] not in category_list:
                    category_list.append(phrases[y])
        else:
            if list_items[x] not in category_list:
                category_list.append(list_items[x])
    
    category_list = [x for x in category_list if x == x]
    
    return(category_list)



df = pd.read_csv (r'https://raw.githubusercontent.com/kennedywaite/CLPS0950FinalProject/main/netflix_titles.csv')
        
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
year_list = category_extraction(df,release_col)

current_list = []
button_identities = [] 

#root = tk.Tk()
#app = Application()
#app = Application(df, genre_list, button_identities, master=root)

if __name__ == "__main__":
    app = Application()
    app.mainloop()