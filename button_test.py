import tkinter as tk
import pandas as pd
import math

class Application(tk.Frame):
    
    def __init__(self, dataFrame, ran_list, button_identities, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH,expand=True)
        counter=0
        #master.geometry("300x500")
        self.create_quit()
        for x in ran_list:
            self.create_genre_widgets(str(x), counter, button_identities)
            counter = counter+1
        self.create_ok_button(button_identities)
            
    def genre_clicked(self, m_title, button_identities, counter):
        user_input = str(m_title)
        output_list = []
        for x in range(0,7787):
            text = df.iat[x,genres_col]
            if user_input in text:
                output_list.append(df.iat[x,2])
        print(output_list)
        #self.button.configure(bg="red")
        
        
            
        
        button_name = (button_identities[counter])
        button_name.configure(bg="red")
        
    #def update_list(self, output_list, current_list):
        #if current list is empty then equal to output list
        #else only keep same elements between lists
        
        #return current_list
        
    def create_ok_button(self, button_identity):
        self.button = tk.Button(self,text="OK",fg="blue",command =lambda: self.ok_clicked(button_identity))
        
        self.button.grid(row = 8, column=2, pady=100)
        
        
    def ok_clicked(self, but_id):
        new_list = []
        
        for x in but_id:
            if x.cget("bg") == 'red':
                new_list.append(x.cget("text"))
        print(new_list)
                
        
                
            
        #find the red buttons
        #compile respective lists to form new list with the common elements
        #return the new list
        
    

    def create_genre_widgets(self, m_title, counter, button_identities):
        
        self.button = tk.Button(self,text=str(m_title),command =lambda: self.genre_clicked(m_title,button_identities,counter))
        #self.button["text"] = str(m_title)
      
            
        self.button.grid(row= counter%6, column=counter%7)
            
        button_identities.append(self.button)
        
        #self.button = tk.set_location(counter)
        #real_row = counter/5 - 1
        #real_col = counter%5 - 1
        #real_row, real_col = self.set_location(self, counter)
        #self.button.grid(real_row,real_col)
        #Instead create a variable that takes the output from the button click 
        #and sets that variable as the input for the 'tag' corresponding with
        #each show's title
        #Do this without breaking this code though, read up on TKinter's documentation

    #def set_location(self, counter):
    #    row = counter/5 - 1
    #    col = counter%5 - 1
    #    return row, col
        
    #create an ok button that when clicked, it will take all the options and move
    #to a different page where all the Netflix titles of those options will appear
    #def create_OK(self):
    
            
    def create_quit(self):
     
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row = 8, column = 4, pady=100)

   
        
        

def category_extraction(dataF, col_num):
#loop through pandas DataFrame column "col_num" and make a list of all entries
    list_items = []
    for x in range(0,7787):
        list_items.append(dataF.iat[x,col_num])
    
#creates a list of all the unique items from list of entries in col_num column
    category_list = []
    for x in range(0,len(list_items)):
        if (type(list_items[x]) != float):
            text = list_items[x]
            phrases = text.split(",")
            for y in range(0,len(phrases)):
                phrases[y] = phrases[y].lstrip()
                if phrases[y] not in category_list:
                    category_list.append(phrases[y])

    return(category_list)



df = pd.read_csv (r'https://raw.githubusercontent.com/kennedywaite/CLPS0950FinalProject/main/netflix_titles.csv')
        
genres_col = 10
        
genre_list = category_extraction(df,genres_col)
current_list = []
button_identities = [] 

root = tk.Tk()
app = Application(df, genre_list, button_identities, master=root)
app.mainloop()

