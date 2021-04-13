import tkinter as tk
import pandas as pd


class Application(tk.Frame):
    def __init__(self, ran_list, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
       
        for x in ran_list:
            self.create_widgets(str(x))
        
        
        self.create_quit()
        
    def list_movie(self, m_title):


        print(str(m_title))
    
        
    def create_widgets(self, m_title):
        self.button = tk.Button(self, command =lambda: self.list_movie(m_title))
        self.button["text"] = str(m_title)
      
        self.button.pack(side="top")
        #Instead create a variable that takes the output from the button click 
        #and sets that variable as the input for the 'tag' corresponding with
        #each show's title
        #Do this without breaking this code though, read up on TKinter's documentation

        
        
    def create_quit(self):
     
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

   
        
        

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

root = tk.Tk()
app = Application(genre_list, master=root)
app.mainloop()